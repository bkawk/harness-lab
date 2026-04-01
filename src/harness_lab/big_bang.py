from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness_lab.backend import read_backend_profile, write_backend_profile
from harness_lab.budget import read_budget, write_budget
from harness_lab.diversity import read_diversity, write_diversity
from harness_lab.external_review import maybe_request_external_review, read_external_review
from harness_lab.human_feedback import (
    manual_human_feedback_responses_path,
    read_human_feedback,
    read_human_feedback_responses,
    write_human_feedback,
)
from harness_lab.hindsight import write_hindsight
from harness_lab.memory import build_candidate_index
from harness_lab.mutation_brief import render_next_change_markdown, write_mutation_brief
from harness_lab.orchestrator import GENESIS_CANDIDATE_ID, LabStepResult, next_candidate_id, run_lab_step
from harness_lab.policy import read_policy, write_policy
from harness_lab.publisher import publish_repo_snapshot
from harness_lab.workspace import write_json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def big_bang_state_path(memory_dir: Path) -> Path:
    return memory_dir / "big_bang_state.json"


def load_big_bang_state(memory_dir: Path) -> dict:
    path = big_bang_state_path(memory_dir)
    if not path.exists():
        return {
            "status": "idle",
            "vital_spark_at": "",
            "started_at": "",
            "last_heartbeat": "",
            "cycles_completed": 0,
            "last_candidate_id": "",
            "last_commit_sha": "",
            "last_dataset_id": "",
            "last_dataset_action": "",
            "last_seed_action": "",
            "last_publish_message": "",
            "last_cycle_mode": "",
            "novelty_cycles_triggered": 0,
            "active_candidate_id": "",
            "active_candidate_started_at": "",
        }
    return json.loads(path.read_text(encoding="utf-8"))


def write_big_bang_state(memory_dir: Path, payload: dict) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = big_bang_state_path(memory_dir)
    write_json(path, payload)
    return path


def update_big_bang_state(memory_dir: Path, **updates: object) -> dict:
    state = load_big_bang_state(memory_dir)
    if not state.get("vital_spark_at") and updates.get("status") == "running":
        state["vital_spark_at"] = str(updates.get("started_at") or updates.get("last_heartbeat") or utc_now())
    state.update(updates)
    write_big_bang_state(memory_dir, state)
    return state


def _read_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _has_nested_values(payload: dict) -> bool:
    return any(isinstance(value, dict) and value for value in payload.values())


def _candidate_lookup_order(index: dict, state: dict) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for candidate_id in (
        str(state.get("active_candidate_id", "") or ""),
        str(state.get("last_candidate_id", "") or ""),
    ):
        if candidate_id and candidate_id not in seen:
            ordered.append(candidate_id)
            seen.add(candidate_id)
    for item in reversed(list(index.get("candidates", []))):
        candidate_id = str(item.get("candidate_id", "") or "")
        if candidate_id and candidate_id not in seen:
            ordered.append(candidate_id)
            seen.add(candidate_id)
    return ordered


def _latest_backend_science_artifacts(candidates_dir: Path, index: dict, state: dict) -> tuple[str, dict, str, dict]:
    fallback_candidate = str(state.get("active_candidate_id", "") or state.get("last_candidate_id", "") or "")
    explicit_candidate_id = fallback_candidate
    explicit_payload: dict = {}
    effective_candidate_id = fallback_candidate
    effective_payload: dict = {}
    for candidate_id in _candidate_lookup_order(index, state):
        candidate_root = candidates_dir / candidate_id
        if not explicit_payload:
            trace_lever_payload = _read_json_file(candidate_root / "traces" / "backend_levers.json")
            proposal_payload = _read_json_file(candidate_root / "proposal.json").get("backend_levers", {})
            candidate_explicit = trace_lever_payload if _has_nested_values(trace_lever_payload) else proposal_payload
            if isinstance(candidate_explicit, dict) and _has_nested_values(candidate_explicit):
                explicit_candidate_id = candidate_id
                explicit_payload = candidate_explicit
        if not effective_payload:
            candidate_effective = _read_json_file(candidate_root / "traces" / "effective_backend_config.json")
            if candidate_effective:
                effective_candidate_id = candidate_id
                effective_payload = candidate_effective
        if explicit_payload and effective_payload:
            break
    return explicit_candidate_id, explicit_payload, effective_candidate_id, effective_payload


