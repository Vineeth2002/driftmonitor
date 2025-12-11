#!/usr/bin/env python3
"""
RunnerWrapper

Small wrapper to standardize model runner outputs and add metadata.
Used by benchmark orchestrator to call different runners uniformly.
"""

from __future__ import annotations
import logging
from typing import List, Dict, Any

logger = logging.getLogger("driftmonitor.benchmark.wrappers.runner_wrapper")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class RunnerWrapper:
    """
    Standardize runner outputs.

    Example:
        wrapped = RunnerWrapper(name="sentiment-distil").run(runner, texts)
    """

    def __init__(self, name: str):
        self.name = name

    def run(self, runner, texts: List[str]) -> Dict[str, Any]:
        """
        Run the provided runner (must have .predict(list[str]) -> list[dict]) and wrap results.

        Returns:
            {
                "runner": self.name,
                "n_items": len(texts),
                "predictions": [...],
            }
        """
        logger.info("Running runner wrapper: %s on %d texts", self.name, len(texts))
        preds = runner.predict(texts)
        return {"runner": self.name, "n_items": len(texts), "predictions": preds}
