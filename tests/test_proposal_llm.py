from __future__ import annotations

from harness_lab import proposal as proposal_module
from harness_lab.workspace import create_candidate_workspace, write_json


def _seed_parent(tmp_path):
    candidates_dir = tmp_path / "candidates"
    memory_dir = tmp_path / "memory"
    candidates_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)

    parent = create_candidate_workspace(candidates_dir, "cand_0001")
    write_json(
        parent.diagnosis_path,
        {
            "candidate_id": "cand_0001",
            "created_at": parent.created_at,
            "status": "complete",
            "summary": "Parent drifted toward weak transfer.",
            "severity": "medium",
            "mechanism": "transfer_guard",
            "failure_modes": ["audit_blocked"],
            "evidence": [],
            "counterfactuals": ["Try a smaller transfer-stability follow-up."],
        },
    )
    write_json(
        memory_dir / "candidate_index.json",
        {
            "candidate_count": 1,
            "candidates": [
                {
                    "candidate_id": "cand_0001",
                    "diagnosis_mechanism": "transfer_guard",
                    "expected_failure_mode": "audit_blocked",
                    "harness_component": "transfer_guard",
                    "benchmark_score": 0.31,
                    "audit_score": 0.27,
                    "backend_fingerprints": ["fusion_changed"],
                }
            ],
            "failure_mode_counts": {"audit_blocked": 1},
            "diagnosis_mechanism_counts": {"transfer_guard": 1},
            "backend_fingerprint_counts": {"fusion_changed": 1},
        },
    )
    write_json(memory_dir / "science_summary.json", {"trend_summary": "", "leaders": {}, "recent_trend": {}})
    return candidates_dir, memory_dir


def test_llm_proposal_can_author_draft(tmp_path, monkeypatch):
    candidates_dir, _memory_dir = _seed_parent(tmp_path)
    monkeypatch.setenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "1")
    monkeypatch.setattr(
        proposal_module,
        "run_claude_json",
        lambda prompt, *, cwd: {
            "rationale": "Claude wants a tighter transfer-stability follow-up.",
            "target": {
                "harness_component": "transfer_guard",
                "expected_failure_mode": "audit_blocked",
                "novelty_basis": "test a narrower transfer guard around the parent failure",
            },
            "changes": [
                {
                    "kind": "llm_priority",
                    "mechanism": "transfer_guard",
                    "summary": "Favor a smaller transfer-stability move instead of a broad architecture jump.",
                }
            ],
            "backend_levers": {
                "science_model": {"hidden_dim": 160, "k_neighbors": 10},
                "science_eval": {"transfer_smoke_max_gap": 0.025},
            },
        },
    )
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "balanced", "summary": ""})
    monkeypatch.setattr(proposal_module, "read_budget", lambda memory_dir: {"exploration_mode": "balanced", "mechanism_budgets": []})
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": False})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})
    seen = {}

    def fake_run(prompt, *, cwd):
        seen["prompt"] = prompt
        return {
            "rationale": "Claude wants a tighter transfer-stability follow-up.",
            "target": {
                "harness_component": "transfer_guard",
                "expected_failure_mode": "audit_blocked",
                "novelty_basis": "test a narrower transfer guard around the parent failure",
            },
            "changes": [
                {
                    "kind": "llm_priority",
                    "mechanism": "transfer_guard",
                    "summary": "Favor a smaller transfer-stability move instead of a broad architecture jump.",
                }
            ],
            "backend_levers": {
                "science_model": {"hidden_dim": 160, "k_neighbors": 10},
                "science_eval": {"transfer_smoke_max_gap": 0.025},
            },
        }

    monkeypatch.setattr(proposal_module, "run_claude_json", fake_run)

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")
    assert draft.rationale == "Claude wants a tighter transfer-stability follow-up."
    assert draft.target["harness_component"] == "transfer_guard"
    assert draft.changes[0]["kind"] == "llm_priority"
    assert draft.backend_levers["science_model"]["hidden_dim"] == 160
    assert draft.backend_levers["science_eval"]["transfer_smoke_max_gap"] == 0.025
    assert "backend_lever_catalog" in seen["prompt"]
    assert "returning empty backend_levers is discouraged" in seen["prompt"]
    assert "Good examples" in seen["prompt"]


def test_invalid_llm_proposal_falls_back_to_heuristic(tmp_path, monkeypatch):
    candidates_dir, _memory_dir = _seed_parent(tmp_path)
    monkeypatch.setenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "1")
    monkeypatch.setattr(proposal_module, "run_claude_json", lambda prompt, *, cwd: {"changes": []})
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "balanced", "summary": ""})
    monkeypatch.setattr(proposal_module, "read_budget", lambda memory_dir: {"exploration_mode": "balanced", "mechanism_budgets": []})
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": False})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")
    assert "Parent drifted toward weak transfer." in draft.rationale
    assert any(change["kind"] == "counterfactual" for change in draft.changes)


