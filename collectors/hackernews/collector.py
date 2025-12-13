import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def collect_hackernews(limit: int = 20):
    """
    Collect top Hacker News stories.

    Returns:
        list[dict]
    """
    collected_at = datetime.utcnow().isoformat() + "Z"

    try:
        ids = requests.get(TOP_STORIES, timeout=10).json()
        results = []

        for story_id in ids[:limit]:
            item = requests.get(ITEM_URL.format(story_id), timeout=10).json()
            if not item or "title" not in item:
                continue

            results.append({
                "source": "hackernews",
                "id": item.get("id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "score": item.get("score", 0),
                "collected_at": collected_at,
            })

        if not results:
            return _fallback(collected_at)

        return results

    except Exception as e:
        logger.exception("HackerNews failed, using fallback")
        return _fallback(collected_at)


def _fallback(collected_at: str):
    return [
        {
            "source": "hackernews",
            "id": 0,
            "title": "Fallback: AI safety discussion",
            "url": "https://news.ycombinator.com/",
            "score": 0,
            "collected_at": collected_at,
        }
    ]
