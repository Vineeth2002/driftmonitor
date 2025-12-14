from pytrends.request import TrendReq
import pandas as pd
import time
import os
from datetime import datetime

os.makedirs("data/raw", exist_ok=True)

today = datetime.utcnow().strftime("%Y-%m-%d")
outfile = f"data/raw/google_trends_{today}.csv"

try:
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(
        ["artificial intelligence", "AI safety", "AI regulation"],
        timeframe="now 1-d"
    )

    time.sleep(10)  # prevent 429

    df = pytrends.interest_over_time()

    if df.empty:
        raise Exception("Empty trends data")

    df.reset_index(inplace=True)
    df.to_csv(outfile, index=False)
    print("Google Trends collected")

except Exception as e:
    print("Google Trends skipped:", e)
    pd.DataFrame(
        {"date": [], "note": ["rate limited or unavailable"]}
    ).to_csv(outfile, index=False)
