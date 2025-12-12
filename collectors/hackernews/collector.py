import requests
import json
import os
from datetime import datetime

HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

KEYWORDS = [
    "ai", "llm", "prompt", "jailbreak",
    "alignment", "safety", "openai"
]

def run():
    ids = requests.get(HN_TOP, timeout=10).json()[:100]

    today = datetime.utcnow().strftime("%Y-%m-%d")
    out_dir = f"data/live/raw/{today}"
    os.makedirs(out_dir, exist_ok=True)

    results = []
    for i in ids:
        item = requests.get(HN_ITEM.format(i), timeout=10).json()
        if not item or "title" not in item:
            continue

        text = (item.get("title", "") + " " + item.get("text", "")).lower()
        if any(k in text for k in KEYWORDS):
            results.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "url": item.get("url"),
                "time": item.get("time"),
                "source": "hackernews"
            })

    with open(f"{out_dir}/hackernews.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
