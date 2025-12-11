# Google Trends Collector (DriftMonitor)

This module collects Google Trends data using `pytrends` when available and falls back to a bundled sample dataset otherwise.

## Purpose
- Produce small, reproducible trend snapshots for a list of keywords.
- Designed to run in GitHub Actions (no secrets required).
- Output is written to `data/live/raw/google_trends_<timestamp>.json`.

## Quick usage (local)
```bash
# from repository root
python -m driftmonitor.collectors.google_trends.cli --keywords "ai safety" "llm safety" --output-dir data/live/raw
