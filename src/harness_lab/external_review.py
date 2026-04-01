from __future__ import annotations

import json
import logging
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("harness_lab.external_review")

from harness_lab.hindsight import read_hindsight
from harness_lab.llm import run_claude_json
from harness_lab.memory import read_json
from harness_lab.workspace import write_json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def external_review_path(memory_dir: Path) -> Path:
    return memory_dir / "external_review.json"


def default_external_review() -> dict:
    return {
        "status": "idle",
        "review_requested": False,
        "reviewer": "none",
        "trigger_reason": "",
        "timestamp": "",
        "candidate_count": 0,
        "last_review_candidate_count": 0,
        "review_interval_candidates": 10,
        "cooldown_remaining_candidates": 0,
        "situation_summary": "No external review yet.",
        "lab_advice": [],
        "human_advice": [],
        "confidence": 0.0,
        "evidence_used": [],
        "command_configured": False,
    }


def read_external_review(memory_dir: Path) -> dict:
    path = external_review_path(memory_dir)
    if not path.exists():
        return default_external_review()
    return json.loads(path.read_text(encoding="utf-8"))


def _recent_streak(candidates: list[dict], label: str) -> int:
    streak = 0
    for item in reversed(candidates):
        if str(item.get("outcome_label", "")).strip() == label:
            streak += 1
        else:
            break
    return streak


def _recent_failure_counts(candidates: list[dict], *, window: int = 10) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in candidates[-window:]:
        for label in item.get("observed_failure_modes", []) or []:
            key = str(label).strip()
            if not key:
                continue
            counts[key] = counts.get(key, 0) + 1
    return counts


def _recent_mechanism_counts(candidates: list[dict], *, window: int = 10) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in candidates[-window:]:
        key = str(item.get("diagnosis_mechanism", "") or item.get("harness_component", "")).strip()
        if not key:
            continue
        counts[key] = counts.get(key, 0) + 1
    return counts


def _review_trigger(index: dict, hindsight: dict, previous: dict, *, force: bool = False) -> tuple[bool, str, int]:
    candidate_count = int(index.get("candidate_count", 0) or 0)
    interval = int(previous.get("review_interval_candidates", 10) or 10)
    last_review_count = int(previous.get("last_review_candidate_count", 0) or 0)
    cooldown_remaining = max(0, interval - max(0, candidate_count - last_review_count))
    candidates = list(index.get("candidates", []))
    dead_end_streak = _recent_streak(candidates, "dead_end")
    train_error_streak = _recent_streak(candidates, "train_error")
    audit_blocked_streak = _recent_streak(candidates, "audit_blocked")
    over_mechanisms = hindsight.get("over_explored_mechanisms", [])
    over_backend = hindsight.get("over_explored_backend_fingerprints", [])

    reason = ""
    if force:
        reason = "forced_review"
    elif train_error_streak >= 2:
        reason = "repeated_train_error"
    elif audit_blocked_streak >= 2:
        reason = "repeated_audit_blocked"
    elif dead_end_streak >= 3:
        reason = "dead_end_streak"
    elif candidate_count >= 6 and not index.get("outcome_label_counts", {}).get("keeper"):
        reason = "no_keeper_yet"
    elif over_mechanisms or over_backend:
        reason = "exhaustion_signal"

    should_review = bool(reason) and (force or cooldown_remaining == 0)
    return should_review, reason, cooldown_remaining


