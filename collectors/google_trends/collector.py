from pytrends.request import TrendReq
from datetime import datetime, timezone

def collect_google_trends(limit=10):
    pytrends = TrendReq(hl="en-US", tz=0)

    pytrends.trending_searches(pn="united_states")
    df = pytrends.trending_searches(pn="united_states")

    results = []
    ts = datetime.now(timezone.utc).isoformat()

    for i, row in df.head(limit).iterrows():
        results.append({
            "id": f"google:{i}",
            "source": "google_trends",
            "title": row[0],
            "text": row[0],
            "collected_at": ts,
            "url": None,
            "metadata": {}
        })

    return {"results": results}
