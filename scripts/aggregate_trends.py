import pandas as pd
import os

BASE = "data/history"
daily = pd.read_csv(f"{BASE}/daily/daily_trends.csv")
daily["date"] = pd.to_datetime(daily["date"])

def build(freq, folder, name):
    df = (
        daily.groupby([pd.Grouper(key="date", freq=freq), "category"])
        .agg({
            "total_words": "sum",
            "risk_words": "sum",
            "risk_percentage": "mean"
        })
        .reset_index()
    )

    df["severity"] = df["risk_percentage"].apply(
        lambda p: "🟢 LOW" if p < 1 else "🟡 MEDIUM" if p <= 5 else "🔴 HIGH"
    )

    df["trend"] = "➖"

    os.makedirs(f"{BASE}/{folder}", exist_ok=True)
    df.to_csv(f"{BASE}/{folder}/{name}.csv", index=False)

build("W", "weekly", "weekly_trends")
build("M", "monthly", "monthly_trends")
build("Q", "quarterly", "quarterly_trends")
