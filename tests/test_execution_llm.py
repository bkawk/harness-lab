from __future__ import annotations

from harness_lab import execution as execution_module
from harness_lab.workspace import create_candidate_workspace, write_json


def _seed_candidate(tmp_path):
    candidates_dir = tmp_path / "candidates"
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    ws = create_candidate_workspace(candidates_dir, "cand_0001")
    write_json(
        ws.proposal_path,
        {
            "candidate_id": "cand_0001",
            "dataset_id": "abc_boundary512_v64",
            "target": {
                "harness_component": "fusion_changed",
                "expected_failure_mode": "audit_blocked",
                "novelty_basis": "test a tighter fusion follow-up",
            },
            "rationale": "Try a smaller fusion change with better transfer stability.",
            "changes": [
                {
                    "kind": "guardrail",
                    "mechanism": "fusion_changed",
                    "summary": "Protect transfer while testing fusion.",
                }
            ],
        },
    )
    write_json(
        ws.diagnosis_path,
        {
            "candidate_id": "cand_0001",
            "status": "complete",
            "summary": "Parent suffered audit_blocked after a benchmark gain.",
            "severity": "high",
            "mechanism": "fusion_changed",
            "failure_modes": ["audit_blocked"],
            "evidence": [],
            "counterfactuals": ["Try a narrower fusion change."],
        },
    )
    write_json(
        ws.memory_dir / "bootstrap_snapshot.json",
        {
            "candidate_id": "cand_0001",
            "policy_summary": "Prefer transfer-stable follow-ups.",
        },
    )
    return candidates_dir


def test_llm_execution_can_author_plan(tmp_path, monkeypatch):
    candidates_dir = _seed_candidate(tmp_path)
    monkeypatch.setenv("HARNESS_LAB_LLM_EXECUTION_ENABLED", "1")
    monkeypatch.setattr(execution_module, "read_hardware_profile", lambda memory_dir: {"environment_hint": "linux_or_remote"})
    monkeypatch.setattr(execution_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "source": "abc", "status": "ready"})
    monkeypatch.setattr(
        execution_module,
        "run_claude_json",
        lambda prompt, *, cwd: {
            "rationale": "Run a benchmark first, then audit only if transfer looks stable.",
            "benchmark": {
                "objective": "Measure whether the smaller fusion change improves benchmark IoU without destabilizing transfer.",
                "steps": ["Apply the fusion change.", "Run the benchmark split.", "Inspect transfer-sensitive metrics."],
                "success_signals": ["Benchmark improves.", "Transfer gap stays bounded."],
            },
            "audit": {
                "required": True,
                "steps": ["Run the audit split if the benchmark is promising."],
                "failure_signals": ["Audit regresses relative to the parent."],
            },
            "trace_capture": ["benchmark_trace", "benchmark_metrics", "audit_trace"],
        },
    )
    plan = execution_module.plan_execution_for_candidate(candidates_dir, "cand_0001")
    assert plan.rationale.startswith("Run a benchmark first")
    assert plan.benchmark["objective"].startswith("Measure whether the smaller fusion change")
    assert plan.audit["required"] is True


def test_invalid_llm_execution_falls_back_to_heuristic(tmp_path, monkeypatch):
    candidates_dir = _seed_candidate(tmp_path)
    monkeypatch.setenv("HARNESS_LAB_LLM_EXECUTION_ENABLED", "1")
    monkeypatch.setattr(execution_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(execution_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "source": "abc", "status": "ready"})
    monkeypatch.setattr(execution_module, "run_claude_json", lambda prompt, *, cwd: {"benchmark": {}})
    plan = execution_module.plan_execution_for_candidate(candidates_dir, "cand_0001")
    assert "Try a smaller fusion change" in plan.rationale
    assert any("Use dataset abc_boundary512_v64 from abc." == step for step in plan.benchmark["steps"])
