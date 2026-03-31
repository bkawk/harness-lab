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


def default_human_feedback() -> dict:
    return {
        "summary": "The lab has no human-facing requests yet.",
        "items": [],
        "responses": [],
    }


def _score_item(*, leverage: int, urgency: int, recurrence: int, cost: int) -> int:
    return leverage + urgency + recurrence - cost


RESPONSE_RULES = (
    {
        "kind": "evaluation",
        "match": "Add transfer smoke gate before full audit",
        "response_summary": "Implemented a transfer-stability smoke gate before full audit.",
    },
    {
        "kind": "ops",
        "match": "Harden backend startup and progress detection",
        "response_summary": "Hardened backend startup and no-progress detection so stuck candidates are cut off earlier.",
    },
)


def _repo_dir_from_memory(memory_dir: Path) -> Path:
    return memory_dir.parent.parent


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
    responses_payload = read_human_feedback_responses(memory_dir)
    response_by_kind = {
        str(item.get("kind", "")).strip(): item
        for item in responses_payload.get("responses", [])
        if str(item.get("kind", "")).strip()
    }

    items: list[dict] = []

    for item in external_review.get("human_advice", [])[:5]:
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "non_self_evolving")).strip() or "non_self_evolving"
        if not summary:
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

    top_outcomes = {str(item.get("label", "")): int(item.get("count", 0) or 0) for item in hindsight.get("top_outcomes", [])}
    top_failures = {str(item.get("label", "")): int(item.get("count", 0) or 0) for item in hindsight.get("top_failure_modes", [])}
    leaders = science_summary.get("leaders", {})
    best_stable = leaders.get("best_stable", {})

    audit_blocked_count = top_outcomes.get("audit_blocked", 0)
    if audit_blocked_count >= 3:
        response = response_by_kind.get("evaluation")
        items.append(
            {
                "kind": "evaluation",
                "summary": "Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.",
                "why_now": (
                    f"{audit_blocked_count} audit-blocked outcomes are dominating the frontier."
                    + (
                        f" Recently addressed by {str(response.get('commit_sha', ''))[:7]}."
                        if response
                        else ""
                    )
                ),
                "evidence": ["artifacts/memory/hindsight.json", "artifacts/memory/science_summary.json"],
                "priority": max(1, _score_item(leverage=5, urgency=5, recurrence=4, cost=2) - (6 if response else 0)),
                "confidence": 0.76,
                "source": "hindsight",
                "response": response or {},
            }
        )

    stale_process_count = top_failures.get("stale_process", 0)
    startup_issue_count = top_failures.get("startup_timeout", 0)
    no_progress_count = top_failures.get("no_progress_timeout", 0)
    if stale_process_count >= 1 or startup_issue_count >= 1 or no_progress_count >= 1:
        response = response_by_kind.get("ops")
        total_ops_failures = stale_process_count + startup_issue_count + no_progress_count
        items.append(
            {
                "kind": "ops",
                "summary": "Harden backend startup and completion reporting so stalled candidates stop consuming full budget.",
                "why_now": (
                    f"The lab has already seen {total_ops_failures} startup/progress stall outcome(s)."
                    + (
                        f" Recently addressed by {str(response.get('commit_sha', ''))[:7]}."
                        if response
                        else ""
                    )
                ),
                "evidence": ["artifacts/memory/hindsight.json"],
                "priority": max(1, _score_item(leverage=4, urgency=4, recurrence=3, cost=2) - (5 if response else 0)),
                "confidence": 0.72,
                "source": "hindsight",
                "response": response or {},
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
        items.append(
            {
                "kind": "dataset",
                "summary": "Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.",
                "why_now": "Current policy keeps steering toward transfer stability, which suggests the data/eval split is a recurring pressure point.",
                "evidence": ["artifacts/memory/policy.json", "artifacts/memory/science_summary.json"],
                "priority": _score_item(leverage=4, urgency=3, recurrence=3, cost=3),
                "confidence": 0.58,
                "source": "policy",
            }
        )

    deduped: dict[tuple[str, str], dict] = {}
    for item in items:
        key = (str(item.get("kind", "")), str(item.get("summary", "")))
        existing = deduped.get(key)
        if existing is None or float(item.get("confidence", 0.0)) > float(existing.get("confidence", 0.0)):
            deduped[key] = item

    ranked = sorted(
        deduped.values(),
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
    path = output_path or human_feedback_path(memory_dir)
    write_json(path, build_human_feedback(memory_dir))
    return path


def read_human_feedback(memory_dir: Path) -> dict:
    path = human_feedback_path(memory_dir)
    if not path.exists():
        return default_human_feedback()
    return json.loads(path.read_text(encoding="utf-8"))
