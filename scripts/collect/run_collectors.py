import json
from pathlib import Path
from datetime import datetime, timezone

from driftmonitor.collectors.google_trends.collector import collect_google_trends
from driftmonitor.collectors.hackernews.collector import collect_hackernews

RAW_BASE = Path("data/live/raw")


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = RAW_BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)

    google_data = collect_google_trends()
    hn_data = collect_hackernews()

    (out_dir / "google_trends.json").write_text(
        json.dumps(google_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    (out_dir / "hackernews.json").write_text(
        json.dumps(hn_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] Collected data for {today}")
    print(f"Saved to: {out_dir}")


if __name__ == "__main__":
    main()
