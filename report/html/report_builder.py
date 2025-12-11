#!/usr/bin/env python3
"""
DriftMonitor HTML Report Builder

This script:
- Loads the latest evaluation output from data/live/processed/
- Renders a clean HTML report using Jinja2 template
- Outputs to: report/html/report.html (GitHub Pages can serve this)
"""

import os
import json
import glob
import logging
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "live", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "report", "html")
TEMPLATE_DIR = os.path.join(BASE_DIR, "report", "templates")

logger = logging.getLogger("driftmonitor.report.html.builder")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def load_latest_processed():
    """Return the latest evaluation file."""
    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, "eval_*.json")))
    if not files:
        raise RuntimeError("No processed evaluation files found.")
    return json.load(open(files[-1], "r", encoding="utf-8"))


def render_html():
    """Render final HTML into OUTPUT_DIR/report.html."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = load_latest_processed()
    logger.info("Loaded evaluation: %d items", data.get("n_texts", 0))

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report_template.html")

    html = template.render(
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        n_texts=data.get("n_texts", 0),
        items=data.get("safety_results", []),
    )

    output_path = os.path.join(OUTPUT_DIR, "report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info("Saved HTML report → %s", output_path)
    return output_path


if __name__ == "__main__":
    path = render_html()
    print(f"Report generated → {path}")
