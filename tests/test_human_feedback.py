from __future__ import annotations

from harness_lab.human_feedback import (
    build_human_feedback,
    build_human_feedback_responses,
    read_manual_human_feedback_responses,
    write_manual_human_feedback_response_template,
)
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
            "recent_scored_candidate_count": 8,
            "recent_top_outcomes": [{"label": "audit_blocked", "count": 4}],
            "recent_top_failure_modes": [{"label": "stale_process", "count": 2}],
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


def test_human_feedback_suppresses_evaluation_when_keepers_match_audit_blocked(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 20}],
            "top_failure_modes": [],
            "recent_scored_candidate_count": 8,
            "recent_top_outcomes": [
                {"label": "audit_blocked", "count": 3},
                {"label": "keeper", "count": 3},
                {"label": "dead_end", "count": 2},
            ],
            "recent_top_failure_modes": [],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": "Prioritize transfer stability."})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {"candidate_id": "cand_0455"}}})

    payload = build_human_feedback(memory_dir)
    kinds = [item["kind"] for item in payload["items"]]

    assert "evaluation" not in kinds


def test_human_feedback_lowers_priority_for_recently_addressed_requests(tmp_path, monkeypatch):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 4}],
            "top_failure_modes": [{"label": "stale_process", "count": 2}],
            "recent_scored_candidate_count": 8,
            "recent_top_outcomes": [{"label": "audit_blocked", "count": 4}],
            "recent_top_failure_modes": [{"label": "stale_process", "count": 2}],
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


