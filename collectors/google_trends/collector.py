"""
Google Trends collector (safe fallback version).

This is intentionally lightweight and CI-safe.
"""

def collect_google_trends():
    """
    Collect Google Trends data.
    Fallback implementation for CI / demo.
    """
    return {
        "source": "google_trends",
        "results": [
            {
                "text": "AI safety interest is increasing globally",
                "meta": {
                    "keyword": "ai safety",
                    "timeframe": "now 7-d"
                }
            }
        ]
    }
