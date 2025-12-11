#!/usr/bin/env python3
"""
Metrics utilities: helpers to prepare distributions from processed data and to compute drift metrics.
"""

from __future__ import annotations
from typing import List, Dict, Any
from driftmonitor.metrics.drift.metrics import texts_to_unigram_dist, jensen_shannon
from driftmonitor.metrics.toxicity.toxicity import batch_toxicity_stats


def build_unigram_from_results(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Given a list of evaluation results (e.g., safety_results from processed JSON),
    extract the 'text' fields and return a unigram distribution.
    """
    texts = [r.get("text", "") for r in results if isinstance(r.get("text", ""), str)]
    return texts_to_unigram_dist(texts)


def compute_drift_between(eval_a: Dict[str, Any], eval_b: Dict[str, Any]) -> Dict[str, float]:
    """
    Given two evaluation dicts (structure: {"safety_results": [...] }),
    compute JSD between their unigram distributions and return summary.
    """
    a_results = eval_a.get("safety_results", [])
    b_results = eval_b.get("safety_results", [])
    p = build_unigram_from_results(a_results)
    q = build_unigram_from_results(b_results)
    jsd = jensen_shannon(p, q)
    return {"jsd": jsd}


def toxicity_summary_of(eval_obj: Dict[str, Any]) -> Dict[str, object]:
    """Compute toxicity summary for an evaluation object (uses toxicity defaults)."""
    results = eval_obj.get("safety_results", [])
    texts = [r.get("text", "") for r in results if isinstance(r.get("text", ""), str)]
    return batch_toxicity_stats(texts)
