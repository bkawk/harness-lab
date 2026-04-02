from __future__ import annotations

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
