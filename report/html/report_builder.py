from pathlib import Path
import json
from datetime import datetime
from jinja2 import Template

PROCESSED_DIR = Path("data/live/processed")
DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

records = []

# Read all daily processed data
for day_dir in sorted(PROCESSED_DIR.glob("*")):
    file = day_dir / "safety_eval.json"
    if file.exists():
        daily = json.loads(file.read_text())
        records.extend(daily)

# Summary metrics
total = len(records)
safe = sum(1 for r in records if r["risk_label"] == "SAFE")
warning = sum(1 for r in records if r["risk_label"] == "WARNING")
risky = sum(1 for r in records if r["risk_label"] == "RISKY")
avg_score = round(
    sum(r["safety_score"] for r in records) / total, 2
) if total else 0.0

# HTML Template
template = Template("""
<!DOCTYPE html>
<html>
<head>
<title>DriftMonitor Dashboard</title>
<style>
body {
  font-family: Arial, sans-serif;
  margin: 40px;
  background: #fafafa;
}
h1 { margin-bottom: 5px; }
.subtitle { color: #555; margin-bottom: 30px; }

.cards {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}
.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  flex: 1;
  text-align: center;
}
.card h2 { margin: 0; }

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}
th, td {
  padding: 10px;
  border: 1px solid #ddd;
}
th {
  background: #f0f0f0;
}
.safe { color: green; font-weight: bold; }
.warning { color: orange; font-weight: bold; }
.risky { color: red; font-weight: bold; }

footer {
  margin-top: 40px;
  color: #777;
  font-size: 14px;
}
</style>
</head>

<body>

<h1>DriftMonitor</h1>
<div class="subtitle">
Daily, Weekly, Monthly AI Safety Monitoring<br>
Last updated: {{ updated }}
</div>

<div class="cards">
  <div class="card"><h2>{{ total }}</h2>Total Items</div>
  <div class="card"><h2>{{ safe }}</h2>SAFE</div>
  <div class="card"><h2>{{ warning }}</h2>WARNING</div>
  <div class="card"><h2>{{ risky }}</h2>RISKY</div>
  <div class="card"><h2>{{ avg_score }}</h2>Avg Safety</div>
</div>

<h2>Latest Safety Evaluations</h2>

<table>
<tr>
  <th>Date</th>
  <th>Source</th>
  <th>Title</th>
  <th>Safety Score</th>
  <th>Risk</th>
</tr>
{% for r in records %}
<tr>
  <td>{{ r.date }}</td>
  <td>{{ r.source }}</td>
  <td>{{ r.title }}</td>
  <td>{{ "%.2f"|format(r.safety_score) }}</td>
  <td class="{{ r.risk_label|lower }}">{{ r.risk_label }}</td>
</tr>
{% endfor %}
</table>

<footer>
Auto-updated via GitHub Actions · 
<a href="https://github.com/Vineeth2002/driftmonitor">GitHub Repo</a>
</footer>

</body>
</html>
""")

html = template.render(
    records=records,
    total=total,
    safe=safe,
    warning=warning,
    risky=risky,
    avg_score=avg_score,
    updated=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
)

(DOCS_DIR / "index.html").write_text(html)
print("✅ Dashboard built at docs/index.html")