def test_mutation_brief_target_overrides_broad_parent_target(tmp_path, monkeypatch):
    candidates_dir, memory_dir = _seed_parent(tmp_path)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "recommended_action": "wait",
            "target_module": "science_model",
        },
    )
    monkeypatch.delenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", raising=False)
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "balanced", "summary": ""})
    monkeypatch.setattr(proposal_module, "read_budget", lambda memory_dir: {"exploration_mode": "balanced", "mechanism_budgets": []})
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": False})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")

    assert draft.target["harness_component"] == "science_model"
    assert draft.memory_context["mutation_brief_target"] == "science_model"
    assert any(change["kind"] == "mutation_brief_focus" for change in draft.changes)


def test_wait_gate_allows_small_targeted_lever_nudges(tmp_path, monkeypatch):
    candidates_dir, memory_dir = _seed_parent(tmp_path)
    write_json(
        memory_dir / 'mutation_brief.json',
        {'recommended_action': 'wait', 'target_module': 'science_model', 'summary': 'wait'},
    )
    monkeypatch.setenv('HARNESS_LAB_LLM_PROPOSAL_ENABLED', '1')
    monkeypatch.setattr(proposal_module, 'choose_best_prepared_dataset', lambda memory_dir: {'dataset_id': 'abc_boundary512_v64'})
    monkeypatch.setattr(proposal_module, 'get_dataset_record', lambda memory_dir, dataset_id: {'dataset_id': dataset_id, 'status': 'ready'})
    monkeypatch.setattr(proposal_module, 'read_hardware_profile', lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, 'read_hindsight', lambda memory_dir: {'summary': '', 'policy_adjustments': [], 'over_explored_mechanisms': [], 'under_explored_promising_mechanisms': [], 'over_explored_backend_fingerprints': [], 'under_explored_backend_fingerprints': []})
    monkeypatch.setattr(proposal_module, 'read_policy', lambda memory_dir: {'selection_mode': 'balanced', 'summary': ''})
    monkeypatch.setattr(proposal_module, 'read_budget', lambda memory_dir: {'exploration_mode': 'balanced', 'mechanism_budgets': []})
    monkeypatch.setattr(proposal_module, 'read_diversity', lambda memory_dir: {'novelty_step_recommended': False})
    monkeypatch.setattr(proposal_module, 'read_external_review', lambda memory_dir: {'status': 'idle', 'review_requested': False})
    monkeypatch.setattr(proposal_module, 'synthesize_parent_candidates', lambda candidates_dir: {'top_parent_id': 'cand_0001', 'ranked_parents': [{'candidate_id': 'cand_0001'}]})
    monkeypatch.setattr(
        proposal_module,
        'run_claude_json',
        lambda prompt, *, cwd: {
            'rationale': 'Try small model nudges.',
            'target': {'harness_component': 'science_model', 'expected_failure_mode': 'audit_blocked', 'novelty_basis': 'small lever move'},
            'changes': [{'kind': 'llm_priority', 'mechanism': 'science_model', 'summary': 'Use small model lever nudges.'}],
            'backend_levers': {
                'science_model': {'hidden_dim': 160, 'k_neighbors': 10, 'global_dim': 256},
                'science_eval': {'transfer_smoke_max_gap': 0.02},
            },
        },
    )

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, 'cand_0002')

    assert draft.backend_levers == {'science_model': {'hidden_dim': 160, 'k_neighbors': 10}}


def test_llm_prompt_suppresses_conflicting_broaden_signals_for_target_module(tmp_path, monkeypatch):
    candidates_dir, memory_dir = _seed_parent(tmp_path)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "recommended_action": "wait",
            "target_module": "science_model",
            "summary": "wait",
        },
    )
    monkeypatch.setenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "1")
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "balanced", "summary": ""})
    monkeypatch.setattr(
        proposal_module,
        "read_budget",
        lambda memory_dir: {
            "exploration_mode": "force_broad_exploration",
            "mechanism_budgets": [{"mechanism": "transfer_guard", "exhausted": True, "remaining_followups": 0}],
        },
    )
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": True, "current_mechanism_streak": 6})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})
    seen = {}

    def fake_run(prompt, *, cwd):
        seen["prompt"] = prompt
        return {
            "rationale": "Try a small science_model lever nudge.",
            "target": {"harness_component": "science_model", "expected_failure_mode": "audit_blocked", "novelty_basis": "small lever move"},
            "changes": [{"kind": "llm_priority", "mechanism": "science_model", "summary": "Use a small model lever nudge."}],
            "backend_levers": {"science_model": {"hidden_dim": 160}},
        }

    monkeypatch.setattr(proposal_module, "run_claude_json", fake_run)

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")

    assert draft.backend_levers == {"science_model": {"hidden_dim": 160}}
    assert "force broader exploration" not in seen["prompt"]
    assert "novelty step" not in seen["prompt"]
    assert "science_model" in seen["prompt"]


