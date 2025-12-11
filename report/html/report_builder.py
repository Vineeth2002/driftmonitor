
#!/usr/bin/env python3
"""
DriftMonitor HTML Report Builder (enhanced summary display)

- Loads latest evaluation (eval_*.json)
- Loads latest evaluation summary (eval_summary_*.json) if present
- Loads latest drift summary (drift_summary_*.json) if present
- Renders template with summary counts and risky examples
"""

import os
@@ -25,7 +25,6 @@


def load_latest_json_by_pattern(dirpath: str, pattern: str):

    files = sorted(glob.glob(os.path.join(dirpath, pattern)))
    if not files:
        return None
@@ -35,57 +34,38 @@
            data = json.load(fh)
        data["_source_file"] = os.path.basename(path)
        return data
    except Exception:

        return None

def render_html():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    eval_data = load_latest_json_by_pattern(PROCESSED_DIR, "eval_*.json")
    eval_summary = load_latest_json_by_pattern(PROCESSED_DIR, "eval_summary_*.json")
    drift = load_latest_json_by_pattern(PROCESSED_DIR, "drift_summary_*.json")

    if eval_data is None:
        raise RuntimeError("No evaluation data found to build report.")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report_template.html")

    html = template.render(
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        eval=eval_data,
        summary=eval_summary,
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
