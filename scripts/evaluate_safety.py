import pandas as pd
import glob
import os
import re
from datetime import datetime

RISK_KEYWORDS = {
    "AI safety": [
        "safety","unsafe","alignment","hallucination",
        "robust","risk","failure","guardrail"
    ],
    "AI regulation": [
        "law","policy","regulation","ban",
        "compliance","governance","oversight"
    ],
    "AI bias": [
        "bias","biased","fairness","unfair",
        "discrimination","inequality","ethical"
    ],
    "AI misuse": [
        "misuse","abuse","fraud","scam",
        "deepfake","weapon","harm","manipulation"
    ]
}

records = []

for file in glob.glob("data/raw/*.csv"):
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        text = re.sub(r"[^a-z ]", " ", " ".join(map(str, row.values)).lower())
        words = text.split()
        total_words = len(words)

        if total_words == 0:
            continue

        for category, keys in RISK_KEYWORDS.items():
            risk_words = sum(words.count(k) for k in keys)

            if risk_words == 0 and total_words > 40:
                risk_words = 1

            risk_pct = round((risk_words / total_words) * 100, 2)

            if risk_pct < 1:
                severity = "🟢 LOW"
            elif risk_pct <= 5:
                severity = "🟡 MEDIUM"
            else:
                severity = "🔴 HIGH"

            records.append({
                "date": datetime.utcnow().date(),
                "category": category,
                "total_words": total_words,
                "risk_words": risk_words,
                "risk_percentage": risk_pct,
                "severity": severity
            })

os.makedirs("data/evaluated", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")
pd.DataFrame(records).to_csv(
    f"data/evaluated/evaluated_{today}.csv", index=False
)

print("Safety evaluation complete")
