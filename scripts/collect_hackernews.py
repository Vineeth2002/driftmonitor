import requests
import pandas as pd
from datetime import datetime
import os

HN_API = "https://hacker-news.firebaseio.com/v0"
TOP_STORIES_URL = f"{HN_API}/topstories.json"

story_ids = requests.get(TOP_STORIES_URL, timeout=10).json()[:50]

records = []

for sid in story_ids:
    item = requests.get(f"{HN_API}/item/{sid}.json", timeout=10).json()
    if not item:
        continue
    title = item.get("title", "")
    if "ai" in title.lower():
        records.append({
            "id": sid,
            "title": title,
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "time": datetime.utcfromtimestamp(item["time"])
        })

df = pd.DataFrame(records)

today = datetime.utcnow().strftime("%Y-%m-%d")
os.makedirs("data/raw", exist_ok=True)
output_path = f"data/raw/hackernews_{today}.csv"

df.to_csv(output_path, index=False)
print(f"[OK] Hacker News saved → {output_path}")
