import pandas as pd
import glob
import os

# Load evaluated safety data
files = glob.glob("data/evaluated/*.csv")
if not files:
    print("No evaluated data found for daily aggregation.")
    exit(0)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

# Ensure datetime
df["date"] = pd.to_datetime(df["date"]).dt.date

# Each row represents one text unit (proxy for now)
df["total_words"] = 1
df["risk_words"] = df["risk_score"]

# Aggregate daily per category
daily = (
    df.groupby(["date", "category"])
      .agg(
          total_words=("total_words", "sum"),
          risk_words=("risk_words", "sum")
      )
      .reset_index()
)

# Calculate risk percentage
daily["risk_percentage"] = (daily["risk_words"] / daily["total_words"]) * 100

# Severity logic
def severity(p):
    if p < 1:
        return "LOW"
    elif p <= 5:
        return "MEDIUM"
    else:
        return "HIGH"

daily["severity"] = daily["risk_percentage"].apply(severity)

# Ensure output directory
os.makedirs("data/history/daily", exist_ok=True)

# Save
daily.to_csv("data/history/daily/daily_summary.csv", index=False)

print("Daily aggregation completed successfully.")
