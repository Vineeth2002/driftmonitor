import pandas as pd
import os
from datetime import datetime

DOCS_DIR = "docs"
DATA_DIR = "data"

os.makedirs(DOCS_DIR, exist_ok=True)

html = []
html.append("<html><head>")
html.append("<title>Drift Monitor</title>")
html.append("""
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    padding: 20px;
}
h1, h2 {
    color: #222;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 30px;
    background-color: white;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
}
th {
    background-color: #343a40;
    color: white;
}
tr:nth-child(even) {
    background-color: #f2f2f2;
}
.footer {
    margin-top: 40px;
    font-size: 12px;
    color: #666;
}
</style>
""")
html.append("</head><body>")

html.append("<h1>AI Drift Monitor</h1>")
html.append("<p><b>Status:</b> Automated monitoring active</p>")

# -------------------------
# 1. Latest evaluation
# -------------------------
html.append("<h2>Latest AI Safety Signals</h2>")

evaluated_files = sorted(
    [f for f in os.listdir("data/evaluated") if f.endswith(".csv")],
    reverse=True
)

if evaluated_files:
    df_latest = pd.read_csv(f"data/evaluated/{evaluated_files[0]}")
    if df_latest.empty:
        html.append("<p>No risk signals detected in latest run.</p>")
    else:
        html.append(df_latest.to_html(index=False))
else:
    html.append("<p>No evaluation data available yet.</p>")

# -------------------------
# 2. Weekly trends
# -------------------------
html.append("<h2>Weekly Risk Trends</h2>")
weekly_path = "data/history/weekly/weekly_trends.csv"

if os.path.exists(weekly_path):
    df_weekly = pd.read_csv(weekly_path)
    html.append(df_weekly.to_html(index=False))
else:
    html.append("<p>Weekly aggregation not available yet.</p>")

# -------------------------
# 3. Monthly trends
# -------------------------
html.append("<h2>Monthly Risk Trends</h2>")
monthly_path = "data/history/monthly/monthly_trends.csv"

if os.path.exists(monthly_path):
    df_monthly = pd.read_csv(monthly_path)
    html.append(df_monthly.to_html(index=False))
else:
    html.append("<p>Monthly aggregation not available yet.</p>")

# -------------------------
# Footer
# -------------------------
html.append("<div class='footer'>")
html.append(f"Last updated (UTC): {datetime.utcnow()}<br>")
html.append("Sources: Google Trends, Hacker News<br>")
html.append("Pipeline: GitHub Actions (Automated)")
html.append("</div>")

html.append("</body></html>")

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html))

print("Dashboard built successfully")
