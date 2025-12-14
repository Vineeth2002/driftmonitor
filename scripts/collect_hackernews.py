import requests
import pandas as pd
from datetime import datetime
import os

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

ids = requests.get(TOP_URL, timeout=10).json()[:50]
rows = []

for i in ids:
    item = requests.get(ITEM_URL.format(i), timeout=10).json()
    if not item:
        continue

    title = item.get("title", "")
    if "ai" in title.lower():
        rows.append({
            "id": i,
            "title": title,
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "time": datetime.utcfromtimestamp(item["time"])
        })

df = pd.DataFrame(rows)

today = datetime.utcnow().strftime("%Y-%m-%d")
os.makedirs("data/raw", exist_ok=True)
df.to_csv(f"data/raw/hackernews_{today}.csv", index=False)

print("Hacker News collected:", today)
