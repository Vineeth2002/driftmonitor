import pandas as pd
import glob
import os

# -------------------------------------------------
# Load evaluated data
# -------------------------------------------------
files = glob.glob("data/evaluated/*.csv")

if not files:
    print("No evaluated files found. Skipping aggregation.")
    exit(0)

frames = []
for f in files:
    df = pd.read_csv(f)
    if not df.empty:
        frames.append(df)

if not frames:
    print("Evaluated files exist but all are empty. Skipping aggregation.")
    exit(0)

df = pd.concat(frames, ignore_index=True)

# Ensure date is datetime
df["date"] = pd.to_datetime(df["date"])

# -------------------------------------------------
# Create output directories
# -------------------------------------------------
os.makedirs("data/history/daily", exist_ok=True)
os.makedirs("data/history/weekly", exist_ok=True)
os.makedirs("data/history/monthly", exist_ok=True)
os.makedirs("data/history/quarterly", exist_ok=True)

# -------------------------------------------------
# DAILY aggregation
# -------------------------------------------------
daily = (
    df.groupby([pd.Grouper(key="date", freq="D"), "category"])
      .risk_score.sum()
      .reset_index()
)

daily.to_csv(
    "data/history/daily/daily_trends.csv",
    index=False
)

# -------------------------------------------------
# WEEKLY aggregation
# -------------------------------------------------
weekly = (
    df.groupby([pd.Grouper(key="date", freq="W"), "category"])
      .risk_score.sum()
      .reset_index()
)

weekly.to_csv(
    "data/history/weekly/weekly_trends.csv",
    index=False
)

# -------------------------------------------------
# MONTHLY aggregation
# -------------------------------------------------
monthly = (
    df.groupby([pd.Grouper(key="date", freq="M"), "category"])
      .risk_score.sum()
      .reset_index()
)

monthly.to_csv(
    "data/history/monthly/monthly_trends.csv",
    index=False
)

# -------------------------------------------------
# QUARTERLY aggregation
# -------------------------------------------------
quarterly = (
    df.groupby([pd.Grouper(key="date", freq="Q"), "category"])
      .risk_score.sum()
      .reset_index()
)

quarterly.to_csv(
    "data/history/quarterly/quarterly_trends.csv",
    index=False
)

print("Daily, weekly, monthly, and quarterly aggregation completed successfully")