def _heuristic_review_payload(index: dict, hindsight: dict, policy: dict, trigger_reason: str, candidate_count: int) -> dict:
    candidates = list(index.get("candidates", []))
    top_failures = sorted(_recent_failure_counts(candidates).items(), key=lambda item: (-item[1], item[0]))
    top_mechanisms = sorted(_recent_mechanism_counts(candidates).items(), key=lambda item: (-item[1], item[0]))
    over_backend = hindsight.get("over_explored_backend_fingerprints", [])
    under_backend = hindsight.get("under_explored_backend_fingerprints", [])
    lab_advice: list[dict] = []
    human_advice: list[dict] = []

    if trigger_reason == "repeated_train_error":
        lab_advice.append(
            {
                "kind": "stabilize",
                "summary": "Shrink the next backend change and prefer stability-oriented follow-ups until train errors stop recurring.",
            }
        )
        human_advice.append(
            {
                "kind": "seed_backend_strength",
                "summary": "Expose smaller independently evolvable backend modules so the lab can make less brittle science edits.",
            }
        )
    if trigger_reason in {"repeated_audit_blocked", "dead_end_streak", "no_keeper_yet", "exhaustion_signal"}:
        lab_advice.append(
            {
                "kind": "direction",
                "summary": "Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.",
            }
        )
    for item in under_backend[:2]:
        fingerprint = str(item.get("fingerprint", "")).strip()
        if fingerprint:
            lab_advice.append(
                {
                    "kind": "backend_priority",
                    "summary": f"Promote backend change type `{fingerprint}` because hindsight says it is promising and under-explored.",
                }
            )
    for item in over_backend[:2]:
        fingerprint = str(item.get("fingerprint", "")).strip()
        if fingerprint:
            lab_advice.append(
                {
                    "kind": "backend_guardrail",
                    "summary": f"Cool down backend change type `{fingerprint}` because it has already been over-explored.",
                }
            )
    if top_failures:
        human_advice.append(
            {
                "kind": "non_self_evolving",
                "summary": f"Consider strengthening the non-self-evolving seed around `{top_failures[0][0]}` if that failure mode keeps dominating.",
            }
        )
    if top_mechanisms:
        human_advice.append(
            {
                "kind": "module_surface",
                "summary": f"Consider exposing `{top_mechanisms[0][0]}` as a more explicit evolvable backend module if it keeps dominating search.",
            }
        )

    situation_summary = (
        f"After {candidate_count} candidates, the lab requested peer review because `{trigger_reason}` fired. "
        f"Current policy mode is `{policy.get('selection_mode', 'balanced')}`."
    )
    evidence_used = [
        "artifacts/memory/candidate_index.json",
        "artifacts/memory/hindsight.json",
        "artifacts/memory/policy.json",
    ]
    return {
        "reviewer": "heuristic",
        "situation_summary": situation_summary,
        "lab_advice": lab_advice[:5],
        "human_advice": human_advice[:5],
        "confidence": 0.55,
        "evidence_used": evidence_used,
    }


def _llm_review_prompt(index: dict, hindsight: dict, policy: dict, trigger_reason: str, candidate_count: int) -> str:
    recent_candidates = list(index.get("candidates", []))[-5:]
    compact_recent = [
        {
            "candidate_id": item.get("candidate_id", ""),
            "outcome_label": item.get("outcome_label", ""),
            "diagnosis_mechanism": item.get("diagnosis_mechanism", ""),
            "backend_fingerprints": item.get("backend_fingerprints", []),
            "benchmark_score": item.get("benchmark_score"),
            "audit_score": item.get("audit_score"),
        }
        for item in recent_candidates
    ]
    payload = {
        "trigger_reason": trigger_reason,
        "candidate_count": candidate_count,
        "policy_summary": policy.get("summary", ""),
        "policy_selection_mode": policy.get("selection_mode", "balanced"),
        "policy_adjustments": policy.get("policy_adjustments", [])[:5],
        "hindsight_findings": hindsight.get("hindsight_findings", [])[:5],
        "top_outcomes": hindsight.get("top_outcomes", []),
        "top_failure_modes": hindsight.get("top_failure_modes", []),
        "over_explored_mechanisms": hindsight.get("over_explored_mechanisms", []),
        "under_explored_promising_mechanisms": hindsight.get("under_explored_promising_mechanisms", []),
        "over_explored_backend_fingerprints": hindsight.get("over_explored_backend_fingerprints", []),
        "under_explored_backend_fingerprints": hindsight.get("under_explored_backend_fingerprints", []),
        "process_classification_counts": hindsight.get("process_classification_counts", {}),
        "throughput_summary": hindsight.get("throughput_summary", {}),
        "recent_candidates": compact_recent,
    }
    return (
        "You are a bounded research peer reviewer for harness-lab.\n"
        "Return only JSON with keys: situation_summary, lab_advice, human_advice, confidence, evidence_used.\n"
        "lab_advice and human_advice must be arrays of objects with keys: kind, summary.\n"
        "lab_advice is allowed to steer only self-evolving search behavior.\n"
        "human_advice is only for non-self-evolving parts that require human review.\n"
        "Keep advice concrete, short, and grounded in the supplied evidence.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _normalize_review_payload(payload: dict, reviewer: str) -> dict | None:
    if not isinstance(payload, dict):
        return None
    situation_summary = str(payload.get("situation_summary", "")).strip()
    confidence = payload.get("confidence", 0.0)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0
    lab_advice = []
    for item in payload.get("lab_advice", []):
        if not isinstance(item, dict):
            continue
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "direction")).strip() or "direction"
        if summary:
            lab_advice.append({"kind": kind, "summary": summary})
    human_advice = []
    for item in payload.get("human_advice", []):
        if not isinstance(item, dict):
            continue
        summary = str(item.get("summary", "")).strip()
        kind = str(item.get("kind", "non_self_evolving")).strip() or "non_self_evolving"
        if summary:
            human_advice.append({"kind": kind, "summary": summary})
    evidence_used = [str(item) for item in payload.get("evidence_used", []) if str(item).strip()]
    if not situation_summary:
        return None
    return {
        "reviewer": reviewer,
        "situation_summary": situation_summary,
        "lab_advice": lab_advice[:5],
        "human_advice": human_advice[:5],
        "confidence": confidence,
        "evidence_used": evidence_used[:8],
    }


