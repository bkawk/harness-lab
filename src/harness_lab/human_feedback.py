from __future__ import annotations

import json
import subprocess
from pathlib import Path

from harness_lab.external_review import read_external_review
from harness_lab.hindsight import read_hindsight
from harness_lab.memory import read_json
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def human_feedback_path(memory_dir: Path) -> Path:
    return memory_dir / "human_feedback.json"


def human_feedback_responses_path(memory_dir: Path) -> Path:
    return memory_dir / "human_feedback_responses.json"


def manual_human_feedback_responses_path(memory_dir: Path) -> Path:
    return _repo_dir_from_memory(memory_dir) / "docs" / "lab_responses.json"


def default_human_feedback() -> dict:
    return {
        "summary": "The lab has no human-facing requests yet.",
        "items": [],
        "responses": [],
    }


def _score_item(*, leverage: int, urgency: int, recurrence: int, cost: int) -> int:
    return leverage + urgency + recurrence - cost


def _response_discount(response: dict | None, *, persistence: bool, default_discount: int) -> int:
    if not response:
        return 0
    return 0 if persistence else default_discount


def _label_counts(items: list[dict]) -> dict[str, int]:
    return {
        str(item.get("label", "")).strip(): int(item.get("count", 0) or 0)
        for item in items
        if str(item.get("label", "")).strip()
    }


def _quoted_identifier(text: str) -> str:
    summary = str(text)
    parts = summary.split("`")
    if len(parts) >= 3:
        return str(parts[1]).strip()
    return ""


RESPONSE_RULES = (
    {
        "kind": "evaluation",
        "match": "Refine transfer failure attribution",
        "response_summary": "Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.",
    },
    {
        "kind": "evaluation",
        "match": "Add transfer smoke gate before full audit",
        "response_summary": "Implemented a transfer-stability smoke gate before full audit.",
    },
    {
        "kind": "module_surface",
        "match": "Make mutation targeting failure-aware",
        "response_summary": "Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.",
    },
    {
        "kind": "module_surface",
        "match": "Enable proposal LLM in big-bang",
        "response_summary": "Enabled live Claude-authored proposals so module-targeted lever choices can actually be explored in the loop.",
    },
    {
        "kind": "ops",
        "match": "Harden backend startup and progress detection",
        "response_summary": "Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.",
    },
    {
        "kind": "dataset",
        "match": "Add named stratified evaluation slices",
        "response_summary": "Added named stratified evaluation slices so prepared datasets can separate benchmark, smoke, and audit behavior more clearly.",
    },
    {
        "kind": "seed_backend",
        "match": "Modularize science",
        "response_summary": "Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.",
    },
)


def _repo_dir_from_memory(memory_dir: Path) -> Path:
    return memory_dir.parent.parent


def _clean_manual_response(item: dict) -> dict:
    kind = str(item.get("kind", "")).strip()
    status = str(item.get("status", "")).strip()
    human_response = str(item.get("human_response", "")).strip()
    next_action = str(item.get("next_action", "")).strip()
    updated_at = str(item.get("updated_at", "")).strip()
    if not kind or (not human_response and not next_action):
        return {}
    response_summary = human_response or next_action
    if human_response and next_action:
        response_summary = f"{human_response} Next: {next_action}"
    return {
        "kind": kind,
        "commit_sha": "",
        "commit_subject": "",
        "response_summary": response_summary,
        "status": status or "responded_manually",
        "response_source": "manual",
        "human_response": human_response,
        "next_action": next_action,
        "updated_at": updated_at,
    }


def read_manual_human_feedback_responses(memory_dir: Path) -> dict:
    path = manual_human_feedback_responses_path(memory_dir)
    if not path.exists():
        return {"summary": "No manual human responses recorded yet.", "responses": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"summary": "Manual human responses file is invalid JSON.", "responses": []}
    responses = []
    for item in payload.get("responses", []):
        if not isinstance(item, dict):
            continue
        cleaned = _clean_manual_response(item)
        if cleaned:
            responses.append(cleaned)
    summary = (
        f"The humans manually responded to {len(responses)} lab request(s)."
        if responses
        else "No manual human responses recorded yet."
    )
    return {"summary": summary, "responses": responses}


def write_manual_human_feedback_response_template(memory_dir: Path, human_feedback: dict | None = None) -> Path:
    path = manual_human_feedback_responses_path(memory_dir)
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    items = human_feedback.get("items", []) if isinstance(human_feedback, dict) else []
    responses = [
        {
            "kind": str(item.get("kind", "")).strip(),
            "status": "",
            "human_response": "",
            "next_action": "",
            "updated_at": "",
        }
        for item in items[:5]
        if str(item.get("kind", "")).strip()
    ]
    write_json(
        path,
        {
            "summary": "Add manual responses here. Any non-empty human_response or next_action will appear in What We Did.",
            "responses": responses,
        },
    )
    return path