def render_big_bang_markdown(
    repo_dir: Path,
    candidates_dir: Path,
    memory_dir: Path,
    latest: LabStepResult | None = None,
) -> Path:
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    output_path = docs_dir / "big_bang.md"
    state = load_big_bang_state(memory_dir)
    candidate_index_path = memory_dir / "candidate_index.json"
    hindsight_path = memory_dir / "hindsight.json"
    budget_path = memory_dir / "budget.json"
    diversity_path = memory_dir / "diversity.json"
    backend_path = memory_dir / "backend_profile.json"
    science_summary_path = memory_dir / "science_summary.json"
    mutation_brief_path = memory_dir / "mutation_brief.json"
    backend_module_summary_path = memory_dir / "backend_module_summary.json"
    index = build_candidate_index(candidates_dir) if candidates_dir.exists() else {
        "candidate_count": 0,
        "candidates": [],
    }
    if candidate_index_path.exists():
        index = json.loads(candidate_index_path.read_text(encoding="utf-8"))
    hindsight = {}
    policy = {}
    budget = {}
    diversity = {}
    backend = {}
    external_review = {}
    human_feedback = {}
    human_feedback_responses = {}
    science_summary = {}
    mutation_brief = {}
    backend_module_summary = {}
    live_command = {}
    if candidates_dir.exists():
        write_hindsight(candidates_dir, hindsight_path)
        write_backend_profile(memory_dir)
        write_policy(candidates_dir, memory_dir, memory_dir / "policy.json")
        write_human_feedback(memory_dir, memory_dir / "human_feedback.json")
        write_mutation_brief(candidates_dir, memory_dir)
        write_budget(memory_dir, budget_path)
        write_diversity(candidates_dir, diversity_path)
        from harness_lab.memory import write_science_summary

        write_science_summary(candidates_dir, science_summary_path)
        render_next_change_markdown(repo_dir, memory_dir)
    if hindsight_path.exists():
        hindsight = json.loads(hindsight_path.read_text(encoding="utf-8"))
    policy_path = memory_dir / "policy.json"
    if policy_path.exists():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    if budget_path.exists():
        budget = json.loads(budget_path.read_text(encoding="utf-8"))
    if diversity_path.exists():
        diversity = json.loads(diversity_path.read_text(encoding="utf-8"))
    if backend_path.exists():
        backend = json.loads(backend_path.read_text(encoding="utf-8"))
    external_review = read_external_review(memory_dir)
    human_feedback = read_human_feedback(memory_dir)
    human_feedback_responses = read_human_feedback_responses(memory_dir)
    if science_summary_path.exists():
        science_summary = json.loads(science_summary_path.read_text(encoding="utf-8"))
    if mutation_brief_path.exists():
        mutation_brief = json.loads(mutation_brief_path.read_text(encoding="utf-8"))
    if backend_module_summary_path.exists():
        backend_module_summary = json.loads(backend_module_summary_path.read_text(encoding="utf-8"))
    active_candidate_id = str(state.get("active_candidate_id", "") or "")
    if active_candidate_id:
        live_command_path = candidates_dir / active_candidate_id / "traces" / "live_command.json"
        if live_command_path.exists():
            live_command = json.loads(live_command_path.read_text(encoding="utf-8"))
    explicit_lever_candidate_id, lever_payload, effective_lever_candidate_id, effective_lever_payload = _latest_backend_science_artifacts(
        candidates_dir,
        index,
        state,
    )
    external_lab_lines = [
        f"- lab advice: `{str(item.get('summary', '')).strip()}`"
        for item in external_review.get("lab_advice", [])[:3]
        if str(item.get("summary", "")).strip()
    ]
    if not external_lab_lines:
        external_lab_lines = ["- lab advice: `No live external advice.`"]
    external_human_lines = [
        f"- human advice: `{str(item.get('summary', '')).strip()}`"
        for item in external_review.get("human_advice", [])[:2]
        if str(item.get("summary", "")).strip()
    ]
    if not external_human_lines:
        external_human_lines = ["- human advice: `No human-facing advice.`"]
    ranked_human_lines = [
        f"- [{int(item.get('priority', 0))}] `{item.get('kind', '')}`: `{item.get('summary', '')}`"
        for item in human_feedback.get("items", [])[:5]
    ]
    if not ranked_human_lines:
        ranked_human_lines = ["- the lab has no ranked human requests yet"]
    response_lines = []
    for item in human_feedback_responses.get("responses", [])[:5]:
        kind = str(item.get("kind", "")).strip() or "-"
        summary = str(item.get("response_summary", "")).strip() or "No response summary."
        commit_sha = str(item.get("commit_sha", "")).strip()
        if commit_sha:
            response_lines.append(f"- `{kind}` addressed by `{commit_sha[:7]}`: `{summary}`")
            continue
        status = str(item.get("status", "")).strip() or "responded_manually"
        response_lines.append(f"- `{kind}` {status}: `{summary}`")
    if not response_lines:
        response_lines = ["- no recent human responses recorded yet"]
    manual_response_relpath = manual_human_feedback_responses_path(memory_dir).relative_to(repo_dir)
    module_lookup = {
        str(item.get("module", "")).strip(): item
        for item in backend_module_summary.get("modules", [])
        if str(item.get("module", "")).strip()
    }
    backend_levers = [
        ("science_model", "model"),
        ("science_loss", "loss"),
        ("science_eval", "eval"),
        ("science_config", "config"),
        ("science_train", "train"),
    ]
    backend_lever_lines = []
    target_module = str(mutation_brief.get("target_module", "")).strip()
    for module_name, label in backend_levers:
        item = module_lookup.get(module_name, {})
        focus = "targeted" if module_name == target_module else "available"
        backend_lever_lines.append(
            f"- {label}: `{module_name}` ({focus}); attempts `{item.get('attempts', 0)}`, "
            f"audit_blocked `{item.get('audit_blocked_count', 0)}`, avg_gap `{item.get('avg_transfer_gap', '-')}`"
        )
    backend_module_lines = []
    for item in backend_module_summary.get("modules", [])[:4]:
        backend_module_lines.append(
            f"- `{item.get('module', '-')}`: attempts `{item.get('attempts', 0)}`, "
            f"audit_blocked `{item.get('audit_blocked_count', 0)}`, "
            f"avg_gap `{item.get('avg_transfer_gap', '-')}`"
        )
    if not backend_module_lines:
        backend_module_lines = ["- no backend module summary yet"]
    backend_science_lines = [
        f"- summary: `{backend_module_summary.get('summary', 'No backend-science summary yet.')}`",
        f"- recommended_action: `{mutation_brief.get('recommended_action', 'wait')}`",
        f"- target_module: `{mutation_brief.get('target_module', '-') or '-'}`",
        f"- problem: `{mutation_brief.get('problem_statement', 'No current backend-science problem statement yet.')}`",
        f"- why_this_module: `{mutation_brief.get('module_rationale', 'No module rationale yet.')}`",
        f"- secondary_context: `{mutation_brief.get('science_debug_summary', 'No secondary backend-science context yet.')}`",
        f"- scored_candidates_since_change: `{mutation_brief.get('context', {}).get('scored_candidates_since_change', '-')}`",
        f"- last_structural_commit: `{str(mutation_brief.get('context', {}).get('last_structural_commit', '') or '-')[:7]}`",
    ]
    chosen_lever_lines = [f"- source_candidate: `{explicit_lever_candidate_id or '-'}`"]
    for module_name, label in backend_levers:
        module_values = lever_payload.get(module_name, {}) if isinstance(lever_payload, dict) else {}
        if isinstance(module_values, dict) and module_values:
            assignments = ", ".join(f"{key}={value}" for key, value in sorted(module_values.items()))
            chosen_lever_lines.append(f"- {label}: `{assignments}`")
    if len(chosen_lever_lines) == 1:
        chosen_lever_lines.append("- no explicit lever values chosen yet")
    effective_field_groups = {
        "science_model": ("hidden_dim", "global_dim", "instance_dim", "k_neighbors", "instance_modulation_scale"),
        "science_loss": ("param_loss_weight", "boundary_loss_weight", "instance_loss_weight", "instance_margin"),
        "science_eval": ("transfer_smoke_min_score", "transfer_smoke_max_gap", "transfer_smoke_min_boundary_f1"),
        "science_config": ("lr", "weight_decay", "time_budget_seconds", "eval_reserve_seconds"),
        "science_train": ("batch_size", "eval_batch_size", "grad_clip", "log_interval"),
    }
    effective_lever_lines = [f"- source_candidate: `{effective_lever_candidate_id or '-'}`"]
    for module_name, label in backend_levers:
        field_names = effective_field_groups.get(module_name, ())
        assignments = [
            f"{field}={effective_lever_payload[field]}"
            for field in field_names
            if isinstance(effective_lever_payload, dict) and field in effective_lever_payload
        ]
        if assignments:
            effective_lever_lines.append(f"- {label}: `{', '.join(assignments)}`")
    if len(effective_lever_lines) == 1:
        effective_lever_lines.append("- no effective backend settings recorded yet")

    recent = list(index.get("candidates", []))[-5:]
    recent_lines = []
    for item in reversed(recent):
        recent_lines.append(
            f"- `{item.get('candidate_id', '')}`: outcome `{item.get('outcome_label', '') or '-'}`; "
            f"diagnosis `{item.get('diagnosis_status', '') or '-'}`; "
            f"benchmark `{item.get('benchmark_score', '-')}`"
        )
    if not recent_lines:
        recent_lines.append("- no candidate history yet")

    leaders = science_summary.get("leaders", {})
    best_benchmark = leaders.get("best_benchmark", {})
    best_audit = leaders.get("best_audit", {})
    best_transfer = leaders.get("best_transfer", {})
    best_stable = leaders.get("best_stable", {})
    leaderboard_lines = [
        f"- best benchmark: `{best_benchmark.get('candidate_id', '-') or '-'}` -> `{best_benchmark.get('benchmark_score', '-')}`",
        f"- best audit: `{best_audit.get('candidate_id', '-') or '-'}` -> `{best_audit.get('audit_score', '-')}`",
        f"- tightest transfer: `{best_transfer.get('candidate_id', '-') or '-'}` -> gap `{best_transfer.get('transfer_gap', '-')}`",
        f"- best stable: `{best_stable.get('candidate_id', '-') or '-'}` -> audit `{best_stable.get('audit_score', '-')}`",
    ]
    recent_trend = science_summary.get("recent_trend", {})
    trend_lines = [
        f"- summary: `{science_summary.get('trend_summary', 'No scored candidates yet.')}`",
        f"- recent benchmark avg: `{recent_trend.get('benchmark_avg', '-')}`",
        f"- recent audit avg: `{recent_trend.get('audit_avg', '-')}`",
        f"- recent transfer gap avg: `{recent_trend.get('avg_transfer_gap', '-')}`",
    ]
    recent_science_lines = []
    for item in reversed(recent_trend.get("candidates", [])[-5:]):
        recent_science_lines.append(
            f"- `{item.get('candidate_id', '')}`: benchmark `{item.get('benchmark_score', '-')}`, "
            f"audit `{item.get('audit_score', '-')}`, gap `{item.get('transfer_gap', '-')}`"
        )
    if not recent_science_lines:
        recent_science_lines.append("- no scored candidates yet")

    latest_lines = []
    if latest is not None:
        latest_lines = [
            f"- candidate: `{latest.candidate_id}`",
            f"- dataset: `{latest.dataset_id}` via `{latest.dataset_action}`",
            f"- seed action: `{latest.seed_action}`",
            f"- proposal status: `{latest.loop.proposal_status}`",
            f"- outcome status: `{latest.loop.outcome_status}`",
            f"- diagnosis status: `{latest.loop.diagnosis_status}`",
            f"- next top parent: `{latest.loop.top_parent_id or '-'}`",
            f"- published: `{latest.published}`",
            f"- commit: `{latest.commit_sha or '-'}`",
            f"- cycle mode: `{state.get('last_cycle_mode', '') or '-'}`",
        ]
    else:
        latest_lines = ["- no completed big-bang step yet"]
    hindsight_adjustments = [
        f"- adjustment: `{item}`"
        for item in hindsight.get("policy_adjustments", [])[:3]
    ]
    if not hindsight_adjustments:
        hindsight_adjustments = ["- adjustment: `No policy adjustments yet.`"]

    content = "\n".join(
        [
            "# Big Bang",
            "",
            "The GitHub repo is the lab dashboard.",
            "",
            "## State",
            f"- status: `{state.get('status', 'idle')}`",
            f"- vital_spark_at: `{state.get('vital_spark_at', '') or '-'}`",
            f"- started_at: `{state.get('started_at', '') or '-'}`",
            f"- last_heartbeat: `{state.get('last_heartbeat', '') or '-'}`",
            f"- cycles_completed: `{state.get('cycles_completed', 0)}`",
            f"- genesis seed: `{GENESIS_CANDIDATE_ID}`",
            f"- last candidate: `{state.get('last_candidate_id', '') or '-'}`",
            f"- last dataset: `{state.get('last_dataset_id', '') or '-'}`",
            f"- last commit: `{state.get('last_commit_sha', '') or '-'}`",
            f"- last publish message: `{state.get('last_publish_message', '') or '-'}`",
            f"- last cycle mode: `{state.get('last_cycle_mode', '') or '-'}`",
            f"- novelty cycles triggered: `{state.get('novelty_cycles_triggered', 0)}`",
            "",
            "## Latest Step",
            *latest_lines,
            "",
            "## Active Backend",
            f"- active_candidate: `{active_candidate_id or '-'}`",
            f"- backend_status: `{live_command.get('status', '-')}`",
            f"- backend_pid: `{live_command.get('pid', '-')}`",
            f"- backend_started_at: `{live_command.get('started_at', '-')}`",
            f"- backend_last_poll_at: `{live_command.get('last_poll_at', '-')}`",
            f"- backend_poll_interval_seconds: `{live_command.get('poll_interval_seconds', '-')}`",
            "",
            "## Recent Candidates",
            *recent_lines,
            "",
            "## Science Leaders",
            *leaderboard_lines,
            "",
            "## Science Trend",
            *trend_lines,
            *recent_science_lines,
            "",
            "## Hindsight",
            f"- summary: `{hindsight.get('summary', 'No hindsight yet.')}`",
            *hindsight_adjustments,
            "",
            "## Policy",
            f"- summary: `{policy.get('summary', 'No policy yet.')}`",
            f"- selection_mode: `{policy.get('selection_mode', '-')}`",
            f"- cooldown_multiplier: `{policy.get('cooldown_multiplier', '-')}`",
            f"- preferred_runner_backend: `{policy.get('preferred_runner_backend', '-')}`",
            f"- publish_every_cycles: `{policy.get('publish_every_cycles', '-')}`",
            f"- novelty_cycle_priority: `{policy.get('novelty_cycle_priority', '-')}`",
            "",
            "## Budget",
            f"- summary: `{budget.get('summary', 'No budget yet.')}`",
            f"- exploration_mode: `{budget.get('exploration_mode', '-')}`",
            f"- tracked_mechanisms: `{len(budget.get('mechanism_budgets', []))}`",
            "",
            "## Backend",
            f"- summary: `{backend.get('summary', 'No backend profile yet.')}`",
            f"- preferred_backend: `{backend.get('preferred_backend', '-')}`",
            f"- available_backends: `{', '.join(backend.get('available_backends', [])) or '-'}`",
            f"- command_backend_configured: `{backend.get('command_backend_configured', False)}`",
            "",
            "## Backend Science",
            *backend_science_lines,
            "### Chosen Lever Values",
            *chosen_lever_lines,
            "",
            "### Effective Backend Settings",
            *effective_lever_lines,
            "",
            "### Modular Levers",
            *backend_lever_lines,
            "",
            "### Recent Module Evidence",
            *backend_module_lines,
            "",
            "## External Review",
            f"- status: `{external_review.get('status', 'idle')}`",
            f"- trigger_reason: `{external_review.get('trigger_reason', '') or '-'}`",
            f"- reviewer: `{external_review.get('reviewer', 'none')}`",
            f"- summary: `{external_review.get('situation_summary', 'No external review yet.')}`",
            *external_lab_lines,
            *external_human_lines,
            "",
            "## What The Lab Wants",
            f"- summary: `{human_feedback.get('summary', 'The lab has no human-facing requests yet.')}`",
            *ranked_human_lines,
            "",
            "## What We Did",
            f"- summary: `{human_feedback_responses.get('summary', 'No recent human responses recorded yet.')}`",
            f"- response_file: `{manual_response_relpath}`",
            *response_lines,
            "",
            "## Diversity",
            f"- summary: `{diversity.get('summary', 'No diversity yet.')}`",
            f"- current_mechanism_streak: `{diversity.get('current_mechanism_streak', '-')}`",
            f"- novelty_step_recommended: `{diversity.get('novelty_step_recommended', False)}`",
        ]
    )
    output_path.write_text(content + "\n", encoding="utf-8")
    return output_path


