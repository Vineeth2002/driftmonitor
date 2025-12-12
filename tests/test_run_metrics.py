import os
import json
from driftmonitor.scripts.metrics import run_metrics

def test_run_no_files(tmp_path, monkeypatch):
    # point processed dir to tmp empty dir
    monkeypatch.chdir(tmp_path)
    os.makedirs("data/live/processed", exist_ok=True)
    out = run_metrics.run()
    assert out == {} or isinstance(out, dict)
