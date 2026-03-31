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
from harness_lab.human_feedback import read_human_feedback, write_human_feedback
from harness_lab.hindsight import write_hindsight
from harness_lab.memory import build_candidate_index
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
    science_summary = {}
    live_command = {}
    if candidates_dir.exists():
        write_hindsight(candidates_dir, hindsight_path)
        write_backend_profile(memory_dir)
        write_policy(candidates_dir, memory_dir, memory_dir / "policy.json")
        write_human_feedback(memory_dir, memory_dir / "human_feedback.json")
        write_budget(memory_dir, budget_path)
        write_diversity(candidates_dir, diversity_path)
        from harness_lab.memory import write_science_summary

        write_science_summary(candidates_dir, science_summary_path)
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
    if science_summary_path.exists():
        science_summary = json.loads(science_summary_path.read_text(encoding="utf-8"))
    active_candidate_id = str(state.get("active_candidate_id", "") or "")
    if active_candidate_id:
        live_command_path = candidates_dir / active_candidate_id / "traces" / "live_command.json"
        if live_command_path.exists():
            live_command = json.loads(live_command_path.read_text(encoding="utf-8"))
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
