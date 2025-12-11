#!/usr/bin/env python3
"""
Toxicity metrics helpers.

Simple, interpretable toxicity metrics:
- counts toxic keyword hits per text
- computes average toxicity across a batch
- designed for lightweight demo & reports
"""

from __future__ import annotations
from typing import Iterable, List, Dict

# small toxicity keyword list (extendable)
DEFAULT_TOXIC_KEYWORDS = {
    "kill",
    "suicide",
    "terror",
    "bomb",
    "rape",
    "idiot",
    "stfu",
    "hate",
    "racist",
    "slur",
}


def toxicity_hits(text: str, keywords: Iterable[str] = DEFAULT_TOXIC_KEYWORDS) -> int:
    """Return number of toxic keyword hits in a text (case-insensitive substring match)."""
    if not isinstance(text, str):
        return 0
    t = text.lower()
    hits = 0
    for k in keywords:
        if k in t:
            hits += 1
    return hits


def batch_toxicity_stats(texts: Iterable[str], keywords: Iterable[str] = DEFAULT_TOXIC_KEYWORDS) -> Dict[str, object]:
    """
    Compute batch toxicity statistics:
    - n_texts
    - total_hits
    - avg_hits_per_text
    - pct_with_hits
    """
    texts = list(texts)
    n = len(texts)
    if n == 0:
        return {"n_texts": 0, "total_hits": 0, "avg_hits_per_text": 0.0, "pct_with_hits": 0.0}
    hits_list = [toxicity_hits(t, keywords) for t in texts]
    total = sum(hits_list)
    pct = sum(1 for h in hits_list if h > 0) / n
    return {
        "n_texts": n,
        "total_hits": total,
        "avg_hits_per_text": total / n,
        "pct_with_hits": pct,
    }
