import pandas as pd
import glob
import os
from datetime import datetime

# ==============================
# Risk keyword definitions
# ==============================
RISK_KEYWORDS = {
    "AI safety": ["alignment", "safety", "hallucination", "robust"],
    "AI bias": ["bias", "fairness", "discrimination"],
    "AI misuse": ["misuse", "weapon", "abuse", "fraud"],
    "AI regulation": ["regulation", "law", "policy", "governance"]
}

RAW_PATH = "data/raw/*.csv"
OUTPUT_DIR = "data/evaluated"

files = glob.glob(RAW_PATH)

if not files:
    print("No raw data files found.")
    exit(0)

records = []

for file in files:
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        text = " ".join(map(str, row.values)).lower()
        total_words = len(text.split())

        for category, keywords in RISK_KEYWORDS.items():
            risk_count = sum(text.count(word) for word in keywords)

            records.append({
                "date": datetime.utcnow().date(),
                "category": category,
                "total_words": total_words,
                "risk_words": risk_count,
                "risk_score": risk_count,  # backward compatibility
                "source": os.path.basename(file)
            })

# ==============================
# Create evaluated dataframe
# ==============================
evaluated_df = pd.DataFrame(records)

if evaluated_df.empty:
    print("No evaluation records created.")
    exit(0)

# ==============================
# Save output
# ==============================
os.makedirs(OUTPUT_DIR, exist_ok=True)

today = datetime.utcnow().strftime("%Y-%m-%d")
output_file = f"{OUTPUT_DIR}/evaluated_{today}.csv"

evaluated_df.to_csv(output_file, index=False)

print(f"Safety evaluation completed: {output_file}")
