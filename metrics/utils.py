from typing import Dict, Any, List

from driftmonitor.metrics.drift.metrics import texts_to_unigram_dist, jensen_shannon
from driftmonitor.metrics.toxicity.toxicity import batch_toxicity_stats


def extract_texts(eval_obj: Dict[str, Any]) -> List[str]:
    results = eval_obj.get("items", []) or eval_obj.get("safety_results", [])
    return [r.get("text", "") for r in results if isinstance(r.get("text"), str)]


def drift_between(eval_a: Dict[str, Any], eval_b: Dict[str, Any]) -> Dict[str, float]:
    p = texts_to_unigram_dist(extract_texts(eval_a))
    q = texts_to_unigram_dist(extract_texts(eval_b))
    return {"jsd": jensen_shannon(p, q)}


def toxicity_summary(eval_obj: Dict[str, Any]) -> Dict[str, float]:
    return batch_toxicity_stats(extract_texts(eval_obj))
