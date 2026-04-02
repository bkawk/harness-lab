from __future__ import annotations

import harness_lab.big_bang as big_bang
from harness_lab.big_bang import _latest_backend_science_artifacts, _latest_live_command_artifact
from harness_lab.workspace import write_json


def test_latest_backend_science_artifacts_prefers_most_recent_candidate_with_lever_payload(tmp_path):
    candidates_dir = tmp_path / "candidates"
    for name in ("cand_0001", "cand_0002", "cand_0003"):
        (candidates_dir / name / "traces").mkdir(parents=True, exist_ok=True)

    write_json(
        candidates_dir / "cand_0002" / "proposal.json",
        {"backend_levers": {"science_model": {"hidden_dim": 160}}},
    )
    write_json(
        candidates_dir / "cand_0002" / "traces" / "effective_backend_config.json",
        {"hidden_dim": 160, "batch_size": 2},
    )
    write_json(
        candidates_dir / "cand_0003" / "proposal.json",
        {"backend_levers": {}},
    )

    index = {
        "candidates": [
            {"candidate_id": "cand_0001"},
            {"candidate_id": "cand_0002"},
            {"candidate_id": "cand_0003"},
        ]
    }
    state = {"active_candidate_id": "cand_0003", "last_candidate_id": "cand_0003"}

    explicit_id, explicit_payload, effective_id, effective_payload = _latest_backend_science_artifacts(
        candidates_dir,
        index,
        state,
    )

    assert explicit_id == "cand_0002"
    assert explicit_payload == {"science_model": {"hidden_dim": 160}}
    assert effective_id == "cand_0002"
    assert effective_payload["hidden_dim"] == 160


def test_latest_live_command_artifact_falls_back_to_most_recent_candidate_with_data(tmp_path):
    candidates_dir = tmp_path / "candidates"
    for name in ("cand_0001", "cand_0002", "cand_0003"):
        (candidates_dir / name / "traces").mkdir(parents=True, exist_ok=True)

    write_json(
        candidates_dir / "cand_0002" / "traces" / "live_command.json",
        {
            "status": "running",
            "pid": 1234,
            "started_at": "2026-04-02T08:00:00+00:00",
            "last_poll_at": "2026-04-02T08:01:00+00:00",
            "poll_interval_seconds": 5,
        },
    )

    index = {
        "candidates": [
            {"candidate_id": "cand_0001"},
            {"candidate_id": "cand_0002"},
            {"candidate_id": "cand_0003"},
        ]
    }
    state = {"active_candidate_id": "", "last_candidate_id": "cand_0003"}

    candidate_id, payload = _latest_live_command_artifact(candidates_dir, index, state)

    assert candidate_id == "cand_0002"
    assert payload["status"] == "running"
    assert payload["pid"] == 1234


def test_render_big_bang_refreshes_code_change_and_autonomous_gates(tmp_path, monkeypatch):
    repo_dir = tmp_path / "repo"
    candidates_dir = repo_dir / "artifacts" / "candidates"
    memory_dir = repo_dir / "artifacts" / "memory"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)
    (candidates_dir / "cand_0001" / "traces").mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "candidate_index.json", {"candidate_count": 1, "candidates": [{"candidate_id": "cand_0001"}]})

    calls: list[str] = []

    def record(name: str):
        def _inner(*args, **kwargs):
            calls.append(name)
            if name == "write_code_change_gate":
                write_json(memory_dir / "code_change_gate.json", {"summary": "gate"})
            if name == "write_autonomous_mutation_gate":
                write_json(memory_dir / "autonomous_mutation_gate.json", {"summary": "auto"})
            if name == "write_code_change_brief":
                write_json(memory_dir / "code_change_brief.json", {"decision_state": "issue"})
            if name == "write_mutation_brief":
                write_json(memory_dir / "mutation_brief.json", {"recommended_action": "targeted_mutation"})
            return memory_dir / f"{name}.json"

        return _inner

    monkeypatch.setattr(big_bang, "write_hindsight", record("write_hindsight"))
    monkeypatch.setattr(big_bang, "write_backend_profile", record("write_backend_profile"))
    monkeypatch.setattr(big_bang, "write_policy", record("write_policy"))
    monkeypatch.setattr(big_bang, "write_human_feedback", record("write_human_feedback"))
    monkeypatch.setattr(big_bang, "write_mutation_brief", record("write_mutation_brief"))
    monkeypatch.setattr(big_bang, "write_code_change_brief", record("write_code_change_brief"))
    monkeypatch.setattr(big_bang, "write_code_change_gate", record("write_code_change_gate"))
    monkeypatch.setattr(big_bang, "write_autonomous_mutation_gate", record("write_autonomous_mutation_gate"))
    monkeypatch.setattr(big_bang, "write_budget", record("write_budget"))
    monkeypatch.setattr(big_bang, "write_diversity", record("write_diversity"))
    monkeypatch.setattr(big_bang, "write_backend_code_map", record("write_backend_code_map"))
    monkeypatch.setattr(big_bang, "render_next_change_markdown", record("render_next_change_markdown"))
    monkeypatch.setattr(big_bang, "render_code_change_markdown", record("render_code_change_markdown"))
    monkeypatch.setattr(big_bang, "read_external_review", lambda _: {})
    monkeypatch.setattr(big_bang, "read_human_feedback", lambda _: {"items": []})
    monkeypatch.setattr(big_bang, "read_human_feedback_responses", lambda _: {"responses": []})

    import harness_lab.memory as memory_mod

    monkeypatch.setattr(memory_mod, "write_science_summary", record("write_science_summary"))

    big_bang.render_big_bang_markdown(repo_dir, candidates_dir, memory_dir)

    assert "write_code_change_gate" in calls
    assert "write_autonomous_mutation_gate" in calls
    assert (memory_dir / "code_change_gate.json").exists()
    assert (memory_dir / "autonomous_mutation_gate.json").exists()
