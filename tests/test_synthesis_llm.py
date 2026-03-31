from __future__ import annotations

from harness_lab import synthesis as synthesis_module


def test_llm_parent_selection_can_override_top_parent(monkeypatch):
    index = {
        "candidate_count": 2,
        "candidates": [
            {
                "candidate_id": "cand_0001",
                "outcome_label": "dead_end",
                "diagnosis_mechanism": "fusion_changed",
                "failure_modes": ["dead_end"],
                "backend_fingerprints": ["fusion_changed"],
                "benchmark_score": 0.22,
                "audit_score": 0.20,
            },
            {
                "candidate_id": "cand_0002",
                "outcome_label": "improved",
                "diagnosis_mechanism": "transfer_guard",
                "failure_modes": ["transfer_win"],
                "backend_fingerprints": ["instance_path_changed"],
                "benchmark_score": 0.31,
                "audit_score": 0.29,
            },
        ],
    }
    ranked = [
        synthesis_module.ParentCandidateScore("cand_0001", 80, ("base=80",)),
        synthesis_module.ParentCandidateScore("cand_0002", 70, ("base=70",)),
    ]
    monkeypatch.setenv("HARNESS_LAB_LLM_PARENT_SELECTION_ENABLED", "1")
    monkeypatch.setattr(
        synthesis_module,
        "run_claude_json",
        lambda prompt, *, cwd: {
            "top_parent_id": "cand_0002",
            "reasoning": "Choose the candidate with better transfer evidence.",
            "candidate_adjustments": [
                {"candidate_id": "cand_0002", "score_delta": 15, "reason": "Better transfer profile."}
            ],
        },
    )

    revised, metadata = synthesis_module._apply_llm_parent_selection(
        index,
        ranked,
        hindsight={},
        policy={},
        budget={},
        hardware_profile={},
        cwd=__import__("pathlib").Path("."),
    )

    assert revised[0].candidate_id == "cand_0002"
    assert metadata["top_parent_id"] == "cand_0002"
    assert metadata["reviewer"] == "claude"
    assert any("llm_parent_selected=1000" in reason for reason in revised[0].reasons)


def test_invalid_llm_parent_selection_keeps_heuristic_order(monkeypatch):
    index = {"candidate_count": 1, "candidates": [{"candidate_id": "cand_0001"}]}
    ranked = [synthesis_module.ParentCandidateScore("cand_0001", 50, ("base=50",))]
    monkeypatch.setenv("HARNESS_LAB_LLM_PARENT_SELECTION_ENABLED", "1")
    monkeypatch.setattr(synthesis_module, "run_claude_json", lambda prompt, *, cwd: {"top_parent_id": "cand_9999"})

    revised, metadata = synthesis_module._apply_llm_parent_selection(
        index,
        ranked,
        hindsight={},
        policy={},
        budget={},
        hardware_profile={},
        cwd=__import__("pathlib").Path("."),
    )

    assert revised[0].candidate_id == "cand_0001"
    assert metadata == {}
