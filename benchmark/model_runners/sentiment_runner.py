import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Try transformers (optional)
try:
    from transformers import pipeline
except Exception:
    pipeline = None

POS_WORDS = {"good", "safe", "helpful", "positive", "improve"}
NEG_WORDS = {"bad", "danger", "harm", "toxic", "fail"}


class SentimentRunner:
    """
    Lightweight sentiment runner with safe fallback.
    """

    def __init__(self):
        self.model = None
        if pipeline is not None:
            try:
                self.model = pipeline("sentiment-analysis")
            except Exception:
                logger.warning("Transformers unavailable, using fallback")

    def _fallback(self, text: str) -> Dict:
        text = text.lower()
        pos = sum(1 for w in POS_WORDS if w in text)
        neg = sum(1 for w in NEG_WORDS if w in text)
        score = 0.5 if pos + neg == 0 else pos / (pos + neg)
        label = "POSITIVE" if score >= 0.5 else "NEGATIVE"
        return {"label": label, "score": round(score, 2)}

    def predict(self, texts: List[str]) -> List[Dict]:
        results = []

        for t in texts:
            if self.model:
                try:
                    r = self.model(t[:512])[0]
                    results.append({
                        "label": r["label"],
                        "score": float(r["score"]),
                    })
                    continue
                except Exception:
                    pass

            results.append(self._fallback(t))

        return results
