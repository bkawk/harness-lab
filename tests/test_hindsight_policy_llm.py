from __future__ import annotations

from harness_lab import hindsight as hindsight_module
from harness_lab import policy as policy_module
from harness_lab.workspace import create_candidate_workspace, write_json


def _make_candidate(candidates_dir, cid, *, outcome_label="dead_end", mechanism="encoder"):
    ws = create_candidate_workspace(candidates_dir, cid)
    write_json(
        ws.outcome_path,
        {
            "candidate_id": cid,
            "status": "complete",
            "outcome_label": outcome_label,
            "benchmark": {"score": 0.5, "summary": "ok"},
            "audit": {"score": 0.4, "summary": "ok"},
            "observed_failure_modes": [],
            "evidence": [],
        },
    )
    write_json(
        ws.diagnosis_path,
        {
            "candidate_id": cid,
            "status": "complete",
            "summary": "test",
            "severity": "medium",
            "mechanism": mechanism,
            "failure_modes": [],
            "evidence": [],
            "counterfactuals": [],
        },
    )
    return ws


def test_llm_hindsight_can_override_summary(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    _make_candidate(candidates_dir, "cand_0001")
    monkeypatch.setenv("HARNESS_LAB_LLM_HINDSIGHT_ENABLED", "1")
    monkeypatch.setattr(
        hindsight_module,
        "run_claude_json",
        lambda prompt, *, cwd: {
            "summary": "The lab is over-repeating the same mechanism and should diversify.",
            "hindsight_findings": ["The recent line is too repetitive."],
            "policy_adjustments": ["Increase novelty pressure for the next cycle."],
        },
    )
    result = hindsight_module.build_hindsight(candidates_dir)
    assert result["summary"].startswith("The lab is over-repeating")
    assert result["hindsight_reviewer"] == "claude"


def test_invalid_llm_hindsight_falls_back(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    _make_candidate(candidates_dir, "cand_0001")
    monkeypatch.setenv("HARNESS_LAB_LLM_HINDSIGHT_ENABLED", "1")
    monkeypatch.setattr(hindsight_module, "run_claude_json", lambda prompt, *, cwd: {"policy_adjustments": []})
    result = hindsight_module.build_hindsight(candidates_dir)
    assert "candidate_count" in result
    assert result.get("hindsight_reviewer") != "claude"


def test_llm_policy_can_override_summary(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    memory_dir = tmp_path / "memory"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "candidate_index.json", {"candidate_count": 3, "candidates": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "candidate_count": 3,
            "summary": "Heuristic hindsight.",
            "hindsight_findings": [],
            "policy_adjustments": [],
            "top_outcomes": [],
            "top_failure_modes": [],
            "over_explored_mechanisms": [],
            "under_explored_promising_mechanisms": [],
            "over_explored_backend_fingerprints": [],
            "under_explored_backend_fingerprints": [],
            "process_classification_counts": {},
            "throughput_summary": {},
        },
    )
    monkeypatch.setenv("HARNESS_LAB_LLM_POLICY_ENABLED", "1")
    monkeypatch.setattr(policy_module, "read_diversity", lambda memory_dir: {"summary": ""})
    monkeypatch.setattr(policy_module, "read_hardware_profile", lambda memory_dir: {"environment_hint": "linux_or_remote"})
    monkeypatch.setattr(policy_module, "read_backend_profile", lambda memory_dir: {"summary": "command backend", "command_backend_configured": True})
    monkeypatch.setattr(policy_module, "read_external_review", lambda memory_dir: {"status": "idle", "lab_advice": []})
    monkeypatch.setattr(
        policy_module,
        "run_claude_json",
        lambda prompt, *, cwd: {
            "summary": "Favor under-explored backend fingerprints while preserving throughput.",
            "selection_mode": "exploit_underexplored",
            "cooldown_multiplier": 1.4,
            "underexplored_bonus": 33,
            "backend_fingerprint_bonus": 18,
            "backend_fingerprint_cooldown": 14,
            "preferred_runner_backend": "command",
            "publish_every_cycles": 1,
            "novelty_cycle_priority": "normal",
            "policy_adjustments": ["Favor under-explored backend fingerprints."],
            "evidence": ["policy:llm_override"],
        },
    )
    result = policy_module.build_policy(candidates_dir, memory_dir)
    assert result["summary"].startswith("Favor under-explored backend fingerprints")
    assert result["policy_reviewer"] == "claude"
    assert result["selection_mode"] == "exploit_underexplored"


def test_invalid_llm_policy_falls_back(tmp_path, monkeypatch):
    candidates_dir = tmp_path / "candidates"
    memory_dir = tmp_path / "memory"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "candidate_index.json", {"candidate_count": 1, "candidates": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "candidate_count": 1,
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
            "top_outcomes": [],
            "top_failure_modes": [],
            "over_explored_mechanisms": [],
            "under_explored_promising_mechanisms": [],
            "over_explored_backend_fingerprints": [],
            "under_explored_backend_fingerprints": [],
            "process_classification_counts": {},
            "throughput_summary": {},
        },
    )
    monkeypatch.setenv("HARNESS_LAB_LLM_POLICY_ENABLED", "1")
    monkeypatch.setattr(policy_module, "read_diversity", lambda memory_dir: {"summary": ""})
    monkeypatch.setattr(policy_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(policy_module, "read_backend_profile", lambda memory_dir: {"summary": "", "command_backend_configured": False})
    monkeypatch.setattr(policy_module, "read_external_review", lambda memory_dir: {"status": "idle", "lab_advice": []})
    monkeypatch.setattr(policy_module, "run_claude_json", lambda prompt, *, cwd: {"selection_mode": "balanced"})
    result = policy_module.build_policy(candidates_dir, memory_dir)
    assert "summary" in result
    assert result.get("policy_reviewer") != "claude"
