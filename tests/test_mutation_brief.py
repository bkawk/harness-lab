from harness_lab.mutation_brief import (
    build_code_change_brief,
    build_mutation_brief,
    render_code_change_markdown,
    render_next_change_markdown,
)
from harness_lab.workspace import write_json


def test_mutation_brief_waits_when_post_change_sample_is_thin(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
    monkeypatch.setattr(
        "harness_lab.mutation_brief._commit_timestamp",
        lambda repo_dir, commit_sha: __import__("datetime").datetime(2026, 4, 1, 0, 0, tzinfo=__import__("datetime").timezone.utc),
    )
    write_json(memory_dir / "human_feedback.json", {"items": [{"kind": "evaluation", "summary": "Improve transfer checks.", "evidence": ["artifacts/memory/hindsight.json"], "priority": 12}], "summary": "x"})
    write_json(memory_dir / "hindsight.json", {"summary": "Repeated audit-blocked outcomes."})
    write_json(memory_dir / "policy.json", {"selection_mode": "stabilize", "summary": "Favor transfer stability."})
    write_json(memory_dir / "budget.json", {"summary": "Broaden exhausted lines."})
    write_json(memory_dir / "backend_profile.json", {"summary": "Real command backend available."})
    write_json(memory_dir / "science_summary.json", {"trend_summary": "Benchmark is outrunning audit."})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "VRAM headroom is present but not urgent.", "likely_issue": "vram_headroom"})
    write_json(memory_dir / "backend_module_summary.json", {"summary": "Recent edits are concentrated in science_eval.", "modules": [{"module": "science_eval", "attempts": 3, "avg_transfer_gap": 0.04}]})
    write_json(
        memory_dir / "candidate_index.json",
        {
            "candidates": [
                {"candidate_id": "cand_0001", "created_at": "2026-04-01T00:10:00+00:00", "benchmark_score": 0.3, "audit_score": 0.27},
                {"candidate_id": "cand_0002", "created_at": "2026-03-31T23:50:00+00:00", "benchmark_score": 0.31, "audit_score": 0.28},
            ]
        },
    )

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["target_module"] == "science_eval"
    assert payload["recommended_action"] == "wait"
    assert payload["last_structural_commit"] == "abc123"
    assert payload["scored_candidates_since_change"] == 1
    assert payload["problem_statement"] == "Improve transfer checks."
    assert "VRAM headroom is present" in payload["module_rationale"]
    assert "only 1 scored candidate" in payload["summary"].lower()
    assert payload["options"][1]["recommended"] is True
    assert any(item["kind"] == "wait" for item in payload["options"])


def test_render_next_change_markdown_writes_wait_option(tmp_path):
    repo_dir = tmp_path
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "summary": "Current priority is `evaluation`.",
            "recommended_action": "targeted_mutation",
            "target_module": "science_eval",
            "problem_statement": "Improve transfer checks.",
            "module_rationale": "Recent edits concentrate in science_eval. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.",
            "science_debug_summary": "VRAM headroom is present but not urgent.",
            "supporting_evidence": ["artifacts/memory/hindsight.json"],
            "guardrails": ["This brief does not authorize or trigger code changes by itself."],
            "verification_plan": ["Run focused tests."],
            "options": [
                {"title": "Mutate science_eval", "why": "Recent edits concentrate there.", "recommended": True},
                {"title": "Wait for more data", "why": "Need more scored candidates.", "recommended": False},
            ],
        },
    )

    path = render_next_change_markdown(repo_dir, memory_dir)
    text = path.read_text(encoding="utf-8")

    assert "Wait for more data" in text
    assert "## Why This Module" in text
    assert "## Secondary Context" in text
    assert "does not authorize or trigger code changes" in text


