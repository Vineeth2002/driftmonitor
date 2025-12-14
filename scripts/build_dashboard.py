import pandas as pd
import plotly.express as px
from datetime import datetime, timezone, timedelta
import os

# Paths
DAILY_PATH = "data/history/daily/daily_trends.csv"
EVAL_PATH = "data/evaluated"
OUTPUT_PATH = "docs/index.html"

os.makedirs("docs", exist_ok=True)

# ---------- Time ----------
ist = timezone(timedelta(hours=5, minutes=30))
last_updated = datetime.now(ist).strftime("%Y-%m-%d %H:%M IST")

# ---------- Load Daily Trends ----------
if not os.path.exists(DAILY_PATH):
    with open(OUTPUT_PATH, "w") as f:
        f.write("<h1>Drift Monitor</h1><p>No data yet.</p>")
    exit(0)

daily = pd.read_csv(DAILY_PATH)
daily["date"] = pd.to_datetime(daily["date"])

today_score = int(daily.iloc[-1]["risk_score"])
yesterday_score = int(daily.iloc[-2]["risk_score"]) if len(daily) > 1 else 0
delta = today_score - yesterday_score

# ---------- Load Evaluated Data ----------
eval_files = sorted(
    [os.path.join(EVAL_PATH, f) for f in os.listdir(EVAL_PATH) if f.endswith(".csv")]
)

eval_df = pd.concat([pd.read_csv(f) for f in eval_files], ignore_index=True)

# Source contribution
source_counts = eval_df.groupby("source").risk_score.sum().reset_index()

# Category breakdown
category_counts = (
    eval_df.assign(category=eval_df["categories"].str.split(","))
    .explode("category")
    .groupby("category")
    .risk_score.sum()
    .reset_index()
)

# ---------- Charts ----------
trend_fig = px.line(
    daily,
    x="date",
    y="risk_score",
    title="Daily AI Risk Trend",
    markers=True
)

source_fig = px.bar(
    source_counts,
    x="source",
    y="risk_score",
    title="Risk Contribution by Source"
)

category_fig = px.bar(
    category_counts,
    x="category",
    y="risk_score",
    title="Risk Contribution by Category"
)

# ---------- Build HTML ----------
html = f"""
<html>
<head>
  <title>Drift Monitor</title>
</head>
<body>

<h1>Drift Monitor – AI Safety Risk Dashboard</h1>
<p><b>Last updated:</b> {last_updated}</p>

<hr>

<h2>Key Metrics</h2>
<ul>
  <li><b>Today’s Risk Score:</b> {today_score}</li>
  <li><b>Yesterday’s Risk Score:</b> {yesterday_score}</li>
  <li><b>24h Change:</b> {delta:+}</li>
  <li><b>Total Signals Processed:</b> {len(eval_df)}</li>
</ul>

<hr>

{trend_fig.to_html(include_plotlyjs='cdn', full_html=False)}

<hr>

{source_fig.to_html(include_plotlyjs=False, full_html=False)}

<hr>

{category_fig.to_html(include_plotlyjs=False, full_html=False)}

</body>
</html>
"""

with open(OUTPUT_PATH, "w") as f:
    f.write(html)

print("Informative dashboard built successfully")
