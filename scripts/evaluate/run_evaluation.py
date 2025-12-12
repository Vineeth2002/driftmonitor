#!/usr/bin/env python3
# driftmonitor/scripts/evaluate/run_evaluation.py
import os
import sys
import json
import glob
import logging
from datetime import datetime

logger = logging.getLogger("driftmonitor.scripts.evaluate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

RAW_DIR = os.path.abspath("data/live/raw")
PROCESSED_DIR = os.path.abspath("data/live/processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Minimal dummy safety classifier — replace with real model if available
def simple_safety_score(text: str) -> float:
    text = (text or "").lower()
    if any(w in text for w in ("harm", "attack", "bomb", "kill")):
        return 0.1
    if any(w in text for w in ("hate", "toxic", "abuse")):
        return 0.3
    if any(w in text for w in ("warning", "vulnerable", "exploit")):
        return 0.5
    return 0.95

def extract_texts_from_raw() -> list:
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.json")))
    texts = []
    for f in files:
        try:
            d = json.load(open(f, "r", encoding="utf-8"))
            if isinstance(d, dict):
                # allow both single and list forms
                if "text" in d:
                    texts.append(d.get("text", ""))
                else:
                    texts.append(json.dumps(d)[:1000])
            elif isinstance(d, list):
                for item in d:
                    if isinstance(item, dict):
                        texts.append(item.get("text", "") or json.dumps(item)[:1000])
                    else:
                        texts.append(str(item)[:1000])
        except Exception:
            continue
    return texts

def evaluate() -> dict:
    texts = extract_texts_from_raw()
    if not texts:
        raise RuntimeError("No raw data found in data/live/raw")

    results = []
    for t in texts:
        score = simple_safety_score(t)
        label = "RISKY" if score < 0.6 else "SAFE"
        reason = ""
        if score < 0.6:
            reason = "heuristic-risk"
        results.append({"text": t[:1000], "safety_score": score, "sentiment_label": label, "reason": reason})

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    eval_file = os.path.join(PROCESSED_DIR, f"eval_{ts}.json")
    summary_file = os.path.join(PROCESSED_DIR, f"eval_summary_{ts}.json")

    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info("Saved evaluation file: %s", eval_file)

    label_counts = {}
    risky = []
    for r in results:
        lbl = r.get("sentiment_label", "UNKNOWN")
        label_counts[lbl] = label_counts.get(lbl, 0) + 1
        if r.get("safety_score", 1.0) < 0.6:
            risky.append(r)

    summary = {"evaluated_at": ts, "n_texts": len(results), "label_counts": label_counts, "n_risky": len(risky), "risky_examples": risky[:10]}
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info("Saved evaluation summary: %s", summary_file)
    return {"eval_file": eval_file, "summary_file": summary_file}

if __name__ == "__main__":
    try:
        out = evaluate()
        print("Evaluation complete:", out)
    except Exception as e:
        logger.exception("Evaluation failed")
        raise
