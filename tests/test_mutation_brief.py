from harness_lab.mutation_brief import build_mutation_brief, render_next_change_markdown
from harness_lab.workspace import write_json


def test_mutation_brief_waits_when_post_change_sample_is_thin(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
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
                {"candidate_id": "cand_0001", "source_commit": "abc123", "benchmark_score": 0.3, "audit_score": 0.27},
                {"candidate_id": "cand_0002", "source_commit": "older", "benchmark_score": 0.31, "audit_score": 0.28},
            ]
        },
    )

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["target_module"] == "science_eval"
    assert payload["recommended_action"] == "wait"
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


def test_mutation_brief_recommends_mutation_after_enough_post_change_signal(tmp_path, monkeypatch):
    memory_dir = tmp_path / "artifacts" / "memory"
    candidates_dir = tmp_path / "artifacts" / "candidates"
    memory_dir.mkdir(parents=True)
    candidates_dir.mkdir(parents=True)
    monkeypatch.setattr("harness_lab.mutation_brief._last_structural_commit", lambda repo_dir: "abc123")
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
                {"candidate_id": "cand_0001", "source_commit": "abc123", "benchmark_score": 0.3, "audit_score": 0.27},
                {"candidate_id": "cand_0002", "source_commit": "abc123", "benchmark_score": 0.31, "audit_score": 0.28},
                {"candidate_id": "cand_0003", "source_commit": "abc123", "benchmark_score": 0.29, "audit_score": 0.26},
                {"candidate_id": "cand_0004", "source_commit": "abc123", "benchmark_score": 0.32, "audit_score": 0.29},
                {"candidate_id": "cand_0005", "source_commit": "abc123", "benchmark_score": 0.33, "audit_score": 0.3},
            ]
        },
    )

    payload = build_mutation_brief(candidates_dir, memory_dir)

    assert payload["recommended_action"] == "targeted_mutation"
    assert payload["options"][0]["recommended"] is True
    assert payload["options"][1]["recommended"] is False
