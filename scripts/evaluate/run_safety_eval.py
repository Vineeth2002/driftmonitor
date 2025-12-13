import json
from pathlib import Path
from datetime import datetime, timezone

from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

RAW_BASE = Path("data/live/raw")
OUT_BASE = Path("data/live/processed")


def load_texts(obj):
    texts = []
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                if "text" in item:
                    texts.append(item["text"])
                elif "title" in item:
                    texts.append(item["title"])
    elif isinstance(obj, dict):
        for item in obj.get("results", []):
            if "text" in item:
                texts.append(item["text"])
            elif "title" in item:
                texts.append(item["title"])
    return texts


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_dir = RAW_BASE / today
    out_dir = OUT_BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)

    clf = SafetyClassifier()
    evaluated_items = []

    for fname in ["google_trends.json", "hackernews.json"]:
        fpath = raw_dir / fname
        if not fpath.exists():
            continue

        data = json.loads(fpath.read_text(encoding="utf-8"))
        texts = load_texts(data)
        scores = clf.score_texts(texts)

        for text, score in zip(texts, scores):
            evaluated_items.append({
                "source": fname.replace(".json", ""),
                "text": text,
                **score,
            })

    output = {
        "date": today,
        "total": len(evaluated_items),
        "items": evaluated_items,
    }

    (out_dir / "evaluated.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] Evaluated {len(evaluated_items)} items for {today}")


if __name__ == "__main__":
    main()