def test_human_feedback_reescalates_addressed_ops_when_failures_persist(tmp_path, monkeypatch):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 2}],
            "top_failure_modes": [{"label": "startup_timeout", "count": 12}],
            "recent_scored_candidate_count": 8,
            "recent_top_outcomes": [{"label": "audit_blocked", "count": 2}],
            "recent_top_failure_modes": [{"label": "startup_timeout", "count": 12}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": ""})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {"candidate_id": "cand_0009"}}})
    monkeypatch.setattr(
        human_feedback_module,
        "read_human_feedback_responses",
        lambda memory_dir: {
            "summary": "The humans recently addressed 1 lab request(s).",
            "responses": [
                {
                    "kind": "ops",
                    "commit_sha": "a3c7559",
                    "response_summary": "Hardened backend startup and no-progress detection.",
                },
            ],
        },
    )

    payload = build_human_feedback(memory_dir)
    ops_item = next(item for item in payload["items"] if item["kind"] == "ops")
    assert ops_item["priority"] >= 9
    assert "persists after" in ops_item["why_now"]


def test_human_feedback_adds_vram_request_on_oom_pressure(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [],
            "top_failure_modes": [{"label": "cuda_oom", "count": 2}],
            "recent_scored_candidate_count": 8,
            "recent_top_outcomes": [],
            "recent_top_failure_modes": [{"label": "cuda_oom", "count": 2}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": ""})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {"candidate_id": "cand_0009"}}})

    payload = build_human_feedback(memory_dir)
    vram_item = next(item for item in payload["items"] if item["kind"] == "vram")
    assert vram_item["priority"] >= 9
    assert "memory-pressure failure" in vram_item["why_now"]


def test_human_feedback_suppresses_stale_failure_advice_when_recent_window_is_clean(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(memory_dir / "external_review.json", {"status": "idle", "human_advice": []})
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 12}],
            "top_failure_modes": [{"label": "science_backend_error", "count": 49}, {"label": "startup_timeout", "count": 33}],
            "recent_scored_candidate_count": 10,
            "recent_top_outcomes": [{"label": "audit_blocked", "count": 6}],
            "recent_top_failure_modes": [{"label": "transfer_smoke_failed", "count": 5}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": "Prioritize transfer stability."})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {"candidate_id": "cand_0209"}}})

    payload = build_human_feedback(memory_dir)
    kinds = [item["kind"] for item in payload["items"]]
    assert "evaluation" in kinds
    assert "ops" not in kinds
    assert "vram" not in kinds


def test_human_feedback_filters_stale_external_review_failure_advice(tmp_path):
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        memory_dir / "external_review.json",
        {
            "status": "reviewed",
            "trigger_reason": "exhaustion_signal",
            "confidence": 0.55,
            "evidence_used": ["artifacts/memory/candidate_index.json"],
            "human_advice": [
                {
                    "kind": "non_self_evolving",
                    "summary": "Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.",
                }
            ],
        },
    )
    write_json(
        memory_dir / "hindsight.json",
        {
            "top_outcomes": [{"label": "audit_blocked", "count": 12}],
            "top_failure_modes": [{"label": "science_backend_error", "count": 49}],
            "recent_scored_candidate_count": 10,
            "recent_top_outcomes": [{"label": "audit_blocked", "count": 6}],
            "recent_top_failure_modes": [{"label": "transfer_smoke_failed", "count": 5}],
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"summary": "Prioritize transfer stability."})
    write_json(memory_dir / "science_summary.json", {"leaders": {"best_stable": {"candidate_id": "cand_0209"}}})

    payload = build_human_feedback(memory_dir)
    assert all("science_backend_error" not in item["summary"] for item in payload["items"])


def test_human_feedback_responses_recognize_recent_eval_and_module_surface_changes(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    repo_dir = tmp_path
    monkeypatch.setattr(
        human_feedback_module,
        "_repo_dir_from_memory",
        lambda path: repo_dir,
    )
    monkeypatch.setattr(
        human_feedback_module,
        "_git_log",
        lambda repo_dir, limit=80: [
            {"commit_sha": "aaaa1111", "subject": "Refine transfer failure attribution"},
            {"commit_sha": "bbbb2222", "subject": "Make mutation targeting failure-aware"},
            {"commit_sha": "cccc3333", "subject": "Enable proposal LLM in big-bang"},
        ],
    )

    payload = build_human_feedback_responses(memory_dir)

    response_by_kind = {item["kind"]: item for item in payload["responses"]}
    assert response_by_kind["evaluation"]["commit_sha"] == "aaaa1111"
    assert response_by_kind["module_surface"]["commit_sha"] == "bbbb2222"


def test_manual_human_feedback_responses_override_commit_inference(tmp_path, monkeypatch):
    repo_dir = tmp_path
    memory_dir = repo_dir / "artifacts" / "memory"
    docs_dir = repo_dir / "docs"
    memory_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        docs_dir / "lab_responses.json",
        {
            "responses": [
                {
                    "kind": "evaluation",
                    "status": "planned",
                    "human_response": "We are watching the new failure reasons for a few more scored candidates.",
                    "next_action": "Tighten boundary smoke only if hard-transfer regressions keep leading.",
                    "updated_at": "2026-04-01T20:00:00+00:00",
                }
            ]
        },
    )
    monkeypatch.setattr(
        human_feedback_module,
        "_repo_dir_from_memory",
        lambda path: repo_dir,
    )
    monkeypatch.setattr(
        human_feedback_module,
        "_git_log",
        lambda repo_dir, limit=80: [
            {"commit_sha": "aaaa1111", "subject": "Refine transfer failure attribution"},
        ],
    )

    payload = build_human_feedback_responses(memory_dir)

    assert payload["responses"][0]["kind"] == "evaluation"
    assert payload["responses"][0]["response_source"] == "manual"
    assert payload["responses"][0]["commit_sha"] == ""
    assert "Next:" in payload["responses"][0]["response_summary"]


def test_manual_human_feedback_template_seeds_current_requests(tmp_path, monkeypatch):
    repo_dir = tmp_path
    memory_dir = repo_dir / "artifacts" / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(
        human_feedback_module,
        "_repo_dir_from_memory",
        lambda path: repo_dir,
    )

    path = write_manual_human_feedback_response_template(
        memory_dir,
        {
            "items": [
                {"kind": "evaluation"},
                {"kind": "vram_headroom"},
            ]
        },
    )
    payload = read_manual_human_feedback_responses(memory_dir)

    assert path.name == "lab_responses.json"
    raw = path.read_text(encoding="utf-8")
    assert "\"kind\": \"evaluation\"" in raw
    assert "\"kind\": \"vram_headroom\"" in raw
    assert payload["responses"] == []