@dataclass(frozen=True)
class BigBangResult:
    cycles_completed: int
    last_candidate_id: str | None
    last_commit_sha: str | None
    status_path: Path
    dashboard_path: Path


def run_big_bang(
    *,
    repo_dir: Path,
    candidates_dir: Path,
    memory_dir: Path,
    datasets_dir: Path,
    source_dataset_id: str,
    prepared_dataset_id: str,
    limit: int,
    offset: int,
    num_points: int,
    val_count: int,
    shard_size: int,
    seed: int,
    workers: int,
    interval_seconds: int,
    cycles: int,
    publish: bool,
    runner_backend: str = "simulated",
) -> BigBangResult:
    started_at = utc_now()
    write_backend_profile(memory_dir)
    write_policy(candidates_dir, memory_dir, memory_dir / "policy.json")
    write_budget(memory_dir, memory_dir / "budget.json")
    write_diversity(candidates_dir, memory_dir / "diversity.json")
    update_big_bang_state(
        memory_dir,
        status="running",
        started_at=started_at,
        last_heartbeat=started_at,
    )
    latest_result: LabStepResult | None = None
    completed = 0
    novelty_cycles_triggered = 0
    try:
        while cycles <= 0 or completed < cycles:
            heartbeat = utc_now()
            update_big_bang_state(memory_dir, status="running", last_heartbeat=heartbeat)
            diversity = read_diversity(memory_dir)
            cycle_mode = "novelty_cycle" if bool(diversity.get("novelty_step_recommended")) else "normal_cycle"
            candidate_id = next_candidate_id(candidates_dir)
            update_big_bang_state(
                memory_dir,
                status="running",
                last_heartbeat=utc_now(),
                active_candidate_id=candidate_id,
                active_candidate_started_at=utc_now(),
                last_cycle_mode=cycle_mode,
            )
            render_big_bang_markdown(repo_dir, candidates_dir, memory_dir, latest_result)
            latest_result = run_lab_step(
                repo_dir=repo_dir,
                candidates_dir=candidates_dir,
                memory_dir=memory_dir,
                datasets_dir=datasets_dir,
                source_dataset_id=source_dataset_id,
                prepared_dataset_id=prepared_dataset_id,
                limit=limit,
                offset=offset,
                num_points=num_points,
                val_count=val_count,
                shard_size=shard_size,
                seed=seed,
                workers=workers,
                candidate_id=candidate_id,
                finalize_outcome=True,
                simulate_outcome=True,
                runner_backend=runner_backend,
                publish=False,
                publish_message=None,
            )
            completed += 1
            if cycle_mode == "novelty_cycle":
                novelty_cycles_triggered += 1
            review = maybe_request_external_review(candidates_dir, memory_dir)
            update_big_bang_state(
                memory_dir,
                status="running",
                last_heartbeat=utc_now(),
                cycles_completed=completed,
                last_candidate_id=latest_result.candidate_id,
                last_commit_sha=latest_result.commit_sha or "",
                last_dataset_id=latest_result.dataset_id,
                last_dataset_action=latest_result.dataset_action,
                last_seed_action=latest_result.seed_action,
                last_publish_message=latest_result.publish_message,
                last_cycle_mode=cycle_mode,
                novelty_cycles_triggered=novelty_cycles_triggered,
                last_external_review_status=review.get("status", ""),
                last_external_review_reason=review.get("trigger_reason", ""),
                active_candidate_id="",
                active_candidate_started_at="",
            )
            render_big_bang_markdown(repo_dir, candidates_dir, memory_dir, latest_result)
            policy = read_policy(memory_dir)
            publish_every_cycles = int(policy.get("publish_every_cycles", 1) or 1)
            novelty_priority = str(policy.get("novelty_cycle_priority", "normal")).strip()
            should_publish_this_cycle = publish and (
                (cycle_mode == "novelty_cycle" and novelty_priority == "high")
                or (publish_every_cycles > 0 and (completed % publish_every_cycles == 0))
            )
            if should_publish_this_cycle:
                publish_result = publish_repo_snapshot(
                    repo_dir,
                    f"big-bang: {cycle_mode} {latest_result.candidate_id}",
                )
                update_big_bang_state(
                    memory_dir,
                    last_commit_sha=publish_result.commit_sha or "",
                    last_publish_message=publish_result.message,
                )
            if cycles > 0 and completed >= cycles:
                break
            time.sleep(max(1, interval_seconds))
    finally:
        final_status = "idle"
        if latest_result is not None:
            final_status = "completed"
        update_big_bang_state(
            memory_dir,
            status=final_status,
            last_heartbeat=utc_now(),
            cycles_completed=completed,
        )
        dashboard_path = render_big_bang_markdown(repo_dir, candidates_dir, memory_dir, latest_result)

    return BigBangResult(
        cycles_completed=completed,
        last_candidate_id=latest_result.candidate_id if latest_result else None,
        last_commit_sha=load_big_bang_state(memory_dir).get("last_commit_sha") or None,
        status_path=big_bang_state_path(memory_dir),
        dashboard_path=dashboard_path,
    )
