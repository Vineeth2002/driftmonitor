import pandas as pd
import glob
import os
from datetime import datetime

RISK_KEYWORDS = {
    "misinformation": ["fake", "hallucination", "misinformation"],
    "bias": ["bias", "fairness", "discrimination"],
    "misuse": ["misuse", "weapon", "abuse"],
    "governance": ["regulation", "policy", "law"],
}

files = glob.glob("data/raw/*.csv")
if not files:
    raise RuntimeError("No raw files to evaluate")

records = []

for file in files:
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()
        for category, keywords in RISK_KEYWORDS.items():
            score = sum(k in text for k in keywords)
            if score > 0:
                records.append({
                    "source_file": os.path.basename(file),
                    "category": category,
                    "risk_score": score,
                    "text": text[:300],
                    "date": datetime.utcnow().date()
                })

out_df = pd.DataFrame(records)

os.makedirs("data/evaluated", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")
out_path = f"data/evaluated/evaluated_{today}.csv"

out_df.to_csv(out_path, index=False)
print(f"[OK] Safety evaluation saved → {out_path}")
