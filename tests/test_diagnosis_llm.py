from __future__ import annotations

from harness_lab import diagnosis as diagnosis_module
from harness_lab.workspace import create_candidate_workspace, write_json


def _seed_candidate(tmp_path):
    candidates_dir = tmp_path / "candidates"
    ws = create_candidate_workspace(candidates_dir, "cand_0001")
    write_json(
        ws.proposal_path,
        {
            "candidate_id": "cand_0001",
            "parent_id": None,
            "status": "candidate",
            "target": {
                "harness_component": "fusion_changed",
                "expected_failure_mode": "audit_blocked",
                "novelty_basis": "test better fusion stability",
            },
            "rationale": "Try a smaller fusion follow-up.",
            "changes": [{"kind": "guardrail", "mechanism": "fusion_changed", "summary": "Protect transfer."}],
        },
    )
    write_json(
        ws.outcome_path,
        {
            "candidate_id": "cand_0001",
            "status": "complete",
            "outcome_label": "audit_blocked",
            "benchmark": {"score": 0.34, "summary": "Benchmark improved."},
            "audit": {"score": 0.28, "summary": "Audit regressed."},
            "observed_failure_modes": ["transfer_collapse"],
            "evidence": ["science_metrics.json", "backend_result.json"],
        },
    )
    write_json(
        ws.diagnosis_path,
        {
            "candidate_id": "cand_0001",
            "status": "in_progress",
            "summary": "",
            "severity": "unknown",
            "mechanism": "",
            "failure_modes": [],
            "evidence": [],
            "counterfactuals": [],
        },
    )
    write_json(ws.traces_dir / "science_metrics.json", {"benchmark_audit_gap": 0.06})
    write_json(ws.traces_dir / "backend_result.json", {"device": "cuda"})
    (ws.traces_dir / "runner_stdout.log").write_text("training trace\n", encoding="utf-8")
    (ws.traces_dir / "runner_stderr.log").write_text("", encoding="utf-8")
    return candidates_dir


def test_llm_diagnosis_can_override_summary(tmp_path, monkeypatch):
    candidates_dir = _seed_candidate(tmp_path)
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HARNESS_LAB_LLM_DIAGNOSIS_ENABLED", "1")
    captured = {}

    def _fake_run(prompt, *, cwd):
        captured["prompt"] = prompt
        return {
            "summary": "Benchmark improved but audit regressed, suggesting transfer collapse in fusion_changed.",
            "severity": "high",
            "mechanism": "fusion_changed",
            "failure_modes": ["transfer_collapse"],
            "evidence": ["science_metrics.json", "backend_result.json"],
            "counterfactuals": ["Try a narrower fusion adjustment with stronger transfer guardrails."],
        }

    write_json(candidates_dir / "cand_0001" / "traces" / "science_progress.json", {"phase": "training", "steps": 40})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "Recent candidates trained to the wall-clock limit.", "likely_issue": "training_consumes_wall_clock_before_eval"})
    monkeypatch.setattr(
        diagnosis_module,
        "run_claude_json",
        _fake_run,
    )
    updated = diagnosis_module.reconcile_diagnosis_from_outcome(candidates_dir, "cand_0001")
    assert updated.summary.startswith("Benchmark improved but audit regressed")
    assert updated.severity == "high"
    assert updated.mechanism == "fusion_changed"
    assert '"science_progress"' in captured["prompt"]
    assert '"science_debug_summary"' in captured["prompt"]


def test_invalid_llm_diagnosis_falls_back_to_heuristic(tmp_path, monkeypatch):
    candidates_dir = _seed_candidate(tmp_path)
    monkeypatch.setenv("HARNESS_LAB_LLM_DIAGNOSIS_ENABLED", "1")
    monkeypatch.setattr(diagnosis_module, "run_claude_json", lambda prompt, *, cwd: {"severity": "critical"})
    updated = diagnosis_module.reconcile_diagnosis_from_outcome(candidates_dir, "cand_0001")
    assert updated.severity == "high"
    assert "Outcome audit_blocked." in updated.summary
