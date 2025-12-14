import pandas as pd
import os

df = pd.read_csv("data/history/daily/daily_trends.csv")
df["date"] = pd.to_datetime(df["date"])

BASE = "data/history"

def agg(freq, name):
    out = (
        df.groupby([pd.Grouper(key="date", freq=freq),"category"])
          .agg(
              total_words=("total_words","sum"),
              risk_words=("risk_words","sum"),
              risk_percentage=("risk_percentage","mean")
          )
          .reset_index()
    )

    out = out.sort_values(["category","date"])
    out["prev"] = out.groupby("category")["risk_percentage"].shift(1)

    def trend(r):
        if pd.isna(r["prev"]): return "NEW"
        if r["risk_percentage"] > r["prev"]: return "UP"
        if r["risk_percentage"] < r["prev"]: return "DOWN"
        return "STABLE"

    out["trend"] = out.apply(trend, axis=1)
    out.drop(columns=["prev"], inplace=True)

    os.makedirs(f"{BASE}/{name}", exist_ok=True)
    out.to_csv(f"{BASE}/{name}/{name}_trends.csv", index=False)

agg("W","weekly")
agg("M","monthly")
agg("Q","quarterly")

print("Trend aggregation complete")
