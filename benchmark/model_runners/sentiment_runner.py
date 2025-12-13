import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    from transformers import pipeline
except Exception:
    pipeline = None

POS_WORDS = {"good", "safe", "helpful", "benefit", "positive"}
NEG_WORDS = {"bad", "danger", "unsafe", "toxic", "harmful", "kill"}


class SentimentRunner:
    def __init__(self):
        self.pipe = None
        if pipeline is not None:
            try:
                self.pipe = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                )
            except Exception:
                self.pipe = None

    def _fallback(self, text: str) -> Dict[str, Any]:
        t = text.lower()
        pos = sum(w in t for w in POS_WORDS)
        neg = sum(w in t for w in NEG_WORDS)
        score = pos / (pos + neg) if (pos + neg) > 0 else 0.5
        label = "POSITIVE" if score >= 0.5 else "NEGATIVE"
        return {"label": label, "score": score}

    def predict(self, texts: List[str]) -> List[Dict[str, Any]]:
        if not texts:
            return []

        if self.pipe is not None:
            try:
                preds = self.pipe(texts, truncation=True)
                return [{"label": p["label"], "score": float(p["score"])} for p in preds]
            except Exception:
                pass

        return [self._fallback(t) for t in texts]
