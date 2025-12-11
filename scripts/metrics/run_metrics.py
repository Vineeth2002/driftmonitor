#!/usr/bin/env python3
"""
Aggregate evaluation summaries into daily, weekly and monthly metric files.

Outputs (written to data/live/processed/):
- metrics_daily.json
- metrics_weekly.json
- metrics_monthly.json
- drift_summary.json
"""
from __future__ import annotations
import json
import glob
import os
from datetime import datetime, timezone
from collections import defaultdict
import re

PROCESSED_DIR = os.path.abspath("data/live/processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

def parse_date(ts_str: str):
    try:
        return datetime.strptime(ts_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        try:
            return datetime.fromisoformat(ts_str)
        except Exception:
            try:
                return datetime.strptime(ts_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except Exception:
                return None

def aggregate():
    files = sorted(
        glob.glob(os.path.join(PROCESSED_DIR, "eval_summary_*.json")) +
        glob.glob(os.path.join(PROCESSED_DIR, "eval_*.json")) +
        glob.glob(os.path.join(PROCESSED_DIR, "eval_sample*.json"))
    )
    if not files:
        print("No eval_summary or eval files found in", PROCESSED_DIR)
        return

    daily = defaultdict(lambda: {"label_counts": defaultdict(int), "n_risky": 0, "n_texts": 0})
    weekly = defaultdict(lambda: {"label_counts": defaultdict(int), "n_risky": 0, "n_texts": 0})
    monthly = defaultdict(lambda: {"label_counts": defaultdict(int), "n_risky": 0, "n_texts": 0})

    for p in files:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue

        ts = data.get("evaluated_at")
        dt = parse_date(ts) if ts else None
        if dt is None:
            bn = os.path.basename(p)
            m = re.search(r"(\d{8}T\d{6}Z|\d{8})", bn)
            if m:
                dt = parse_date(m.group(1))
        if dt is None:
            dt = datetime.fromtimestamp(os.path.getmtime(p), tz=timezone.utc)

        day_key = dt.strftime("%Y-%m-%d")
        week_key = f"{dt.strftime('%Y')}-W{dt.isocalendar()[1]:02d}"
        month_key = dt.strftime("%Y-%m")

        label_counts = data.get("label_counts")
        n_texts = data.get("n_texts") or 0
        n_risky = data.get("n_risky") or 0

        if label_counts is None and "safety_results" in data:
            counts = defaultdict(int)
            n_texts = len(data.get("safety_results", []))
            n_risky = 0
            threshold = float(data.get("safety_threshold", 0.6) if data.get("safety_threshold") is not None else 0.6)
            for item in data.get("safety_results", []):
                lbl = (item.get("sentiment_label") or "UNKNOWN").upper()
                counts[lbl] += 1
                try:
                    ss = float(item.get("safety_score", 1.0))
                except Exception:
                    ss = 1.0
                if ss < threshold:
                    n_risky += 1
            label_counts = dict(counts)
        elif label_counts is None:
            label_counts = {}

        def add_agg(container, key):
            for k, v in (label_counts or {}).items():
                container[key]["label_counts"][k] = container[key]["label_counts"].get(k, 0) + int(v)
            container[key]["n_risky"] += int(n_risky)
            container[key]["n_texts"] += int(n_texts)

        add_agg(daily, day_key)
        add_agg(weekly, week_key)
        add_agg(monthly, month_key)

    def clean(d):
        out = {}
        for k, v in sorted(d.items()):
            out[k] = {
                "label_counts": dict(v["label_counts"]),
                "n_risky": int(v["n_risky"]),
                "n_texts": int(v["n_texts"]),
            }
        return out

    metrics_daily = clean(daily)
    metrics_weekly = clean(weekly)
    metrics_monthly = clean(monthly)

    drift = {"eval_a": None, "eval_b": None, "drift": {"n_risky_change_pct": None}}
    try:
        days = sorted(metrics_daily.keys())
        if len(days) >= 2:
            a, b = days[-2], days[-1]
            drift["eval_a"] = a
            drift["eval_b"] = b
            a_r = metrics_daily[a]["n_risky"]
            b_r = metrics_daily[b]["n_risky"]
            change = None
            if a_r == 0:
                change = None
            else:
                change = (b_r - a_r) / float(max(1, a_r))
            drift["drift"]["n_risky_change_pct"] = change
    except Exception:
        pass

    def write_json(fname, obj):
        path = os.path.join(PROCESSED_DIR, fname)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
        print("Wrote", path)

    write_json("metrics_daily.json", metrics_daily)
    write_json("metrics_weekly.json", metrics_weekly)
    write_json("metrics_monthly.json", metrics_monthly)
    write_json("drift_summary.json", drift)

if __name__ == "__main__":
    aggregate()
