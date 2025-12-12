import os
import json
from datetime import datetime
from collections import Counter

RAW_DIR = "data/live/raw"
OUT_DIR = "data/live/processed/monthly"

def load_month(month_prefix: str):
    """
    month_prefix example: '2025-12'
    """
    items = []

    if not os.path.isdir(RAW_DIR):
        return items

    for day in os.listdir(RAW_DIR):
        if not day.startswith(month_prefix):
            continue

        day_dir = os.path.join(RAW_DIR, day)
        if not os.path.isdir(day_dir):
            continue

        for fname in os.listdir(day_dir):
            if fname.endswith(".json"):
                with open(os.path.join(day_dir, fname), encoding="utf-8") as f:
                    data = json.load(f)
                    items.extend(data.get("items", []))

    return items

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    month_prefix = datetime.utcnow().strftime("%Y-%m")
    items = load_month(month_prefix)

    source_count = Counter()
    keyword_count = Counter()

    for item in items:
        source_count[item.get("source", "unknown")] += 1
        title = item.get("title", "")
        keyword_count.update(title.lower().split())

    summary = {
        "month": month_prefix,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_items": len(items),
        "source_distribution": dict(source_count),
        "top_keywords": keyword_count.most_common(30),
    }

    out_file = f"{OUT_DIR}/monthly_{month_prefix}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Monthly summary written:", out_file)

if __name__ == "__main__":
    main()
