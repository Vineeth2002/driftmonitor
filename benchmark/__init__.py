"""
DriftMonitor - Benchmark package

Provides small model runners, wrappers, and safety classifier implementations.
The code attempts to use transformers pipelines if available, otherwise falls
back to a lightweight rule-based classifier suitable for CI and GitHub Actions.
"""

__all__ = ["runners", "wrappers", "classifiers"]
