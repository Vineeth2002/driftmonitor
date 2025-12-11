#!/usr/bin/env python3
"""
Run Evaluation Pipeline for DriftMonitor (enhanced summary)

- Loads raw data from data/live/raw
- Applies SafetyClassifier
- Saves processed eval JSON: data/live/processed/eval_<ts>.json
- Saves a summary JSON: data/live/processed/eval_summary_<ts>.json
  which contains:
    - counts per sentiment label
    - number of risky items (safety_score < threshold)
    - top N risky examples (text, safety_score, reason)
"""

from __future__ import annotations
import os
import json
import glob
import logging
from datetime import datetime
from typing import List, Dict, Any

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier
from driftmonitor.scripts.evaluate.utils import load_latest_json, extract_text_fields

logger = logging.getLogger("driftmonitor.scripts.evaluate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

RAW_DIR = os.path.abspath("data/live/raw")
PROCESSED_DIR = os.path.abspath("data/live/processed")

# thresholds and parameters
SAFETY_THRESHOLD = 0.60  # anything below this considered 'risky' (tunable)
TOP_RISKY_N = 10


def evaluate() -> Dict[str, str]:
    """
    Run evaluation and summary creation.
    Returns a dict with keys: 'eval_file' and 'summary_file' (absolute paths).
    """
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Load raw files
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.json")))
    if not raw_files:
        raise RuntimeError("No raw data found in data/live/raw")

    logger.info("Found %d raw data files", len(raw_files))

    all_items: List[Dict[str, Any]] = []
    for path in raw_files:
        loaded = load_latest_json(path)
        results = loaded.get("results", [])
        if isinstance(results, list):
            all_items.extend(results)
    logger.info("Total combined items: %d", len(all_items))

    # Extract texts
    texts = extract_text_fields(all_items)
    logger.info("Extracted %d text fields to classify", len(texts))

    # Run classifier
    clf = SafetyClassifier()
    safety_results = clf.score_texts(texts)

    # Timestamps and output paths
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    eval_file = os.path.join(PROCESSED_DIR, f"eval_{ts}.json")
    summary_file = os.path.join(PROCESSED_DIR, f"eval_summary_{ts}.json")

    # Save full evaluation results
    full_output = {
        "evaluated_at": ts,
        "n_texts": len(texts),
        "safety_results": safety_results,
    }

    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump(full_output, f, indent=2, ensure_ascii=False)
    logger.info("Saved evaluation output → %s", eval_file)

    # Build summary: counts by sentiment label and risky items
    label_counts: Dict[str, int] = {}
    risky_items: List[Dict[str, Any]] = []
    for r in safety_results:
        lbl = (r.get("sentiment_label") or "UNKNOWN").upper()
        label_counts[lbl] = label_counts.get(lbl, 0) + 1
        try:
            ss = float(r.get("safety_score", 1.0))
        except Exception:
            ss = 1.0
        if ss < SAFETY_THRESHOLD:
            risky_items.append({
                "text": (r.get("text") or "")[:600],
                "safety_score": ss,
                "reason": r.get("reason", ""),
            })

    risky_items_sorted = sorted(risky_items, key=lambda x: x["safety_score"])[:TOP_RISKY_N]

    summary = {
        "evaluated_at": ts,
        "n_texts": len(texts),
        "label_counts": label_counts,
        "n_risky": len(risky_items),
        "risky_examples": risky_items_sorted,
        "safety_threshold": SAFETY_THRESHOLD,
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info("Saved evaluation summary → %s", summary_file)

    return {"eval_file": os.path.abspath(eval_file), "summary_file": os.path.abspath(summary_file)}


if __name__ == "__main__":
    out = evaluate()
    print(f"Evaluation complete: {out}")
