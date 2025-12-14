import pandas as pd
import glob
import os
from datetime import datetime
from pandas.errors import EmptyDataError

RISK_KEYWORDS = {
    "AI safety": ["safety", "alignment", "robust"],
    "AI regulation": ["law", "policy", "regulation", "governance"],
    "AI bias": ["bias", "fairness", "discrimination"],
    "AI misuse": ["misuse", "abuse", "weapon"]
}

raw_files = glob.glob("data/raw/*.csv")
records = []

for file in raw_files:
    try:
        # Skip truly empty files
        if os.path.getsize(file) == 0:
            continue

        df = pd.read_csv(file)

        # Skip files with no usable rows
        if df.empty:
            continue

    except EmptyDataError:
        # Pandas-safe fallback
        continue

    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()
        total_words = len(text.split())

        for category, keywords in RISK_KEYWORDS.items():
            risk_words = sum(text.count(k) for k in keywords)

            if total_words == 0:
                risk_pct = 0.0
            else:
                risk_pct = round((risk_words / total_words) * 100, 2)

            if risk_pct > 5:
                severity = "🔴 HIGH"
            elif risk_pct >= 1:
                severity = "🟡 MEDIUM"
            else:
                severity = "🟢 LOW"

            records.append({
                "date": datetime.utcnow().date(),
                "category": category,
                "total_words": total_words,
                "risk_words": risk_words,
                "risk_percentage": risk_pct,
                "severity": severity
            })

# Always write a file (even if empty)
os.makedirs("data/evaluated", exist_ok=True)
out = pd.DataFrame(records)

today = datetime.utcnow().strftime("%Y-%m-%d")
out.to_csv(f"data/evaluated/evaluated_{today}.csv", index=False)

print(f"Safety evaluation completed for {today}")
