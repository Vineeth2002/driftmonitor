import os
import json
import tempfile
from driftmonitor.scripts.evaluate.run_evaluation import evaluate

def test_evaluation_pipeline(tmp_path, monkeypatch):
    # Prepare fake raw directory
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    # Create fake raw file
    raw_file = raw_dir / "fake_raw.json"
    raw_file.write_text(json.dumps({
        "results": [
            {"title": "AI safety is improving."},
            {"text": "This is a dangerous example."}
        ]
    }))

    # Monkeypatch global paths
    monkeypatch.setattr("driftmonitor.scripts.evaluate.run_evaluation.RAW_DIR", str(raw_dir))
    monkeypatch.setattr("driftmonitor.scripts.evaluate.run_evaluation.PROCESSED_DIR", str(processed_dir))

    out = evaluate()
    assert os.path.exists(out)
    data = json.load(open(out))
    assert "safety_results" in data
    assert len(data["safety_results"]) == 2
