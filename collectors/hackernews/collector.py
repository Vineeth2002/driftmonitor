import requests
from datetime import datetime, timezone

TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def collect_hackernews(limit=10):
    ids = requests.get(TOP_STORIES, timeout=10).json()[:limit]

    results = []
    ts = datetime.now(timezone.utc).isoformat()

    for i in ids:
        item = requests.get(ITEM_URL.format(i), timeout=10).json()
        if not item or "title" not in item:
            continue

        results.append({
            "id": f"hn:{i}",
            "source": "hackernews",
            "title": item.get("title"),
            "text": item.get("title"),
            "collected_at": ts,
            "url": item.get("url"),
            "metadata": {"score": item.get("score")}
        })

    return {"results": results}
