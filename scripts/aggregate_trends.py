import pandas as pd
import glob
import os

files = glob.glob("data/evaluated/*.csv")
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

df["date"] = pd.to_datetime(df["date"])

weekly = df.groupby(
    [pd.Grouper(key="date", freq="W"), "category"]
).risk_score.sum().reset_index()

monthly = df.groupby(
    [pd.Grouper(key="date", freq="M"), "category"]
).risk_score.sum().reset_index()

os.makedirs("data/history/weekly", exist_ok=True)
os.makedirs("data/history/monthly", exist_ok=True)

weekly.to_csv("data/history/weekly/weekly_trends.csv", index=False)
monthly.to_csv("data/history/monthly/monthly_trends.csv", index=False)

print("[OK] Weekly & Monthly trends computed")
