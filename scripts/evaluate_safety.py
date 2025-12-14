import pandas as pd
import glob
import os
from datetime import datetime

RISK_KEYWORDS = {
    "AI safety": [
        "alignment", "hallucination", "unsafe", "failure", "risk",
        "security", "leak", "danger", "threat"
    ],
    "AI regulation": [
        "regulation", "law", "policy", "compliance", "ban",
        "governance", "oversight", "rules"
    ],
    "AI bias": [
        "bias", "discrimination", "fairness", "inequality",
        "racism", "gender", "skewed"
    ],
    "AI misuse": [
        "misuse", "weapon", "fraud", "deepfake", "abuse",
        "scam", "malicious"
    ],
}

files = glob.glob("data/raw/*.csv")
records = []

for f in files:
    try:
        df = pd.read_csv(f)
    except:
        continue

    text_col = "text" if "text" in df.columns else df.columns[1]

    for _, row in df.iterrows():
        text = str(row[text_col]).lower()
        total_words = len(text.split())

        for category, words in RISK_KEYWORDS.items():
            risk_hits = sum(text.count(w) for w in words)

            records.append({
                "date": datetime.utcnow().date(),
                "category": category,
                "total_words": total_words,
                "risk_words": risk_hits,
            })

out = pd.DataFrame(records)

out["risk_percentage"] = (
    (out["risk_words"] / out["total_words"].replace(0, 1)) * 100
).round(2)

def severity(p):
    if p < 1:
        return "🟢 LOW"
    elif p <= 5:
        return "🟡 MEDIUM"
    return "🔴 HIGH"

out["severity"] = out["risk_percentage"].apply(severity)

os.makedirs("data/evaluated", exist_ok=True)
today = datetime.utcnow().strftime("%Y-%m-%d")
out.to_csv(f"data/evaluated/evaluated_{today}.csv", index=False)

print("Safety evaluation complete")
