# Benchmark Module (DriftMonitor)

This module provides lightweight model runners, wrappers, and a small safety classifier.

Key points:
- Attempts to use Hugging Face `transformers` pipeline for better quality when available.
- If `transformers` or weights are not available (common in lightweight CI), falls back to fast,
  interpretable rule-based heuristics so the pipeline always produces results.
- Designed for GitHub Actions: small, deterministic, and reproducible outputs.

Usage example (python REPL):
```python
from driftmonitor.benchmark.classifiers.safety_classifier import SafetyClassifier
clf = SafetyClassifier()
texts = ["This is dangerous", "This looks safe and helpful"]
print(clf.score_texts(texts))
