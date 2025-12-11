#!/usr/bin/env python3
"""
Drift metrics: KL divergence & Jensen-Shannon divergence (JSD).

This implementation:
- Is lightweight and dependency-free (uses only Python stdlib).
- Works on discrete unigram token distributions derived from text lists.
- Provides helpers to convert texts -> distributions and compute KL / JSD.
- Avoids zero/undefined log by smoothing with a small epsilon.

Usage:
    from driftmonitor.metrics.drift.metrics import texts_to_unigram_dist, jensen_shannon, kldiv

    a = texts_to_unigram_dist(["this is a test", "another test"])
    b = texts_to_unigram_dist(["this is different"])
    jsd = jensen_shannon(a, b)
"""
from __future__ import annotations
import math
from collections import Counter
from typing import Dict, Iterable, List, Tuple

EPS = 1e-12  # smoothing to avoid log(0)


def tokenize(text: str) -> List[str]:
    """Very small tokenizer: lowercase + split on whitespace + simple punctuation strip."""
    if not isinstance(text, str):
        return []
    text = text.lower()
    for ch in '.,;:"()[]{}<>/?\\|`~!@#$%^&*-_=+':
        text = text.replace(ch, " ")
    toks = [t for t in text.split() if t]
    return toks


def texts_to_unigram_dist(texts: Iterable[str]) -> Dict[str, float]:
    """
    Convert iterable of texts into a unigram probability distribution dict.
    Returns mapping token -> probability (sums to 1).
    """
    counter = Counter()
    total = 0
    for text in texts:
        toks = tokenize(text)
        counter.update(toks)
        total += len(toks)
    if total == 0:
        return {}
    dist = {tok: count / total for tok, count in counter.items()}
    return dist


def _union_keys(p: Dict[str, float], q: Dict[str, float]) -> List[str]:
    return list(set(p.keys()) | set(q.keys()))


def kldiv(p: Dict[str, float], q: Dict[str, float]) -> float:
    """
    Compute Kullback-Leibler divergence KL(p || q).
    Both p and q are discrete distributions (dict token->prob).
    Returns a non-negative float; if q has zeros where p has mass, smoothing is used.
    """
    keys = _union_keys(p, q)
    kl = 0.0
    for k in keys:
        p_k = p.get(k, 0.0)
        q_k = q.get(k, 0.0)
        if p_k <= 0:
            continue
        # apply smoothing
        q_k = q_k if q_k > 0 else EPS
        kl += p_k * math.log(p_k / q_k)
    return kl


def jensen_shannon(p: Dict[str, float], q: Dict[str, float]) -> float:
    """
    Compute Jensen-Shannon divergence JSD(p || q) based on KL.
    Returns value in [0, ln(2)] if natural log used. Many users prefer normalized JSD in [0,1].
    This function returns normalized JSD in [0,1].
    """
    if not p and not q:
        return 0.0
    # make M = 0.5*(p+q)
    keys = _union_keys(p, q)
    m = {}
    for k in keys:
        m[k] = 0.5 * (p.get(k, 0.0) + q.get(k, 0.0))
    kl_pm = kldiv(p, m)
    kl_qm = kldiv(q, m)
    jsd = 0.5 * (kl_pm + kl_qm)
    # Normalize by ln(2) to map into [0,1]
    norm = jsd / math.log(2.0) if math.log(2.0) > 0 else jsd
    if norm < 0:
        norm = 0.0
    if norm > 1:
        norm = 1.0
    return norm
