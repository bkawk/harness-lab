"""Tests for bounded external review fallback, including optional Claude review."""
from __future__ import annotations

from harness_lab.external_review import (
    _heuristic_review_payload,
    maybe_request_external_review,
)
from harness_lab import external_review as external_review_module
from harness_lab.workspace import write_json


class TestExternalReviewFallbackChain:
    def _setup_review_env(self, tmp_path, *, candidate_count=10):
        candidates_dir = tmp_path / "candidates"
        candidates_dir.mkdir(parents=True, exist_ok=True)
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)

        candidates = [
            {"candidate_id": f"cand_{i:04d}", "outcome_label": "dead_end"}
            for i in range(candidate_count)
        ]
        write_json(memory_dir / "candidate_index.json", {
            "candidate_count": candidate_count,
            "candidates": candidates,
            "outcome_label_counts": {"dead_end": candidate_count},
            "failure_mode_counts": {},
            "diagnosis_mechanism_counts": {},
        })
        write_json(memory_dir / "hindsight.json", {
            "candidate_count": candidate_count,
            "summary": "",
            "hindsight_findings": [],
            "policy_adjustments": [],
            "top_outcomes": [{"label": "dead_end", "count": candidate_count}],
            "top_failure_modes": [],
            "over_explored_mechanisms": [],
            "under_explored_promising_mechanisms": [],
            "over_explored_backend_fingerprints": [],
            "under_explored_backend_fingerprints": [],
            "mechanism_stats": [],
            "backend_fingerprint_stats": [],
            "process_classification_counts": {},
            "throughput_summary": {},
        })
        return candidates_dir, memory_dir

    def test_heuristic_fallback_works(self, tmp_path, monkeypatch):
        monkeypatch.delenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", raising=False)
        candidates_dir, memory_dir = self._setup_review_env(tmp_path)
        result = maybe_request_external_review(candidates_dir, memory_dir, force=True)
        assert result["status"] == "reviewed"
        assert result["reviewer"] == "heuristic"
        assert result["trigger_reason"] == "forced_review"
        assert isinstance(result["lab_advice"], list)
        assert isinstance(result["human_advice"], list)

    def test_dead_end_streak_triggers_review(self, tmp_path, monkeypatch):
        monkeypatch.delenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", raising=False)
        candidates_dir, memory_dir = self._setup_review_env(tmp_path)
        result = maybe_request_external_review(candidates_dir, memory_dir)
        assert result["status"] == "reviewed"
        assert result["trigger_reason"] == "dead_end_streak"
        assert any(a["kind"] == "direction" for a in result["lab_advice"])

    def test_command_reviewer_takes_priority(self, tmp_path, monkeypatch):
        """When HARNESS_LAB_EXTERNAL_REVIEW_COMMAND is set but fails, falls back to heuristic."""
        monkeypatch.setenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", "false")  # will exit 1
        candidates_dir, memory_dir = self._setup_review_env(tmp_path)
        result = maybe_request_external_review(candidates_dir, memory_dir, force=True)
        # Command fails, so falls back to heuristic
        assert result["reviewer"] == "heuristic"

    def test_llm_reviewer_takes_priority_when_enabled(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HARNESS_LAB_LLM_REVIEW_ENABLED", "1")
        monkeypatch.delenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", raising=False)
        candidates_dir, memory_dir = self._setup_review_env(tmp_path)
        monkeypatch.setattr(
            external_review_module,
            "run_claude_json",
            lambda prompt, *, cwd: {
                "situation_summary": "Claude review fired.",
                "lab_advice": [{"kind": "direction", "summary": "Try a different backend line."}],
                "human_advice": [{"kind": "seed_backend_strength", "summary": "Strengthen the seed backend."}],
                "confidence": 0.82,
                "evidence_used": ["artifacts/memory/candidate_index.json"],
            },
        )
        result = maybe_request_external_review(candidates_dir, memory_dir, force=True)
        assert result["status"] == "reviewed"
        assert result["reviewer"] == "claude"
        assert result["situation_summary"] == "Claude review fired."
        assert result["confidence"] == 0.82

    def test_llm_review_falls_back_to_heuristic_on_invalid_payload(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HARNESS_LAB_LLM_REVIEW_ENABLED", "1")
        monkeypatch.delenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", raising=False)
        candidates_dir, memory_dir = self._setup_review_env(tmp_path)
        monkeypatch.setattr(external_review_module, "run_claude_json", lambda prompt, *, cwd: {"lab_advice": []})
        result = maybe_request_external_review(candidates_dir, memory_dir, force=True)
        assert result["status"] == "reviewed"
        assert result["reviewer"] == "heuristic"

    def test_idle_when_no_trigger(self, tmp_path, monkeypatch):
        monkeypatch.delenv("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", raising=False)
        candidates_dir, memory_dir = self._setup_review_env(tmp_path, candidate_count=2)
        # Only 2 candidates, no streaks => idle
        # Override candidates to have mixed outcomes
        write_json(memory_dir / "candidate_index.json", {
            "candidate_count": 2,
            "candidates": [
                {"candidate_id": "cand_0000", "outcome_label": "keeper"},
                {"candidate_id": "cand_0001", "outcome_label": "dead_end"},
            ],
            "outcome_label_counts": {"keeper": 1, "dead_end": 1},
            "failure_mode_counts": {},
            "diagnosis_mechanism_counts": {},
        })
        result = maybe_request_external_review(candidates_dir, memory_dir)
        assert result["status"] == "idle"
