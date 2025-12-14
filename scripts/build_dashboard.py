import pandas as pd
import os

output_path = "docs/index.html"
daily_path = "data/history/daily/daily_trends.csv"

html = """
<!DOCTYPE html>
<html>
<head>
  <title>Drift Monitor</title>
</head>
<body>
<h1>Drift Monitor</h1>
"""

if not os.path.exists(daily_path):
    html += "<p>Status: No trend data available yet.</p>"
    html += "<p>Automation is running correctly.</p>"
else:
    df = pd.read_csv(daily_path)

    if df.empty:
        html += "<p>Status: No trend data available yet.</p>"
    else:
        latest = df.iloc[-1]
        html += f"""
        <h2>Daily AI Risk Signal</h2>
        <p><b>Date:</b> {latest['date']}</p>
        <p><b>Total Risk Score:</b> {latest['risk_score']}</p>

        <h3>Daily History</h3>
        <table border="1" cellpadding="6">
        <tr><th>Date</th><th>Risk Score</th></tr>
        """

        for _, row in df.iterrows():
            html += f"<tr><td>{row['date']}</td><td>{row['risk_score']}</td></tr>"

        html += "</table>"

html += "</body></html>"

os.makedirs("docs", exist_ok=True)
with open(output_path, "w") as f:
    f.write(html)

print("Dashboard built successfully")
