import logging
import re
from typing import List, Dict, Any

from driftmonitor.benchmark.model_runners.sentiment_runner import SentimentRunner

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TOXIC_KEYWORDS = {
    "kill", "suicide", "terror", "bomb", "rape",
    "hate", "racist", "idiot", "stfu"
}

MISUSE_PATTERNS = {
    "jailbreak": 0.9,
    "bypass": 0.8,
    "override": 0.8,
    "disable safety": 0.9,
    "remove guardrails": 0.9,
}


class SafetyClassifier:
    """
    Produces safety scores for texts.

    Output keys:
    - text
    - sentiment_label
    - sentiment_score
    - toxicity_score
    - misuse_score
    - safety_score
    - risk_label
    - reason
    """

    def __init__(self):
        self.sentiment = SentimentRunner()

    def _toxicity_score(self, text: str) -> float:
        t = text.lower()
        hits = sum(1 for k in TOXIC_KEYWORDS if k in t)
        return min(1.0, hits / 3.0) if hits else 0.0

    def _misuse_score(self, text: str) -> float:
        t = text.lower()
        for k, v in MISUSE_PATTERNS.items():
            if re.search(k, t):
                return v
        return 0.0

    def score_texts(self, texts: List[str]) -> List[Dict[str, Any]]:
        if not texts:
            return []

        sentiments = self.sentiment.predict(texts)
        results = []

        for text, sent in zip(texts, sentiments):
            tox = self._toxicity_score(text)
            misuse = self._misuse_score(text)

            safety = 1.0
            safety -= tox * 0.6
            safety -= misuse * 0.8

            if sent["label"] == "NEGATIVE":
                safety -= 0.1 * sent["score"]

            safety = max(0.0, min(1.0, safety))

            if misuse >= 0.7:
                risk = "RISKY"
            elif tox >= 0.4 or sent["label"] == "NEGATIVE":
                risk = "WARNING"
            else:
                risk = "SAFE"

            results.append({
                "text": text,
                "sentiment_label": sent["label"],
                "sentiment_score": sent["score"],
                "toxicity_score": round(tox, 3),
                "misuse_score": round(misuse, 3),
                "safety_score": round(safety, 3),
                "risk_label": risk,
                "reason": f"sentiment={sent['label']} tox={tox:.2f} misuse={misuse:.2f}",
            })

        return results
