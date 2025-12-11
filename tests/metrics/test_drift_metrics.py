
---

### File: `DriftMonitor/tests/metrics/test_drift_metrics.py`
```python
from driftmonitor.metrics.drift.metrics import texts_to_unigram_dist, jensen_shannon, kldiv
from driftmonitor.metrics.toxicity.toxicity import toxicity_hits, batch_toxicity_stats

def test_texts_to_unigram_dist_and_divergences():
    a_texts = ["This is safe", "Model is helpful and safe"]
    b_texts = ["This is dangerous", "This is harmful and dangerous"]
    p = texts_to_unigram_dist(a_texts)
    q = texts_to_unigram_dist(b_texts)
    assert isinstance(p, dict) and isinstance(q, dict)
    # JSD should be between 0 and 1
    jsd = jensen_shannon(p, q)
    assert 0.0 <= jsd <= 1.0

    # KL is non-negative
    klpq = kldiv(p, q)
    assert klpq >= 0.0

def test_toxicity_helpers():
    t = "This is dangerous and you should kill it"
    hits = toxicity_hits(t)
    assert hits >= 1
    stats = batch_toxicity_stats([t, "safe text"])
    assert stats["n_texts"] == 2
    assert stats["total_hits"] >= 1
