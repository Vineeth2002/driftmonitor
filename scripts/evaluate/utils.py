"""
Utility functions for evaluation pipeline.
"""

import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("driftmonitor.scripts.evaluate.utils")


def load_latest_json(path: str) -> Dict[str, Any]:
    """Load JSON and return dictionary (safe)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error("Failed to read JSON %s: %s", path, exc)
        return {"results": []}


def extract_text_fields(items: List[Dict[str, Any]]) -> List[str]:
    """
    Extract text-like fields from HackerNews, GoogleTrends, Custom prompts, etc.

    - From HackerNews: "title"
    - From Custom: "text"
    - From Google Trends: convert keywords + timestamps into synthetic text
    """

    texts = []

    for item in items:
        # HackerNews items
        if "title" in item and isinstance(item["title"], str):
            texts.append(item["title"])

        # Custom prompts
        if "text" in item and isinstance(item["text"], str):
            texts.append(item["text"])

        # Google Trends items
        if "keyword" in item and isinstance(item["keyword"], str):
            texts.append(f"Trend keyword: {item['keyword']} shows variation")

    return texts
