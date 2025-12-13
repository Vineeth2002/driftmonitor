import json
from pathlib import Path
from datetime import datetime

BASE = Path("data/live/processed")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

STYLE_PATH = "assets/style.css"


def load_latest_daily():
    days = sorted(d.name for d in BASE.iterdir() if d.is_dir() and d.name[:4].isdigit())
    if not days:
        return None, None
    latest = days[-1]
    f = BASE / latest / "evaluated.json"
    if not f.exists():
        return None, None
    return latest, json.loads(f.read_text(encoding="utf-8"))


def load_latest_weekly():
    fdir = BASE / "weekly"
    if not fdir.exists():
        return None
    files = sorted(fdir.glob("weekly_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def load_latest_monthly():
    fdir = BASE / "monthly"
    if not fdir.exists():
        return None
    files = sorted(fdir.glob("monthly_*.json"))
    return json.loads(files[-1].read_text()) if files else None


def main():
    today, daily = load_latest_daily()
    weekly = load_latest_weekly()
    monthly = load_latest_monthly()

    if not daily:
        DOCS.joinpath("index.html").write_text(
            "<h2>No data available yet</h2>",
            encoding="utf-8",
        )
        return

    items = daily["items"]

    def count(label):
        return sum(1 for i in items if i["risk_label"] == label)

    safe = count("SAFE")
    warning = count("WARNING")
    risky = count("RISKY")

    rows = ""
    for i in items[:50]:
        rows += f"""
        <tr>
            <td>{i.get("source","")}</td>
            <td>{i.get("risk_label")}</td>
            <td>{i.get("safety_score")}</td>
            <td>{i.get("reason")}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DriftMonitor Dashboard</title>
    <link rel="stylesheet" href="{STYLE_PATH}">
</head>
<body>
<div class="container">
<h1>DriftMonitor</h1>
<p class="timestamp">Last updated: {today}</p>

<div class="summary">
    <p>Total items: <b>{daily["total"]}</b></p>
    <p class="safe">SAFE: {safe}</p>
    <p class="warning">WARNING: {warning}</p>
    <p class="risky">RISKY: {risky}</p>
</div>

<h2>Latest Evaluated Items</h2>
<table>
<tr>
    <th>Source</th>
    <th>Risk</th>
    <th>Score</th>
    <th>Reason</th>
</tr>
{rows}
</table>

{f"<h2>Weekly Summary</h2><pre>{json.dumps(weekly, indent=2)}</pre>" if weekly else ""}
{f"<h2>Monthly Summary</h2><pre>{json.dumps(monthly, indent=2)}</pre>" if monthly else ""}

<p class="footer">DriftMonitor · AI Safety & Drift Monitoring</p>
</div>
</body>
</html>
"""

    DOCS.joinpath("index.html").write_text(html, encoding="utf-8")
    print("[OK] Dashboard built → docs/index.html")


if __name__ == "__main__":
    main()
