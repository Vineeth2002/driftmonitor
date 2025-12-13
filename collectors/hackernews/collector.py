import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def collect_hackernews(limit: int = 10):
    """
    Collect HackerNews top stories.
    Safe fallback included.
    """
    collected_at = datetime.utcnow().isoformat() + "Z"

    try:
        ids = requests.get(HN_TOP_STORIES, timeout=10).json()[:limit]
        results = []

        for story_id in ids:
            item = requests.get(HN_ITEM.format(story_id), timeout=10).json()
            if not item:
                continue

            results.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title", ""),
                    "text": item.get("title", ""),
                    "url": item.get("url", ""),
                    "score": item.get("score", 0),
                }
            )

        return {
            "source": "hackernews",
            "collected_at": collected_at,
            "results": results,
        }

    except Exception as exc:
        logger.exception("HackerNews failed, fallback used: %s", exc)
        return {
            "source": "hackernews",
            "collected_at": collected_at,
            "results": [
                {
                    "id": "fallback",
                    "title": "Sample HackerNews item",
                    "text": "Sample HackerNews item",
                    "url": "",
                    "score": 0,
                }
            ],
        }
