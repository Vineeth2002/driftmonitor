#!/usr/bin/env python3
"""
SentimentRunner

Attempts to use Hugging Face `transformers` pipeline for sentiment analysis
(using a small off-the-shelf model). If `transformers` is not installed or
loading the model fails (e.g., offline runner), the code falls back to a
very small rule-based sentiment heuristic (polarity via word lists).

This runner is lightweight and safe to run inside GitHub Actions.
"""

from __future__ import annotations
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("driftmonitor.benchmark.model_runners.sentiment")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Try to import transformers pipeline; may not be available in small GH runners
try:
    from transformers import pipeline, Pipeline
except Exception:  # pragma: no cover - runtime optional import
    pipeline = None  # type: ignore
    Pipeline = None  # type: ignore

# Simple word lists for fallback rule-based sentiment
_POSITIVE_WORDS = {
    "good",
    "great",
    "positive",
    "safe",
    "improved",
    "benefit",
    "helpful",
    "accurate",
    "success",
    "stable",
}
_NEGATIVE_WORDS = {
    "bad",
    "worse",
    "danger",
    "unsafe",
    "harmful",
    "misleading",
    "problem",
    "error",
    "fail",
    "toxic",
}


class SentimentRunner:
    """
    SentimentRunner class.

    Methods
    -------
    predict(texts: List[str]) -> List[Dict[str, Any]]
        Returns a list of predictions with fields: label, score, model (str).
    """

    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.pipeline: Optional[Pipeline] = None
        self._init_pipeline()

    def _init_pipeline(self) -> None:
        """Initialize transformers pipeline if available; otherwise leave None."""
        if pipeline is None:
            logger.warning("transformers pipeline not available — using fallback rule-based sentiment.")
            self.pipeline = None
            return
        try:
            logger.info("Loading transformers pipeline model: %s", self.model_name)
            self.pipeline = pipeline("sentiment-analysis", model=self.model_name)
        except Exception as exc:
            logger.exception("Failed to init transformers pipeline (%s) — using fallback.", exc)
            self.pipeline = None

    def _rule_based(self, text: str) -> Dict[str, Any]:
        """Very small, fast heuristic sentiment scorer (fallback)."""
        txt = text.lower()
        pos = sum(1 for w in _POSITIVE_WORDS if w in txt)
        neg = sum(1 for w in _NEGATIVE_WORDS if w in txt)
        # score normalized between 0 and 1
        score = 0.5
        if pos + neg > 0:
            score = float(pos) / (pos + neg)
        label = "POSITIVE" if score >= 0.5 else "NEGATIVE"
        return {"label": label, "score": score, "model": "rule-fallback"}

    def predict(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predict sentiment for each text.

        Returns list of dicts: {"label": str, "score": float, "model": str}
        """
        if not texts:
            return []

        # Use transformers pipeline if available
        if self.pipeline is not None:
            try:
                preds = self.pipeline(texts, truncation=True)
                # pipeline returns e.g. [{"label": "POSITIVE", "score": 0.999}]
                result = []
                for p in preds:
                    result.append({"label": p.get("label"), "score": float(p.get("score") or 0.0), "model": self.model_name})
                return result
            except Exception as exc:
                logger.exception("Transformers pipeline failed during prediction: %s", exc)
                # fall through to rule-based fallback

        # Fallback: rule-based
        return [self._rule_based(t) for t in texts]
