import pandas as pd
from pathlib import Path
from datetime import datetime

OUTPUT = Path("docs/index.html")
OUTPUT.parent.mkdir(exist_ok=True)

SEVERITY_COLORS = {
    "🟢 LOW": "#1b5e20",
    "🟠 MEDIUM": "#e65100",
    "🔴 HIGH": "#b71c1c"
}

def load_table(path):
    if not path.exists():
        return None
    return pd.read_csv(path)

def render_table(df, title):
    if df is None or df.empty:
        return f"<h3>{title}</h3><p>No data available yet.</p>"

    rows = ""
    for _, r in df.iterrows():
        color = SEVERITY_COLORS.get(r["severity"], "#333")
        rows += f"""
        <tr style="border-left:6px solid {color}">
            <td>{r['category']}</td>
            <td>{int(r['total_words'])}</td>
            <td>{int(r['risk_words'])}</td>
            <td>{r['risk_percentage']}%</td>
            <td><strong style="color:{color}">{r['severity']}</strong></td>
        </tr>
        """

    return f"""
    <h3>{title}</h3>
    <table>
        <tr>
            <th>Category</th>
            <th>Total Words</th>
            <th>Risk Words</th>
            <th>Risk %</th>
            <th>Severity</th>
        </tr>
        {rows}
    </table>
    """

daily = load_table(Path("data/history/daily/daily_trends.csv"))
weekly = load_table(Path("data/history/weekly/weekly_trends.csv"))
monthly = load_table(Path("data/history/monthly/monthly_trends.csv"))
quarterly = load_table(Path("data/history/quarterly/quarterly_trends.csv"))

html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AI Drift Monitor</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #0f172a;
    color: #e5e7eb;
    padding: 40px;
}}
h1 {{ color: #f8fafc; }}
h3 {{ margin-top: 40px; }}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    background: #020617;
}}
th {{
    background: #111827;
    padding: 10px;
}}
td {{
    padding: 10px;
    border-bottom: 1px solid #1f2933;
}}
.legend {{
    background:#020617;
    padding:15px;
    border-radius:8px;
    width: fit-content;
}}
</style>
</head>
<body>

<h1>AI Drift Monitor</h1>
<p><strong>Status:</strong> Automated monitoring active</p>

<div class="legend">
<b>Severity Legend</b><br>
🟢 LOW – Normal signal level<br>
🟠 MEDIUM – Elevated attention<br>
🔴 HIGH – Immediate concern
</div>

{render_table(daily, "Daily Risk Summary")}
{render_table(weekly, "Weekly Risk Summary")}
{render_table(monthly, "Monthly Risk Summary")}
{render_table(quarterly, "Quarterly Risk Summary")}

<p style="margin-top:40px;font-size:12px;">
Last updated (UTC): {datetime.utcnow()}<br>
Sources: Google Trends, Hacker News<br>
Pipeline: GitHub Actions (Automated)
</p>

</body>
</html>
"""

OUTPUT.write_text(html, encoding="utf-8")
print("Dashboard built successfully")
