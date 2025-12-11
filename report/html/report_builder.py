#!/usr/bin/env python3
"""
DriftMonitor HTML Report Builder (updated)

- Loads the latest evaluation output from data/live/processed/
- Loads the latest drift summary (if present) from data/live/processed/
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


def load_latest_json_by_pattern(dirpath: str, pattern: str):
    """Return loaded JSON object for the latest file matching pattern, or None."""
    files = sorted(glob.glob(os.path.join(dirpath, pattern)))
    if not files:
        return None
    path = files[-1]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data["_source_file"] = os.path.basename(path)
        return data
    except Exception as exc:
        logger.exception("Failed to load JSON %s: %s", path, exc)
        return None


def load_latest_processed():
    """Return the latest evaluation file (eval_*.json) or raise if none found."""
    data = load_latest_json_by_pattern(PROCESSED_DIR, "eval_*.json")
    if data is None:
        raise RuntimeError("No processed evaluation files found in %s." % PROCESSED_DIR)
    return data


def load_latest_drift_summary():
    """Return the latest drift_summary_*.json if available, otherwise None."""
    return load_latest_json_by_pattern(PROCESSED_DIR, "drift_summary_*.json")


def render_html():
    """Render final HTML into OUTPUT_DIR/report.html."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load main evaluation
    eval_data = load_latest_processed()
    logger.info("Loaded evaluation: %d items from %s", eval_data.get("n_texts", 0), eval_data.get("_source_file"))

    # Load drift summary if present
    drift = load_latest_drift_summary()
    if drift:
        logger.info("Loaded drift summary from %s", drift.get("_source_file", "unknown"))
    else:
        logger.info("No drift summary found (continuing without it).")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report_template.html")

    html = template.render(
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        n_texts=eval_data.get("n_texts", 0),
        items=eval_data.get("safety_results", []),
        drift_summary=drift,
    )

    output_path = os.path.join(OUTPUT_DIR, "report.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info("Saved HTML report → %s", output_path)
    return output_path


if __name__ == "__main__":
    path = render_html()
    print(f"Report generated → {path}")
