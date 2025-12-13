import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Try pytrends, fallback safely
try:
    from pytrends.request import TrendReq
except Exception:
    TrendReq = None


DEFAULT_KEYWORDS = [
    "ai safety",
    "llm jailbreak",
    "prompt injection",
    "ai misuse",
]


def collect_google_trends(keywords=None):
    """
    Collect Google Trends data.
    Always returns a deterministic structure.
    """
    keywords = keywords or DEFAULT_KEYWORDS
    collected_at = datetime.utcnow().isoformat() + "Z"

    # ---- Fallback mode (GitHub Actions safe) ----
    if TrendReq is None:
        logger.warning("pytrends not available, using fallback data")
        return {
            "source": "google_trends",
            "collected_at": collected_at,
            "results": [
                {
                    "keyword": kw,
                    "text": f"Trend keyword: {kw}",
                    "interest": 0,
                }
                for kw in keywords
            ],
        }

    # ---- Real collection ----
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload(keywords, timeframe="now 1-d")
        df = pytrends.interest_over_time()

        results = []
        for kw in keywords:
            if kw in df:
                val = int(df[kw].iloc[-1])
                results.append(
                    {
                        "keyword": kw,
                        "text": f"Trend keyword: {kw}",
                        "interest": val,
                    }
                )

        return {
            "source": "google_trends",
            "collected_at": collected_at,
            "results": results,
        }

    except Exception as exc:
        logger.exception("Google Trends failed, fallback used: %s", exc)
        return {
            "source": "google_trends",
            "collected_at": collected_at,
            "results": [
                {
                    "keyword": kw,
                    "text": f"Trend keyword: {kw}",
                    "interest": 0,
                }
                for kw in keywords
            ],
        }
