import pandas as pd
import plotly.express as px
from datetime import datetime, timezone, timedelta
import os

# ---------------- Paths ----------------
DAILY_PATH = "data/history/daily/daily_trends.csv"
EVAL_PATH = "data/evaluated"
OUTPUT_PATH = "docs/index.html"

os.makedirs("docs", exist_ok=True)

# ---------------- Time (IST) ----------------
ist = timezone(timedelta(hours=5, minutes=30))
last_updated = datetime.now(ist).strftime("%d %b %Y, %I:%M %p IST")

# ---------------- Load data ----------------
if not os.path.exists(DAILY_PATH):
    with open(OUTPUT_PATH, "w") as f:
        f.write("<h1>Drift Monitor</h1><p>No data yet.</p>")
    exit(0)

daily = pd.read_csv(DAILY_PATH)
daily["date"] = pd.to_datetime(daily["date"])

today_score = int(daily.iloc[-1]["risk_score"])
yesterday_score = int(daily.iloc[-2]["risk_score"]) if len(daily) > 1 else 0
delta = today_score - yesterday_score

# Evaluated data
eval_files = sorted(
    [os.path.join(EVAL_PATH, f) for f in os.listdir(EVAL_PATH) if f.endswith(".csv")]
)
eval_df = pd.concat([pd.read_csv(f) for f in eval_files], ignore_index=True)

# ---------------- Charts ----------------
trend_fig = px.line(
    daily,
    x="date",
    y="risk_score",
    markers=True,
    title="Daily AI Safety Risk Trend"
)
trend_fig.update_layout(margin=dict(l=30, r=30, t=60, b=30))

source_fig = px.bar(
    eval_df.groupby("source").risk_score.sum().reset_index(),
    x="source",
    y="risk_score",
    title="Risk Contribution by Source"
)

category_fig = px.bar(
    eval_df.assign(category=eval_df["categories"].str.split(","))
          .explode("category")
          .groupby("category")
          .risk_score.sum()
          .reset_index(),
    x="category",
    y="risk_score",
    title="Risk Contribution by Category"
)

# ---------------- HTML (Styled) ----------------
html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Drift Monitor</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
    background: #f4f6f9;
    margin: 0;
    color: #1f2937;
}}

.header {{
    background: #0f172a;
    color: white;
    padding: 24px 40px;
}}

.container {{
    padding: 30px 40px;
}}

.kpis {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}}

.card h3 {{
    margin: 0;
    font-size: 14px;
    color: #6b7280;
}}

.card .value {{
    font-size: 34px;
    font-weight: 700;
    margin-top: 8px;
}}

.delta-positive {{ color: #16a34a; }}
.delta-negative {{ color: #dc2626; }}

.panel {{
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}}

.footer {{
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    padding: 20px;
}}
</style>
</head>

<body>

<div class="header">
    <h1>Drift Monitor</h1>
    <p>Automated AI Safety Risk Intelligence</p>
</div>

<div class="container">

<div class="kpis">
    <div class="card">
        <h3>Today’s Risk Score</h3>
        <div class="value">{today_score}</div>
    </div>

    <div class="card">
        <h3>24h Change</h3>
        <div class="value {'delta-positive' if delta >= 0 else 'delta-negative'}">
            {delta:+}
        </div>
    </div>

    <div class="card">
        <h3>Total Signals Processed</h3>
        <div class="value">{len(eval_df)}</div>
    </div>

    <div class="card">
        <h3>Last Updated</h3>
        <div class="value" style="font-size:18px;">{last_updated}</div>
    </div>
</div>

<div class="panel">
{trend_fig.to_html(include_plotlyjs='cdn', full_html=False)}
</div>

<div class="panel">
{source_fig.to_html(include_plotlyjs=False, full_html=False)}
</div>

<div class="panel">
{category_fig.to_html(include_plotlyjs=False, full_html=False)}
</div>

</div>

<div class="footer">
Drift Monitor · Fully automated · GitHub-native · No manual intervention
</div>

</body>
</html>
"""

with open(OUTPUT_PATH, "w") as f:
    f.write(html)

print("High-quality dashboard generated")
