from __future__ import annotations

from harness_lab.memory import build_backend_code_map


def test_backend_code_map_includes_modules_and_failure_hints(tmp_path):
    payload = build_backend_code_map(tmp_path)

    assert payload["module_count"] == 5
    modules = {item["module"]: item for item in payload["modules"]}
    assert "science_train" in modules
    assert "batch_size" in modules["science_train"]["levered_surfaces"]
    assert "run_training_cycle" in modules["science_train"]["key_functions"]

    hints = {item["failure_mode"]: item for item in payload["failure_to_code_hints"]}
    assert "vram_headroom" in hints
    assert "science_train" in hints["vram_headroom"]["likely_modules"]
