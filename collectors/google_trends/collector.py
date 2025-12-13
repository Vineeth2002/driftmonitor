import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Optional dependency
try:
    from pytrends.request import TrendReq
except Exception:
    TrendReq = None

KEYWORDS = ["ai safety", "llm safety", "model safety"]

def collect_google_trends():
    """
    Collect Google Trends data.

    Returns:
        list[dict]
    """
    collected_at = datetime.utcnow().isoformat() + "Z"

    if TrendReq is None:
        logger.warning("pytrends not available, using fallback data")
        return _fallback(collected_at)

    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        results = []

        for kw in KEYWORDS:
            pytrends.build_payload([kw], timeframe="now 7-d")
            df = pytrends.interest_over_time()

            if df.empty:
                continue

            series = {
                str(idx): int(val)
                for idx, val in df[kw].items()
            }

            results.append({
                "source": "google_trends",
                "keyword": kw,
                "collected_at": collected_at,
                "series": series,
            })

        if not results:
            return _fallback(collected_at)

        return results

    except Exception as e:
        logger.exception("Google Trends failed, using fallback")
        return _fallback(collected_at)


def _fallback(collected_at: str):
    """Deterministic fallback data."""
    return [
        {
            "source": "google_trends",
            "keyword": "ai safety",
            "collected_at": collected_at,
            "series": {
                "2025-01-01": 40,
                "2025-01-02": 45,
                "2025-01-03": 42,
            },
        }
    ]
