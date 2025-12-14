import pandas as pd
import os
from datetime import datetime

RISK_KEYWORDS = {
    "AI safety": ["alignment", "hallucination", "unsafe", "robustness"],
    "AI regulation": ["law", "policy", "compliance", "regulation"],
    "AI bias": ["bias", "fairness", "discrimination"],
    "AI misuse": ["misuse", "deepfake", "fraud", "scam"]
}

def severity_label(risk_pct):
    if risk_pct < 1:
        return "🟢 LOW"
    elif risk_pct <= 5:
        return "🟡 MEDIUM"
    return "🔴 HIGH"

os.makedirs("data/evaluated", exist_ok=True)

input_files = os.listdir("data/raw")
rows = []

for file in input_files:
    df = pd.read_csv(f"data/raw/{file}")

    text = " ".join(df["text"].astype(str)).lower().split()
    total_words = len(text)

    for category, keywords in RISK_KEYWORDS.items():
        risk_words = sum(text.count(k) for k in keywords)
        risk_pct = round((risk_words / total_words) * 100, 2) if total_words else 0

        rows.append({
            "date": datetime.utcnow().date().isoformat(),
            "category": category,
            "total_words": total_words,
            "risk_words": risk_words,
            "risk_percentage": risk_pct,
            "severity": severity_label(risk_pct)
        })

out_df = pd.DataFrame(rows)
out_df.to_csv(f"data/evaluated/evaluated_{datetime.utcnow().date()}.csv", index=False)

print("Safety evaluation complete")