def test_build_code_change_brief_uses_code_context(tmp_path):
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "summary": "Current priority is `evaluation`.",
            "recommended_action": "targeted_mutation",
            "target_module": "science_loss",
            "problem_statement": "Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.",
            "module_rationale": "Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust.",
            "supporting_evidence": ["artifacts/memory/hindsight.json"],
            "verification_plan": ["Run focused tests for the target module and adjacent seams."],
            "options": [
                {"kind": "targeted_mutation", "title": "Mutate science_loss", "why": "x", "recommended": True},
                {"kind": "wait", "title": "Wait on broad mutation", "why": "Need more scored candidates.", "recommended": False},
            ],
        },
    )
    write_json(
        memory_dir / "backend_code_map.json",
        {
            "summary": "Backend code context is available.",
            "modules": [
                {
                    "module": "science_loss",
                    "file": "src/harness_lab/science_loss.py",
                    "purpose": "Loss seam.",
                    "key_functions": ["compute_instance_loss", "compute_loss"],
                    "levered_surfaces": ["boundary_loss_weight", "instance_margin"],
                    "fixed_surfaces": ["Loss recipe"],
                }
            ],
            "failure_to_code_hints": [
                {
                    "failure_mode": "boundary_smoke:gap_too_wide",
                    "likely_modules": ["science_eval", "science_loss"],
                    "why": "Boundary failures often reflect weak loss pressure or strict eval thresholds.",
                }
            ],
        },
    )

    payload = build_code_change_brief(memory_dir)

    assert payload["target_module"] == "science_loss"
    assert payload["target_file"] == "src/harness_lab/science_loss.py"
    assert "compute_loss" in payload["target_functions"]
    assert "stronger transfer-sensitive loss pressure" in payload["code_hypothesis"]
    assert "boundary_loss_weight" in payload["proposed_change"]
    assert payload["failure_to_code_hint"]["failure_mode"] == "boundary_smoke:gap_too_wide"
    assert "Add, remove, or refactor code" in payload["execution_contract"]["allowed_actions"][0]
    assert "Do not silently roll back" in payload["execution_contract"]["failure_behavior"][2]
    assert payload["wait_option"]["title"] == "Wait on broad mutation"
    assert "science_loss" not in payload["target_file"] or payload["proposed_change"]


def test_render_code_change_markdown_writes_concrete_sections(tmp_path):
    repo_dir = tmp_path
    memory_dir = tmp_path / "artifacts" / "memory"
    memory_dir.mkdir(parents=True)
    write_json(
        memory_dir / "code_change_brief.json",
        {
            "summary": "Current priority is `evaluation`.",
            "recommended_action": "wait",
            "target_module": "science_loss",
            "target_file": "src/harness_lab/science_loss.py",
            "target_functions": ["compute_instance_loss", "compute_loss"],
            "problem_statement": "Improve transfer stability.",
            "why_this_module": "Boundary failures point here.",
            "code_hypothesis": "The current transfer problem is more likely to improve through stronger transfer-sensitive loss pressure than through changing evaluation thresholds alone.",
            "proposed_change": "Adjust transfer-sensitive loss pressure in a bounded way.",
            "execution_contract": {
                "allowed_actions": ["Add, remove, or refactor code within the target module."],
                "scope_limits": ["Keep the write scope to the target module plus adjacent focused tests."],
                "failure_behavior": ["Abort the attempt if compile checks or focused tests fail."],
            },
            "do_not_change": ["Do not change science_eval thresholds in the same patch."],
            "acceptance_checks": ["The loss change remains bounded."],
            "focused_tests": ["tests/test_science_loss.py"],
            "verification_plan": ["Run focused tests."],
            "abort_conditions": ["Abort if the patch spreads into unrelated modules."],
            "wait_option": {"title": "Wait on broad mutation", "why": "Need more scored candidates."},
            "supporting_evidence": ["artifacts/memory/hindsight.json", "src/harness_lab/science_loss.py"],
            "note": "Review only.",
        },
    )

    path = render_code_change_markdown(repo_dir, memory_dir)
    text = path.read_text(encoding="utf-8")

    assert "# Code Change Brief" in text
    assert "## Target Functions" in text
    assert "## Code Hypothesis" in text
    assert "## Execution Contract" in text
    assert "## Failure Behavior" in text
    assert "src/harness_lab/science_loss.py" in text
    assert "Wait on broad mutation" in text


