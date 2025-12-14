import pandas as pd
import glob
import os

INPUT = "data/evaluated/*.csv"
OUTPUT_BASE = "data/history"

def severity_label(pct):
    if pct >= 30:
        return "🔴 HIGH"
    elif pct >= 10:
        return "🟠 MEDIUM"
    else:
        return "🟢 LOW"

files = glob.glob(INPUT)
if not files:
    print("No evaluated data found. Skipping aggregation.")
    exit(0)

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

df["date"] = pd.to_datetime(df["date"])
df["total_words"] = 1   # each row = one signal
df["risk_words"] = df["risk_score"]

def aggregate(freq, folder, filename):
    os.makedirs(folder, exist_ok=True)

    agg = (
        df.groupby([pd.Grouper(key="date", freq=freq), "category"])
          .agg(
              total_words=("total_words", "sum"),
              risk_words=("risk_words", "sum")
          )
          .reset_index()
    )

    agg["risk_percentage"] = (
        (agg["risk_words"] / agg["total_words"]) * 100
    ).round(2)

    agg["severity"] = agg["risk_percentage"].apply(severity_label)

    agg.to_csv(os.path.join(folder, filename), index=False)

# Daily / Weekly / Monthly / Quarterly
aggregate("D", f"{OUTPUT_BASE}/daily", "daily_trends.csv")
aggregate("W", f"{OUTPUT_BASE}/weekly", "weekly_trends.csv")
aggregate("M", f"{OUTPUT_BASE}/monthly", "monthly_trends.csv")
aggregate("Q", f"{OUTPUT_BASE}/quarterly", "quarterly_trends.csv")

print("All aggregations complete")
