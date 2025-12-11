import json
import os
import tempfile
from types import SimpleNamespace

import pytest

from driftmonitor.collectors.google_trends.collector import GoogleTrendsCollector, DEFAULT_OUTPUT_DIR, SAMPLE_FILE

MODULE_DIR = os.path.dirname(__file__)


def test_load_sample_exists():
    # sample file should exist in repo layout (test expects the path above)
    assert os.path.exists(SAMPLE_FILE), f"Sample file missing at {SAMPLE_FILE}"


def test_collect_fallback_to_sample(tmp_path, monkeypatch):
    # Simulate pytrends not installed by forcing TrendReq to None in module
    import importlib
    mod = importlib.import_module("driftmonitor.collectors.google_trends.collector")
    monkeypatch.setattr(mod, "TrendReq", None)

    collector = GoogleTrendsCollector(output_dir=str(tmp_path), kw_list=["nonexistent term"], max_terms=1)
    results = collector.collect()
    # expecting fallback sample (list)
    assert isinstance(results, list)
    assert len(results) >= 1
    # Save should create a file
    saved = collector.save(results)
    assert os.path.exists(saved)


def test_save_writes_files(tmp_path):
    # ensure save creates a JSON + CSV summary if possible
    collector = GoogleTrendsCollector(output_dir=str(tmp_path))
    sample = [
        {"keyword": "x", "timeframe": "now 1-d", "geo": "", "data_points": 2, "series": {"t1": 1, "t2": 2}}
    ]
    saved = collector.save(sample)
    assert os.path.exists(saved)
    summary_csv = saved.replace(".json", ".summary.csv")
    assert os.path.exists(summary_csv)
