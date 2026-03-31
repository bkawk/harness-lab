from __future__ import annotations

import json
from pathlib import Path

from harness_lab.external_review import read_external_review
from harness_lab.hindsight import read_hindsight
from harness_lab.memory import read_json
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def human_feedback_path(memory_dir: Path) -> Path:
    return memory_dir / "human_feedback.json"


def default_human_feedback() -> dict:
    return {
        "summary": "The lab has no human-facing requests yet.",
        "items": [],
    }


def _score_item(*, leverage: int, urgency: int, recurrence: int, cost: int) -> int:
    return leverage + urgency + recurrence - cost


def build_human_feedback(memory_dir: Path) -> dict:
    external_review = read_external_review(memory_dir)
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    science_summary = read_json(memory_dir / "science_summary.json") if (memory_dir / "science_summary.json").exists() else {}

    items: list[dict] = []

    for item in external_review.get("human_advice", [])[:5]:
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "non_self_evolving")).strip() or "non_self_evolving"
        if not summary:
            continue
        items.append(
            {
                "kind": kind,
                "summary": summary,
                "why_now": str(external_review.get("trigger_reason", "") or "external_review"),
                "evidence": list(external_review.get("evidence_used", []))[:5],
                "priority": _score_item(leverage=5, urgency=4, recurrence=3, cost=2),
                "confidence": float(external_review.get("confidence", 0.55) or 0.55),
                "source": "external_review",
            }
        )

    top_outcomes = {str(item.get("label", "")): int(item.get("count", 0) or 0) for item in hindsight.get("top_outcomes", [])}
    top_failures = {str(item.get("label", "")): int(item.get("count", 0) or 0) for item in hindsight.get("top_failure_modes", [])}
    leaders = science_summary.get("leaders", {})
    best_stable = leaders.get("best_stable", {})

    audit_blocked_count = top_outcomes.get("audit_blocked", 0)
    if audit_blocked_count >= 3:
        items.append(
            {
                "kind": "evaluation",
                "summary": "Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.",
                "why_now": f"{audit_blocked_count} audit-blocked outcomes are dominating the frontier.",
                "evidence": ["artifacts/memory/hindsight.json", "artifacts/memory/science_summary.json"],
                "priority": _score_item(leverage=5, urgency=5, recurrence=4, cost=2),
                "confidence": 0.76,
                "source": "hindsight",
            }
        )

    stale_process_count = top_failures.get("stale_process", 0)
    if stale_process_count >= 1:
        items.append(
            {
                "kind": "ops",
                "summary": "Harden backend startup and completion reporting so stalled candidates stop consuming full budget.",
                "why_now": f"The lab has already seen {stale_process_count} stale-process outcomes.",
                "evidence": ["artifacts/memory/hindsight.json"],
                "priority": _score_item(leverage=4, urgency=4, recurrence=3, cost=2),
                "confidence": 0.72,
                "source": "hindsight",
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
    }


def write_human_feedback(memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = output_path or human_feedback_path(memory_dir)
    write_json(path, build_human_feedback(memory_dir))
    return path


def read_human_feedback(memory_dir: Path) -> dict:
    path = human_feedback_path(memory_dir)
    if not path.exists():
        return default_human_feedback()
    return json.loads(path.read_text(encoding="utf-8"))
