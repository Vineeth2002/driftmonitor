import pandas as pd
import plotly.express as px
import os

path = "data/history/weekly/weekly_trends.csv"

os.makedirs("docs", exist_ok=True)

if not os.path.exists(path):
    with open("docs/index.html", "w") as f:
        f.write("<h2>No data yet. Pipeline running.</h2>")
    exit()

df = pd.read_csv(path)

fig = px.line(
    df,
    x="date",
    y="risk_score",
    color="category",
    title="AI Safety Risk Drift (Weekly)",
    markers=True
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Week",
    yaxis_title="Risk Score",
    legend_title="Risk Category",
    height=600
)

fig.write_html("docs/index.html")

print("Dashboard built")
