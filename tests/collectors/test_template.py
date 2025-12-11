import os
from driftmonitor.collectors.template.collector import CustomPromptsCollector, TemplateCollector, SAMPLE_FILE


def test_sample_exists():
    assert os.path.exists(SAMPLE_FILE), f"Sample file missing: {SAMPLE_FILE}"


def test_custom_prompts_collect_and_save(tmp_path):
    collector = CustomPromptsCollector(output_dir=str(tmp_path), max_items=10)
    results = collector.collect()
    assert isinstance(results, list)
    assert len(results) >= 1
    saved = collector.save(results)
    assert os.path.exists(saved)
