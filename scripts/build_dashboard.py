import pandas as pd
import os
from datetime import datetime

OUTPUT_DIR = "docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_csv(path):
    return pd.read_csv(path) if os.path.exists(path) else None

def severity_label(p):
    if p > 5:
        return "HIGH"
    elif p >= 1:
        return "MEDIUM"
    return "LOW"

def severity_badge(label):
    colors = {
        "LOW": "🟢 LOW",
        "MEDIUM": "🟡 MEDIUM",
        "HIGH": "🔴 HIGH"
    }
    return colors[label]

def prepare(df):
    df["risk_percentage"] = ((df["risk_words"] / df["total_words"]) * 100).round(2)
    df["severity"] = df["risk_percentage"].apply(severity_label)
    df["severity"] = df["severity"].apply(severity_badge)
    return df

daily = load_csv("data/history/daily/daily_summary.csv")
weekly = load_csv("data/history/weekly/weekly_summary.csv")
monthly = load_csv("data/history/monthly/monthly_summary.csv")
quarterly = load_csv("data/history/quarterly/quarterly_summary.csv")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI Drift Monitor</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    background: #f6f8fa;
}}
h1 {{
    margin-bottom: 5px;
}}
.status {{
    font-weight: bold;
    margin-bottom: 30px;
}}
.container {{
    display: grid;
    grid-template-columns: 3fr 1fr;
    gap: 30px;
}}
.card {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th {{
    background: #2f363d;
    color: white;
    padding: 10px;
    text-align: left;
}}
td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}
.badge {{
    font-weight: bold;
}}
.guide {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    position: sticky;
    top: 20px;
}}
.footer {{
    margin-top: 40px;
    color: #555;
    font-size: 14px;
}}
</style>
</head>

<body>

<h1>AI Drift Monitor</h1>
<div class="status">Status: Automated monitoring active</div>

<div class="container">

<div>
"""

def section(title, df):
    if df is None or df.empty:
        return f"<div class='card'><h2>{title}</h2><p>No data available yet.</p></div>"

    df = prepare(df)
    rows = ""
    for _, r in df.iterrows():
        rows += f"""
        <tr>
            <td>{r['date']}</td>
            <td>{r['category']}</td>
            <td>{r['total_words']}</td>
            <td>{r['risk_words']}</td>
            <td>{r['risk_percentage']}%</td>
            <td class="badge">{r['severity']}</td>
        </tr>
        """

    return f"""
    <div class="card">
    <h2>{title}</h2>
    <table>
        <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Total Words</th>
            <th>Risk Words</th>
            <th>Risk %</th>
            <th>Severity</th>
        </tr>
        {rows}
    </table>
    </div>
    """

html += section("Daily AI Risk Summary", daily)
html += section("Weekly AI Risk Summary", weekly)
html += section("Monthly AI Risk Summary", monthly)
html += section("Quarterly AI Risk Summary", quarterly)

html += """
</div>

<div class="guide">
<h2>Severity Guide</h2>
<p>🟢 <b>LOW</b><br>&lt; 1% risk words<br>Minimal AI risk</p>
<p>🟡 <b>MEDIUM</b><br>1–5% risk words<br>Moderate AI risk</p>
<p>🔴 <b>HIGH</b><br>&gt; 5% risk words<br>Elevated AI risk</p>
</div>

</div>

<div class="footer">
Last updated (UTC): """ + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + """<br>
Sources: Google Trends, Hacker News<br>
Pipeline: GitHub Actions (Automated)
</div>

</body>
</html>
"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard built successfully")
