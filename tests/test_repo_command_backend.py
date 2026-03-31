from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_repo_command_backend():
    path = Path(__file__).resolve().parents[1] / "scripts" / "repo_command_backend.py"
    spec = importlib.util.spec_from_file_location("repo_command_backend_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_dataset_counts_handles_string_preprocess_manifest():
    module = _load_repo_command_backend()
    train_count, val_count = module.dataset_counts(
        {"preprocess_manifest": "preprocess/preprocess_manifest.json"},
        {
            "splits": {
                "train": [{"num_samples": 448}],
                "val": [{"num_samples": 64}],
            }
        },
    )
    assert train_count == 448
    assert val_count == 64


def test_oom_error_becomes_vram_failure_mode(tmp_path, monkeypatch):
    module = _load_repo_command_backend()
    result_path = tmp_path / "result.json"
    proposal_path = tmp_path / "proposal.json"
    diagnosis_path = tmp_path / "diagnosis.json"
    plan_path = tmp_path / "plan.json"
    proposal_path.write_text('{"target":{"harness_component":"fusion_changed","expected_failure_mode":""},"changes":[]}\n', encoding="utf-8")
    diagnosis_path.write_text('{"mechanism":"fusion_changed"}\n', encoding="utf-8")
    plan_path.write_text('{"benchmark":{"objective":"test"}}\n', encoding="utf-8")

    monkeypatch.setenv("HARNESS_LAB_CANDIDATE_ID", "cand_oom")
    monkeypatch.setenv("HARNESS_LAB_RESULT_PATH", str(result_path))
    monkeypatch.setenv("HARNESS_LAB_PROPOSAL_PATH", str(proposal_path))
    monkeypatch.setenv("HARNESS_LAB_DIAGNOSIS_PATH", str(diagnosis_path))
    monkeypatch.setenv("HARNESS_LAB_PLAN_PATH", str(plan_path))
    monkeypatch.setenv("HARNESS_LAB_DATASET_ID", "abc_boundary512")
    monkeypatch.setenv("HARNESS_LAB_DATASET_PATH", "")

    module.fallback_backend(RuntimeError("CUDA out of memory. Tried to allocate 304.00 MiB."))
    payload = module.read_json(result_path)
    assert "cuda_oom" in payload["observed_failure_modes"]
    assert "vram_pressure" in payload["observed_failure_modes"]
