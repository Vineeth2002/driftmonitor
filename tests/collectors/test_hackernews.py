import json
import os
import tempfile
from unittest.mock import Mock

import pytest
import requests

from driftmonitor.collectors.hackernews.collector import HackerNewsCollector, SAMPLE_FILE, HN_TOP_STORIES, HN_ITEM_URL


def test_sample_exists():
    assert os.path.exists(SAMPLE_FILE), f"Sample file missing at {SAMPLE_FILE}"


def test_collect_fallback_on_network_error(monkeypatch, tmp_path):
    # Simulate requests.get raising an exception for the topstories endpoint
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network down")

    monkeypatch.setattr("requests.get", raise_exc)
    collector = HackerNewsCollector(output_dir=str(tmp_path), fetch_top_n=5)
    results = collector.collect()
    assert isinstance(results, list)
    assert len(results) >= 1
    saved = collector.save(results)
    assert os.path.exists(saved)


def test_collect_success(monkeypatch, tmp_path):
    # Mock topstories returning two IDs and items for them
    top_ids_resp = Mock()
    top_ids_resp.raise_for_status = Mock()
    top_ids_resp.json = Mock(return_value=[1111, 2222])

    item_resp_1 = Mock()
    item_resp_1.raise_for_status = Mock()
    item_resp_1.json = Mock(return_value={
        "id": 1111, "type": "story", "by": "user1", "time": 1700000000, "title": "T1", "url": "http://t1", "score": 10, "descendants": 1
    })
    item_resp_2 = Mock()
    item_resp_2.raise_for_status = Mock()
    item_resp_2.json = Mock(return_value={
        "id": 2222, "type": "story", "by": "user2", "time": 1700000100, "title": "T2", "url": "http://t2", "score": 5, "descendants": 0
    })

    # The first call to requests.get -> topstories, then item 1111, then 2222
    sequence = [top_ids_resp, item_resp_1, item_resp_2]

    def side_effect(url, *args, **kwargs):
        return sequence.pop(0)

    monkeypatch.setattr("requests.get", side_effect)
    collector = HackerNewsCollector(output_dir=str(tmp_path), fetch_top_n=2)
    results = collector.collect()
    assert isinstance(results, list)
    assert len(results) == 2
    saved = collector.save(results)
    assert os.path.exists(saved)
