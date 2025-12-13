import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

PROCESSED = Path("data/live/processed")
OUT = PROCESSED / "weekly"

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    agg = Counter()
    total = 0

    for d in days:
        f = PROCESSED / d / "evaluated.json"
        if not f.exists():
            continue

        data = json.loads(f.read_text(encoding="utf-8"))
        total += data.get("total", 0)

        for item in data.get("items", []):
            agg[item.get("risk_label", "UNKNOWN")] += 1

    summary = {
        "window": "last_7_days",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_items": total,
        "risk_breakdown": dict(agg),
    }

    out_file = OUT / f"weekly_{today}.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("[OK] Weekly metrics written:", out_file)

if __name__ == "__main__":
    main()
