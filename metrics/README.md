# Metrics Module (DriftMonitor)

This module provides lightweight, dependency-free metrics for:

- Distributional drift:
  - Kullback–Leibler divergence (KL)
  - Jensen–Shannon divergence (JSD) — returned normalized to [0,1]
- Toxicity statistics:
  - Token/sub-string based toxic keyword hits
  - Batch-level summaries

Design goals:
- Small and interpretable metrics useful for reports and admissions review.
- No heavy dependencies so it runs reliably in GitHub Actions.
- Easily extended: replace tokenizer or use pre-built embeddings later.

Quick usage:
```python
from driftmonitor.metrics.utils import compute_drift_between, toxicity_summary_of
a = json.load(open("data/live/processed/eval_20251201T000000Z.json"))
b = json.load(open("data/live/processed/eval_20251208T000000Z.json"))
print(compute_drift_between(a,b))
print(toxicity_summary_of(b))