def _git_log(repo_dir: Path, limit: int = 80) -> list[dict]:
    try:
        completed = subprocess.run(
            ["git", "log", f"-n{limit}", "--format=%H%x09%s"],
            cwd=repo_dir,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    rows: list[dict] = []
    for line in (completed.stdout or "").splitlines():
        if not line.strip():
            continue
        sha, _, subject = line.partition("\t")
        rows.append({"commit_sha": sha.strip(), "subject": subject.strip()})
    return rows


def build_human_feedback_responses(memory_dir: Path) -> dict:
    repo_dir = _repo_dir_from_memory(memory_dir)
    commits = _git_log(repo_dir)
    responses: list[dict] = []
    seen_kinds: set[str] = set()
    manual_payload = read_manual_human_feedback_responses(memory_dir)
    for response in manual_payload.get("responses", []):
        kind = str(response.get("kind", "")).strip()
        if not kind or kind in seen_kinds:
            continue
        responses.append(response)
        seen_kinds.add(kind)
    for commit in commits:
        subject = str(commit.get("subject", ""))
        for rule in RESPONSE_RULES:
            kind = str(rule["kind"])
            if kind in seen_kinds:
                continue
            if str(rule["match"]) in subject:
                responses.append(
                    {
                        "kind": kind,
                        "commit_sha": str(commit.get("commit_sha", "")),
                        "commit_subject": subject,
                        "response_summary": str(rule["response_summary"]),
                        "status": "addressed_recently",
                    }
                )
                seen_kinds.add(kind)
    summary = (
        f"The humans recently addressed {len(responses)} lab request(s)."
        if responses
        else "No recent human responses recorded yet."
    )
    return {"summary": summary, "responses": responses}


def write_human_feedback_responses(memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = output_path or human_feedback_responses_path(memory_dir)
    write_json(path, build_human_feedback_responses(memory_dir))
    return path


def read_human_feedback_responses(memory_dir: Path) -> dict:
    path = human_feedback_responses_path(memory_dir)
    if not path.exists():
        return {"summary": "No recent human responses recorded yet.", "responses": []}
    return json.loads(path.read_text(encoding="utf-8"))


def build_human_feedback(memory_dir: Path) -> dict:
    external_review = read_external_review(memory_dir)
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    science_summary = read_json(memory_dir / "science_summary.json") if (memory_dir / "science_summary.json").exists() else {}
    science_debug = read_json(memory_dir / "science_debug_summary.json") if (memory_dir / "science_debug_summary.json").exists() else {}
    responses_payload = read_human_feedback_responses(memory_dir)
    response_by_kind = {
        str(item.get("kind", "")).strip(): item
        for item in responses_payload.get("responses", [])
        if str(item.get("kind", "")).strip()
    }
    top_outcomes = _label_counts(hindsight.get("top_outcomes", []))
    top_failures = _label_counts(hindsight.get("top_failure_modes", []))
    recent_top_outcomes = _label_counts(hindsight.get("recent_top_outcomes", []))
    recent_top_failures = _label_counts(hindsight.get("recent_top_failure_modes", []))
    recent_scored_candidate_count = int(hindsight.get("recent_scored_candidate_count", 0) or 0)

    items: list[dict] = []

    for item in external_review.get("human_advice", [])[:5]:
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "non_self_evolving")).strip() or "non_self_evolving"
        if not summary:
            continue
        if kind == "non_self_evolving" and recent_scored_candidate_count > 0:
            referenced_failure = _quoted_identifier(summary)
            if referenced_failure and recent_top_failures.get(referenced_failure, 0) == 0:
                continue
        response = response_by_kind.get(kind)
        priority = _score_item(leverage=5, urgency=4, recurrence=3, cost=2)
        why_now = str(external_review.get("trigger_reason", "") or "external_review")
        if response:
            priority = max(1, priority - 6)
            why_now = f"{why_now}; addressed recently by {str(response.get('commit_sha', ''))[:7]}"
        items.append(
            {
                "kind": kind,
                "summary": summary,
                "why_now": why_now,
                "evidence": list(external_review.get("evidence_used", []))[:5],
                "priority": priority,
                "confidence": float(external_review.get("confidence", 0.55) or 0.55),
                "source": "external_review",
                "response": response or {},
            }
        )

    leaders = science_summary.get("leaders", {})
    best_stable = leaders.get("best_stable", {})

    audit_blocked_count = recent_top_outcomes.get("audit_blocked", 0)
    recent_keeper_count = recent_top_outcomes.get("keeper", 0)
    recent_dead_end_count = recent_top_outcomes.get("dead_end", 0)
    evaluation_dominates_frontier = audit_blocked_count >= 3 and audit_blocked_count > recent_keeper_count
    if evaluation_dominates_frontier:
        response = response_by_kind.get("evaluation")
        persistence = bool(response) and audit_blocked_count >= 6
        items.append(
            {
                "kind": "evaluation",
                "summary": "Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.",
                "why_now": (
                    f"{audit_blocked_count} audit-blocked outcomes are dominating the frontier"
                    f" over {recent_keeper_count} keeper and {recent_dead_end_count} dead-end outcomes."
                    + (
                        f" The pressure persists after {str(response.get('commit_sha', ''))[:7]}."
                        if persistence
                        else f" Recently addressed by {str(response.get('commit_sha', ''))[:7]}."
                        if response
                        else ""
                    )
                ),
                "evidence": ["artifacts/memory/hindsight.json", "artifacts/memory/science_summary.json"],
                "priority": max(
                    1,
                    _score_item(leverage=5, urgency=5, recurrence=4, cost=2)
                    - _response_discount(response, persistence=persistence, default_discount=6),
                ),
                "confidence": 0.82 if persistence else 0.76,
                "source": "hindsight",
                "response": response or {},
            }
        )

    stale_process_count = recent_top_failures.get("stale_process", 0)
    startup_issue_count = recent_top_failures.get("startup_timeout", 0)
    no_progress_count = recent_top_failures.get("no_progress_timeout", 0)
    oom_count = recent_top_failures.get("cuda_oom", 0) + recent_top_failures.get("oom", 0) + recent_top_failures.get("vram_pressure", 0)
    if stale_process_count >= 1 or startup_issue_count >= 1 or no_progress_count >= 1:
        response = response_by_kind.get("ops")
        total_ops_failures = stale_process_count + startup_issue_count + no_progress_count
        persistence = bool(response) and total_ops_failures >= 6
        items.append(
            {
                "kind": "ops",
                "summary": "Harden backend startup and completion reporting so stalled candidates stop consuming full budget.",
                "why_now": (
                    f"The lab has already seen {total_ops_failures} startup/progress stall outcome(s)."
                    + (
                        f" The pressure persists after {str(response.get('commit_sha', ''))[:7]}."
                        if persistence
                        else f" Recently addressed by {str(response.get('commit_sha', ''))[:7]}."
                        if response
                        else ""
                    )
                ),
                "evidence": ["artifacts/memory/hindsight.json"],
                "priority": max(
                    1,
                    _score_item(leverage=4, urgency=4, recurrence=3, cost=2)
                    - _response_discount(response, persistence=persistence, default_discount=5),
                ),
                "confidence": 0.84 if persistence else 0.72,
                "source": "hindsight",
                "response": response or {},
            }
        )

    if oom_count >= 1:
        items.append(
            {
                "kind": "vram",
                "summary": "Increase effective VRAM headroom or reduce memory pressure so science candidates can finish without OOM-driven degradation.",
                "why_now": f"The lab has already seen {oom_count} memory-pressure failure(s), and the backend is now explicitly surfacing VRAM limits.",
                "evidence": ["artifacts/memory/hindsight.json", "artifacts/candidates/*/traces/science_progress.json"],
                "priority": _score_item(leverage=5, urgency=5, recurrence=3, cost=4),
                "confidence": 0.88,
                "source": "hindsight",
            }
        )
    vram_debug = science_debug.get("vram", {}) if isinstance(science_debug, dict) else {}
    avg_peak_vram_ratio = vram_debug.get("avg_peak_vram_ratio")
    avg_peak_vram_mb = vram_debug.get("avg_peak_vram_mb")
    completed_with_scores = int((science_debug.get("counts", {}) or {}).get("completed_with_scores", 0) or 0) if isinstance(science_debug, dict) else 0
    if (
        oom_count == 0
        and isinstance(avg_peak_vram_ratio, (int, float))
        and isinstance(avg_peak_vram_mb, (int, float))
        and completed_with_scores >= 2
        and float(avg_peak_vram_ratio) <= 0.2
    ):
        items.append(
            {
                "kind": "vram_headroom",
                "summary": "Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.",
                "why_now": (
                    f"Recent real-backend runs are averaging about {float(avg_peak_vram_mb):.1f} MB of peak VRAM, "
                    f"which is only about {float(avg_peak_vram_ratio) * 100:.1f}% of the available GPU memory."
                ),
                "evidence": ["artifacts/memory/science_debug_summary.json", "artifacts/memory/hardware_profile.json"],
                "priority": _score_item(leverage=3, urgency=2, recurrence=2, cost=2),
                "confidence": 0.72,
                "source": "science_debug",
            }
        )

    if not best_stable:
        items.append(
            {
                "kind": "seed_backend",
                "summary": "Strengthen the non-self-evolving seed backend so the lab has a better starting scientific basin.",
                "why_now": "The lab has not yet established a stable leader with strong transfer.",
                "evidence": ["artifacts/memory/science_summary.json"],
                "priority": _score_item(leverage=5, urgency=3, recurrence=2, cost=3),
                "confidence": 0.63,
                "source": "science_summary",
            }
        )

    policy_summary = str(policy.get("summary", "")).strip()
    if "transfer" in policy_summary.lower():
        response = response_by_kind.get("dataset")
        transfer_failure_count = recent_top_failures.get("transfer_collapse", 0) + recent_top_failures.get("transfer_regression", 0)
        persistence = bool(response) and (audit_blocked_count >= 6 or transfer_failure_count >= 4)
        items.append(
            {
                "kind": "dataset",
                "summary": "Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.",
                "why_now": (
                    "Current policy keeps steering toward transfer stability, which suggests the data/eval split is a recurring pressure point."
                    + (
                        f" The pressure persists after {str(response.get('commit_sha', ''))[:7]}."
                        if persistence
                        else f" Recently addressed by {str(response.get('commit_sha', ''))[:7]}."
                        if response
                        else ""
                    )
                ),
                "evidence": ["artifacts/memory/policy.json", "artifacts/memory/science_summary.json"],
                "priority": max(
                    1,
                    _score_item(leverage=4, urgency=3, recurrence=3, cost=3)
                    - _response_discount(response, persistence=persistence, default_discount=5),
                ),
                "confidence": 0.68 if persistence else 0.58,
                "source": "policy",
                "response": response or {},
            }
        )

    for item in items:
        item["recent_scored_candidate_count"] = recent_scored_candidate_count
        if item["source"] in {"hindsight", "policy", "science_debug"} and recent_scored_candidate_count > 0:
            item["recent_window_required"] = True

    deduped: dict[tuple[str, str], dict] = {}
    for item in items:
        key = (str(item.get("kind", "")), str(item.get("summary", "")))
        existing = deduped.get(key)
        if existing is None or float(item.get("confidence", 0.0)) > float(existing.get("confidence", 0.0)):
            deduped[key] = item

    filtered = [
        item
        for item in deduped.values()
        if not (
            bool(item.get("recent_window_required"))
            and int(item.get("recent_scored_candidate_count", 0) or 0) > 0
            and int(item.get("priority", 0) or 0) > 0
            and item["kind"] in {"evaluation", "ops", "vram", "dataset"}
            and (
                (
                    item["kind"] == "evaluation"
                    and not evaluation_dominates_frontier
                )
                or (
                    item["kind"] == "ops"
                    and (stale_process_count + startup_issue_count + no_progress_count) == 0
                )
                or (
                    item["kind"] == "vram"
                    and oom_count == 0
                )
                or (
                    item["kind"] == "dataset"
                    and (audit_blocked_count + transfer_failure_count) == 0
                )
            )
        )
    ]

    ranked = sorted(
        filtered,
        key=lambda item: (
            -int(item.get("priority", 0) or 0),
            -float(item.get("confidence", 0.0) or 0.0),
            str(item.get("kind", "")),
            str(item.get("summary", "")),
        ),
    )

    summary = (
        f"The lab has {len(ranked)} ranked requests for human help."
        if ranked
        else "The lab has no human-facing requests yet."
    )
    return {
        "summary": summary,
        "items": ranked[:8],
        "responses": responses_payload.get("responses", [])[:5],
    }


def write_human_feedback(memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_human_feedback_responses(memory_dir)
    human_feedback = build_human_feedback(memory_dir)
    write_manual_human_feedback_response_template(memory_dir, human_feedback)
    path = output_path or human_feedback_path(memory_dir)
    write_json(path, human_feedback)
    return path


def read_human_feedback(memory_dir: Path) -> dict:
    path = human_feedback_path(memory_dir)
    if not path.exists():
        return default_human_feedback()
    return json.loads(path.read_text(encoding="utf-8"))
