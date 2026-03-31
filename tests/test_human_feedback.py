from __future__ import annotations

from harness_lab.human_feedback import build_human_feedback
from harness_lab import human_feedback as human_feedback_module
from harness_lab.workspace import write_json


def test_human_feedback_ranks_external_review_items(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        memory_dir / "external_review.json",
        {
            "status": "reviewed",
            "trigger_reason": "repeated_audit_blocked",
            "confidence": 0.81,
            "evidence_used": ["artifacts/memory/candidate_index.json"],
            "human_advice": [
                {"kind": "seed_backend", "summary": "Expose a better transfer-stability module."},
            ],
        },
    )
    write_json(memory_dir / "hindsight.json", {"top_outcomes": [], "top_failure_modes": [], "summary": "", "hindsight_findings": [], "policy_adjustments": []})
    write_json(memory_dir / "policy.json", {"summary": ""})
    write_json(memory_dir / "science_summary.json", {"leaders": {}})

    payload = build_human_feedback(memory_dir)
    assert payload["items"][0]["kind"] == "seed_backend"
    assert payload["items"][0]["source"] == "external_review"


def test_human_feedback_adds_transfer_and_ops_requests(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 4}],
            "top_failure_modes": [{"label": "stale_process", "count": 2}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": "Prioritize transfer stability."})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {}}})

    payload = build_human_feedback(memory_dir)
    kinds = [item["kind"] for item in payload["items"]]
    assert "evaluation" in kinds
    assert "ops" in kinds
    assert "dataset" in kinds


def test_human_feedback_lowers_priority_for_recently_addressed_requests(tmp_path, monkeypatch):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 4}],
            "top_failure_modes": [{"label": "stale_process", "count": 2}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": "Prioritize transfer stability."})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {}}})
    monkeypatch.setattr(
        human_feedback_module,
        "read_human_feedback_responses",
        lambda memory_dir: {
            "summary": "The humans recently addressed 2 lab request(s).",
            "responses": [
                {
                    "kind": "evaluation",
                    "commit_sha": "930a088",
                    "response_summary": "Implemented a transfer-stability smoke gate before full audit.",
                },
                {
                    "kind": "ops",
                    "commit_sha": "a3c7559",
                    "response_summary": "Hardened backend startup and no-progress detection.",
                },
                {
                    "kind": "dataset",
                    "commit_sha": "3b11024",
                    "response_summary": "Added named stratified evaluation slices.",
                },
            ],
        },
    )

    payload = build_human_feedback(memory_dir)
    items = {item["kind"]: item for item in payload["items"]}
    assert items["evaluation"]["priority"] < 12
    assert items["ops"]["priority"] < 9
    assert payload["responses"][-1]["kind"] == "dataset"
    assert payload["responses"][0]["kind"] == "evaluation"