def _run_llm_review(index: dict, hindsight: dict, policy: dict, trigger_reason: str, candidate_count: int, memory_dir: Path) -> dict | None:
    if str(os.environ.get("HARNESS_LAB_LLM_REVIEW_ENABLED", "")).strip().lower() not in {"1", "true", "yes"}:
        return None
    prompt = _llm_review_prompt(index, hindsight, policy, trigger_reason, candidate_count)
    payload = run_claude_json(prompt, cwd=memory_dir.parent.parent)
    result = _normalize_review_payload(payload, "claude") if payload else None
    if result:
        log.info("external review authored by claude (trigger=%s)", trigger_reason)
    else:
        log.warning("external review: claude fallback (trigger=%s, payload=%s)", trigger_reason, "empty" if not payload else "invalid")
    return result


def _run_command_review(memory_dir: Path, trigger_reason: str) -> dict | None:
    command = os.environ.get("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", "").strip()
    if not command:
        return None
    result_path = memory_dir / "external_review_result.json"
    env = os.environ.copy()
    env["HARNESS_LAB_EXTERNAL_REVIEW_RESULT_PATH"] = str(result_path)
    env["HARNESS_LAB_EXTERNAL_REVIEW_TRIGGER"] = trigger_reason
    env["HARNESS_LAB_CANDIDATE_INDEX_PATH"] = str(memory_dir / "candidate_index.json")
    env["HARNESS_LAB_HINDSIGHT_PATH"] = str(memory_dir / "hindsight.json")
    env["HARNESS_LAB_POLICY_PATH"] = str(memory_dir / "policy.json")
    env["HARNESS_LAB_SCIENCE_SUMMARY_PATH"] = str(memory_dir / "science_summary.json")
    completed = subprocess.run(command, shell=True, cwd=str(memory_dir.parent.parent), env=env, capture_output=True, text=True)
    if completed.returncode != 0 or not result_path.exists():
        return None
    payload = read_json(result_path)
    payload["reviewer"] = "command"
    return payload


def maybe_request_external_review(candidates_dir: Path, memory_dir: Path, *, force: bool = False) -> dict:
    from harness_lab.policy import read_policy

    memory_dir.mkdir(parents=True, exist_ok=True)
    previous = read_external_review(memory_dir)
    index = read_json(memory_dir / "candidate_index.json") if (memory_dir / "candidate_index.json").exists() else {"candidate_count": 0, "candidates": []}
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    should_review, trigger_reason, cooldown_remaining = _review_trigger(index, hindsight, previous, force=force)
    candidate_count = int(index.get("candidate_count", 0) or 0)
    payload = default_external_review()
    payload.update(
        {
            "status": "cooldown" if trigger_reason and not should_review else ("reviewed" if should_review else "idle"),
            "review_requested": should_review,
            "trigger_reason": trigger_reason,
            "timestamp": utc_now(),
            "candidate_count": candidate_count,
            "last_review_candidate_count": int(previous.get("last_review_candidate_count", 0) or 0),
            "review_interval_candidates": int(previous.get("review_interval_candidates", 10) or 10),
            "cooldown_remaining_candidates": cooldown_remaining,
            "command_configured": bool(os.environ.get("HARNESS_LAB_EXTERNAL_REVIEW_COMMAND", "").strip()),
        }
    )
    if should_review:
        review_payload = (
            _run_llm_review(index, hindsight, policy, trigger_reason, candidate_count, memory_dir)
            or
            _run_command_review(memory_dir, trigger_reason)
            or _heuristic_review_payload(index, hindsight, policy, trigger_reason, candidate_count)
        )
        payload.update(review_payload)
        payload["last_review_candidate_count"] = candidate_count
    elif previous.get("status") == "reviewed":
        payload["situation_summary"] = str(previous.get("situation_summary", "External review remains available.")) or "External review remains available."
        payload["lab_advice"] = list(previous.get("lab_advice", []))
        payload["human_advice"] = list(previous.get("human_advice", []))
        payload["confidence"] = float(previous.get("confidence", 0.0) or 0.0)
        payload["evidence_used"] = list(previous.get("evidence_used", []))
        payload["reviewer"] = str(previous.get("reviewer", "none"))

    write_json(external_review_path(memory_dir), payload)
    return payload