def test_llm_retries_when_targeted_module_has_empty_levers_without_reason(tmp_path, monkeypatch):
    candidates_dir, memory_dir = _seed_parent(tmp_path)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "target_module": "science_model",
            "summary": "act",
        },
    )
    monkeypatch.setenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "1")
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "stabilize", "summary": ""})
    monkeypatch.setattr(proposal_module, "read_budget", lambda memory_dir: {"exploration_mode": "balanced", "mechanism_budgets": []})
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": False})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})
    seen_prompts = []
    payloads = iter(
        [
            {
                "rationale": "Try a small science_model move.",
                "target": {"harness_component": "science_model", "expected_failure_mode": "audit_blocked", "novelty_basis": "small lever move"},
                "changes": [{"kind": "llm_priority", "mechanism": "science_model", "summary": "Try a small model nudge."}],
                "backend_levers": {},
            },
            {
                "rationale": "Try a small science_model move.",
                "target": {"harness_component": "science_model", "expected_failure_mode": "audit_blocked", "novelty_basis": "small lever move"},
                "changes": [{"kind": "llm_priority", "mechanism": "science_model", "summary": "Try a small model nudge."}],
                "backend_levers": {"science_model": {"hidden_dim": 160}},
            },
        ]
    )

    def fake_run(prompt, *, cwd):
        seen_prompts.append(prompt)
        return next(payloads)

    monkeypatch.setattr(proposal_module, "run_claude_json", fake_run)

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")

    assert draft.backend_levers == {"science_model": {"hidden_dim": 160}}
    assert len(seen_prompts) == 2
    assert "Do not leave both `backend_levers` and `no_lever_reason` empty." in seen_prompts[-1]


def test_llm_does_not_retry_when_empty_levers_have_good_reason(tmp_path, monkeypatch):
    candidates_dir, memory_dir = _seed_parent(tmp_path)
    write_json(
        memory_dir / "mutation_brief.json",
        {
            "recommended_action": "targeted_mutation",
            "target_module": "science_model",
            "summary": "act",
        },
    )
    monkeypatch.setenv("HARNESS_LAB_LLM_PROPOSAL_ENABLED", "1")
    monkeypatch.setattr(proposal_module, "choose_best_prepared_dataset", lambda memory_dir: {"dataset_id": "abc_boundary512_v64"})
    monkeypatch.setattr(proposal_module, "get_dataset_record", lambda memory_dir, dataset_id: {"dataset_id": dataset_id, "status": "ready"})
    monkeypatch.setattr(proposal_module, "read_hardware_profile", lambda memory_dir: {})
    monkeypatch.setattr(proposal_module, "read_hindsight", lambda memory_dir: {"summary": "", "policy_adjustments": [], "over_explored_mechanisms": [], "under_explored_promising_mechanisms": [], "over_explored_backend_fingerprints": [], "under_explored_backend_fingerprints": []})
    monkeypatch.setattr(proposal_module, "read_policy", lambda memory_dir: {"selection_mode": "stabilize", "summary": ""})
    monkeypatch.setattr(proposal_module, "read_budget", lambda memory_dir: {"exploration_mode": "balanced", "mechanism_budgets": []})
    monkeypatch.setattr(proposal_module, "read_diversity", lambda memory_dir: {"novelty_step_recommended": False})
    monkeypatch.setattr(proposal_module, "read_external_review", lambda memory_dir: {"status": "idle", "review_requested": False})
    monkeypatch.setattr(proposal_module, "synthesize_parent_candidates", lambda candidates_dir: {"top_parent_id": "cand_0001", "ranked_parents": [{"candidate_id": "cand_0001"}]})
    seen_prompts = []

    def fake_run(prompt, *, cwd):
        seen_prompts.append(prompt)
        return {
            "rationale": "Hold steady on explicit levers for one more scored result.",
            "target": {"harness_component": "science_model", "expected_failure_mode": "audit_blocked", "novelty_basis": "wait for one more scored result"},
            "changes": [{"kind": "llm_priority", "mechanism": "science_model", "summary": "Hold explicit levers steady for one more scored result."}],
            "backend_levers": {},
            "no_lever_reason": "The recent targeted-mutation window is still narrow, so one more scored candidate would make the next explicit lever move less noisy.",
        }

    monkeypatch.setattr(proposal_module, "run_claude_json", fake_run)

    draft = proposal_module.draft_proposal_for_candidate(candidates_dir, "cand_0002")

    assert draft.backend_levers == {}
    assert len(seen_prompts) == 1
