import json
from pathlib import Path
from datetime import datetime
from collections import Counter

PROCESSED = Path("data/live/processed")
OUT = PROCESSED / "monthly"

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    month = datetime.utcnow().strftime("%Y-%m")

    agg = Counter()
    total = 0

    for d in PROCESSED.iterdir():
        if not d.is_dir() or not d.name.startswith(month):
            continue

        f = d / "evaluated.json"
        if not f.exists():
            continue

        data = json.loads(f.read_text(encoding="utf-8"))
        total += data.get("total", 0)

        for item in data.get("items", []):
            agg[item.get("risk_label", "UNKNOWN")] += 1

    summary = {
        "month": month,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_items": total,
        "risk_breakdown": dict(agg),
    }

    out_file = OUT / f"monthly_{month}.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("[OK] Monthly metrics written:", out_file)

if __name__ == "__main__":
    main()
