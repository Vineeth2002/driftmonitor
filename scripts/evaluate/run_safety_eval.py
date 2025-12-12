from datetime import date
from pathlib import Path
import json

TODAY = date.today().isoformat()

RAW_DIR = Path("data/live/raw") / TODAY
OUT_DIR = Path("data/live/processed") / TODAY
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Load raw
items = []
for file in RAW_DIR.glob("*.json"):
    with open(file) as f:
        items.extend(json.load(f)["results"])

# Run SafetyClassifier → results
with open(OUT_DIR / "safety_results.json", "w") as f:
    json.dump(results, f, indent=2)