def test_mutation_brief_recommends_mutation_after_enough_post_change_signal(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
    monkeypatch.setattr(
        "harness_lab.mutation_brief._commit_timestamp",
        lambda repo_dir, commit_sha: __import__("datetime").datetime(2026, 4, 1, 0, 0, tzinfo=__import__("datetime").timezone.utc),
    )
    write_json(memory_dir / "human_feedback.json", {"items": [{"kind": "evaluation", "summary": "Improve transfer checks.", "priority": 12}], "summary": "x"})
    write_json(memory_dir / "hindsight.json", {"summary": "Repeated audit-blocked outcomes."})
    write_json(memory_dir / "policy.json", {"selection_mode": "stabilize", "summary": "Favor transfer stability."})
    write_json(memory_dir / "budget.json", {"summary": "Broaden exhausted lines."})
    write_json(memory_dir / "backend_profile.json", {"summary": "Real command backend available."})
    write_json(memory_dir / "science_summary.json", {"trend_summary": "Benchmark is outrunning audit."})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "No dominant runtime issue.", "likely_issue": ""})
    write_json(memory_dir / "backend_module_summary.json", {"modules": [{"module": "science_eval", "attempts": 3, "avg_transfer_gap": 0.04}]})
    write_json(
        memory_dir / "candidate_index.json",
        {
            "candidates": [
                {"candidate_id": "cand_0001", "created_at": "2026-04-01T00:01:00+00:00", "benchmark_score": 0.3, "audit_score": 0.27},
                {"candidate_id": "cand_0002", "created_at": "2026-04-01T00:02:00+00:00", "benchmark_score": 0.31, "audit_score": 0.28},
                {"candidate_id": "cand_0003", "created_at": "2026-04-01T00:03:00+00:00", "benchmark_score": 0.29, "audit_score": 0.26},
            ]
        },
    )

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["recommended_action"] == "targeted_mutation"
    assert payload["last_structural_commit"] == "abc123"
    assert payload["scored_candidates_since_change"] == 3
    assert payload["options"][0]["recommended"] is True
    assert payload["options"][1]["recommended"] is False


def test_mutation_brief_targets_science_loss_for_boundary_failure_modes(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
    monkeypatch.setattr(
        "harness_lab.mutation_brief._commit_timestamp",
        lambda repo_dir, commit_sha: __import__("datetime").datetime(2026, 4, 1, 0, 0, tzinfo=__import__("datetime").timezone.utc),
    )
    write_json(memory_dir / "human_feedback.json", {"items": [{"kind": "evaluation", "summary": "Improve transfer checks.", "priority": 12}], "summary": "x"})
    write_json(
        memory_dir / "hindsight.json",
        {
            "summary": "Boundary transfer is failing.",
            "recent_top_failure_modes": [{"label": "boundary_smoke:gap_too_wide", "count": 3}],
            "policy_adjustments": [],
        },
    )
    write_json(memory_dir / "policy.json", {"selection_mode": "stabilize", "summary": "Favor transfer stability."})
    write_json(memory_dir / "budget.json", {"summary": "Broaden exhausted lines."})
    write_json(memory_dir / "backend_profile.json", {"summary": "Real command backend available."})
    write_json(memory_dir / "science_summary.json", {"trend_summary": "Benchmark is outrunning audit."})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "No dominant runtime issue.", "likely_issue": ""})
    write_json(memory_dir / "backend_module_summary.json", {"modules": [{"module": "science_model", "attempts": 3, "avg_transfer_gap": 0.04}]})
    write_json(
        memory_dir / "candidate_index.json",
        {
            "candidates": [
                {"candidate_id": "cand_0001", "created_at": "2026-04-01T00:01:00+00:00", "benchmark_score": 0.3, "audit_score": 0.27},
                {"candidate_id": "cand_0002", "created_at": "2026-04-01T00:02:00+00:00", "benchmark_score": 0.31, "audit_score": 0.28},
                {"candidate_id": "cand_0003", "created_at": "2026-04-01T00:03:00+00:00", "benchmark_score": 0.29, "audit_score": 0.26},
            ]
        },
    )

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["target_module"] == "science_loss"
    assert "boundary-transfer specific" in payload["module_rationale"]


