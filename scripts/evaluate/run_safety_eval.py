import json
import os
from datetime import datetime
from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier

TODAY = datetime.utcnow().strftime("%Y-%m-%d")
RAW_DIR = f"data/live/raw/{TODAY}"
OUT_DIR = f"data/live/processed/{TODAY}"
os.makedirs(OUT_DIR, exist_ok=True)

clf = SafetyClassifier()

results = []

for file in os.listdir(RAW_DIR):
    with open(os.path.join(RAW_DIR, file)) as f:
        items = json.load(f)

    texts = [i["title"] for i in items]
    scores = clf.score_texts(texts)

    for item, score in zip(items, scores):
        results.append({
            **item,
            **score
        })

with open(f"{OUT_DIR}/evaluated.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Evaluated {len(results)} items")
