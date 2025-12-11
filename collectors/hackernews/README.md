# HackerNews Collector (DriftMonitor)

This module fetches top stories from Hacker News using the public Firebase API and writes a compact JSON snapshot.

## Key features
- No API keys required.
- Lightweight: fetches a limited number of top stories (configurable).
- Bundled sample fallback ensures reproducible output in GitHub Actions.
- Outputs timestamped JSON files under `data/live/raw`.

## Quick usage
```bash
python -m driftmonitor.collectors.hackernews.cli --fetch-top-n 50 --output-dir data/live/raw