def test_mutation_brief_targets_science_train_for_vram_headroom(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
    monkeypatch.setattr(
        "harness_lab.mutation_brief._commit_timestamp",
        lambda repo_dir, commit_sha: __import__("datetime").datetime(2026, 4, 1, 0, 0, tzinfo=__import__("datetime").timezone.utc),
    )
    write_json(
        memory_dir / "human_feedback.json",
        {"items": [{"kind": "vram_headroom", "summary": "Use more VRAM.", "priority": 5}], "summary": "x"},
    )
    write_json(memory_dir / "hindsight.json", {"summary": "VRAM headroom remains large.", "policy_adjustments": []})
    write_json(memory_dir / "policy.json", {"selection_mode": "stabilize", "summary": "Favor transfer stability."})
    write_json(memory_dir / "budget.json", {"summary": "Broaden exhausted lines."})
    write_json(memory_dir / "backend_profile.json", {"summary": "Real command backend available."})
    write_json(memory_dir / "science_summary.json", {"trend_summary": "Benchmark is outrunning audit."})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "VRAM headroom is present.", "likely_issue": "vram_headroom"})
    write_json(memory_dir / "backend_module_summary.json", {"modules": [{"module": "science_model", "attempts": 3, "avg_transfer_gap": 0.04}]})
    write_json(memory_dir / "candidate_index.json", {"candidates": []})

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["target_module"] == "science_train"
    assert "favor explicit train-capacity moves first" in payload["module_rationale"]


def test_mutation_brief_vram_headroom_overrides_boundary_failure_target(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
    monkeypatch.setattr(
        "harness_lab.mutation_brief._commit_timestamp",
        lambda repo_dir, commit_sha: __import__("datetime").datetime(2026, 4, 1, 0, 0, tzinfo=__import__("datetime").timezone.utc),
    )
    write_json(
        memory_dir / "human_feedback.json",
        {"items": [{"kind": "vram_headroom", "summary": "Use more VRAM.", "priority": 5}], "summary": "x"},
    )
    write_json(
        memory_dir / "hindsight.json",
        {
            "summary": "Boundary failures are present, but the live human ask is VRAM headroom.",
            "policy_adjustments": [],
            "recent_top_failure_modes": [{"label": "boundary_smoke:gap_too_wide", "count": 4}],
        },
    )
    write_json(memory_dir / "policy.json", {"selection_mode": "stabilize", "summary": "Favor transfer stability."})
    write_json(memory_dir / "budget.json", {"summary": "Broaden exhausted lines."})
    write_json(memory_dir / "backend_profile.json", {"summary": "Real command backend available."})
    write_json(memory_dir / "science_summary.json", {"trend_summary": "Benchmark is outrunning audit."})
    write_json(memory_dir / "science_debug_summary.json", {"summary": "VRAM headroom is present.", "likely_issue": "vram_headroom"})
    write_json(memory_dir / "backend_module_summary.json", {"modules": [{"module": "science_loss", "attempts": 5, "avg_transfer_gap": 0.05}]})
    write_json(memory_dir / "candidate_index.json", {"candidates": []})

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["target_module"] == "science_train"
    assert "Start with batch_size and eval_batch_size" in payload["module_rationale"]
