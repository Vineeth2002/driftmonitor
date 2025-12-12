import os
import json
from datetime import datetime
from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

RAW_DIR = "data/live/raw"
OUT_DIR = "data/live/processed"

def main():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    raw_day = os.path.join(RAW_DIR, today)
    out_day = os.path.join(OUT_DIR, today)

    if not os.path.isdir(raw_day):
        print("No raw data for today:", today)
        return

    os.makedirs(out_day, exist_ok=True)
    clf = SafetyClassifier()

    texts = []
    sources = []

    for f in os.listdir(raw_day):
        if f.endswith(".json"):
            with open(os.path.join(raw_day, f), encoding="utf-8") as fh:
                data = json.load(fh)
                for item in data.get("items", []):
                    text = f"{item.get('title','')} {item.get('text','')}".strip()
                    texts.append(text)
                    sources.append(item.get("source", "unknown"))

    results = clf.score_texts(texts)

    summary = {"SAFE": 0, "WARNING": 0, "RISKY": 0}
    for r in results:
        summary[r["risk_label"]] += 1

    with open(os.path.join(out_day, "safety_eval.json"), "w") as f:
        json.dump(results, f, indent=2)

    with open(os.path.join(out_day, "safety_summary.json"), "w") as f:
        json.dump({
            "date": today,
            "total_items": len(results),
            "risk_breakdown": summary
        }, f, indent=2)

    print("Safety evaluation completed for", today)

if __name__ == "__main__":
    main()
