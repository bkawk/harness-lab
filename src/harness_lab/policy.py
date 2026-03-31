from __future__ import annotations

import json
import os
from pathlib import Path

from harness_lab.backend import read_backend_profile, write_backend_profile
from harness_lab.diversity import read_diversity
from harness_lab.external_review import read_external_review
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
from harness_lab.llm import run_claude_json
from harness_lab.memory import read_json, write_candidate_index
from harness_lab.workspace import write_json


def default_policy() -> dict:
    return {
        "summary": "No policy yet.",
        "selection_mode": "balanced",
        "cooldown_multiplier": 1.0,
        "underexplored_bonus": 20,
        "backend_fingerprint_bonus": 10,
        "backend_fingerprint_cooldown": 12,
        "preferred_runner_backend": "simulated",
        "publish_every_cycles": 1,
        "novelty_cycle_priority": "normal",
        "policy_adjustments": [],
        "evidence": [],
    }


def _llm_policy_prompt(index: dict, hindsight: dict, diversity: dict, hardware: dict, backend: dict, external_review: dict, fallback_policy: dict) -> str:
    payload = {
        "candidate_count": index.get("candidate_count", 0),
        "hindsight_summary": hindsight.get("summary", ""),
        "hindsight_findings": hindsight.get("hindsight_findings", [])[:8],
        "policy_adjustments": hindsight.get("policy_adjustments", [])[:8],
        "diversity_summary": diversity.get("summary", ""),
        "hardware_summary": {
            "environment_hint": hardware.get("environment_hint", ""),
            "cpu_count": hardware.get("cpu_count"),
            "memory_gb_estimate": hardware.get("memory_gb_estimate"),
        },
        "backend_summary": backend.get("summary", ""),
        "external_review_summary": {
            "status": external_review.get("status", ""),
            "trigger_reason": external_review.get("trigger_reason", ""),
            "reviewer": external_review.get("reviewer", ""),
            "lab_advice": external_review.get("lab_advice", [])[:3],
        },
        "heuristic_fallback_policy": fallback_policy,
    }
    return (
        "You are synthesizing bounded policy for harness-lab.\n"
        "Return only JSON with keys: summary, selection_mode, cooldown_multiplier, underexplored_bonus, "
        "backend_fingerprint_bonus, backend_fingerprint_cooldown, preferred_runner_backend, publish_every_cycles, "
        "novelty_cycle_priority, policy_adjustments, evidence.\n"
        "Keep the policy grounded in the supplied hindsight and operating context.\n\n"
        f"{json.dumps(payload, indent=2, sort_keys=True)}"
    )


def _normalize_llm_policy_payload(payload: dict, fallback: dict) -> dict | None:
    if not isinstance(payload, dict):
        return None
    summary = str(payload.get("summary", "")).strip()
    selection_mode = str(payload.get("selection_mode", fallback.get("selection_mode", "balanced"))).strip()
    preferred_runner_backend = str(payload.get("preferred_runner_backend", fallback.get("preferred_runner_backend", "simulated"))).strip()
    novelty_cycle_priority = str(payload.get("novelty_cycle_priority", fallback.get("novelty_cycle_priority", "normal"))).strip()
    if not summary:
        return None
    normalized = dict(fallback)
    normalized.update(
        {
            "summary": summary,
            "selection_mode": selection_mode or fallback.get("selection_mode", "balanced"),
            "cooldown_multiplier": float(payload.get("cooldown_multiplier", fallback.get("cooldown_multiplier", 1.0)) or fallback.get("cooldown_multiplier", 1.0)),
            "underexplored_bonus": int(payload.get("underexplored_bonus", fallback.get("underexplored_bonus", 20)) or fallback.get("underexplored_bonus", 20)),
            "backend_fingerprint_bonus": int(payload.get("backend_fingerprint_bonus", fallback.get("backend_fingerprint_bonus", 10)) or fallback.get("backend_fingerprint_bonus", 10)),
            "backend_fingerprint_cooldown": int(payload.get("backend_fingerprint_cooldown", fallback.get("backend_fingerprint_cooldown", 12)) or fallback.get("backend_fingerprint_cooldown", 12)),
            "preferred_runner_backend": preferred_runner_backend or fallback.get("preferred_runner_backend", "simulated"),
            "publish_every_cycles": int(payload.get("publish_every_cycles", fallback.get("publish_every_cycles", 1)) or fallback.get("publish_every_cycles", 1)),
            "novelty_cycle_priority": novelty_cycle_priority or fallback.get("novelty_cycle_priority", "normal"),
            "policy_adjustments": [str(item).strip() for item in payload.get("policy_adjustments", []) if str(item).strip()][:8] or list(fallback.get("policy_adjustments", [])),
            "evidence": [str(item).strip() for item in payload.get("evidence", []) if str(item).strip()][:8] or list(fallback.get("evidence", [])),
            "policy_reviewer": "claude",
        }
    )
    return normalized


def build_policy(candidates_dir: Path, memory_dir: Path) -> dict:
    candidate_index_path = memory_dir / "candidate_index.json"
    if not candidate_index_path.exists():
        write_candidate_index(candidates_dir, candidate_index_path)
    index = read_json(candidate_index_path) if candidate_index_path.exists() else {"candidate_count": 0}
    hindsight = read_hindsight(memory_dir)
    diversity = read_diversity(memory_dir)
    hardware = read_hardware_profile(memory_dir)
    backend = read_backend_profile(memory_dir)
    external_review = read_external_review(memory_dir)

    top_outcomes = {str(item.get("label", "")): int(item.get("count", 0)) for item in hindsight.get("top_outcomes", [])}
    top_failure_modes = {str(item.get("label", "")): int(item.get("count", 0)) for item in hindsight.get("top_failure_modes", [])}
    policy_adjustments = [str(item) for item in hindsight.get("policy_adjustments", []) if str(item).strip()]
    over_explored = hindsight.get("over_explored_mechanisms", [])
    under_explored = hindsight.get("under_explored_promising_mechanisms", [])
    over_backend = hindsight.get("over_explored_backend_fingerprints", [])
    under_backend = hindsight.get("under_explored_backend_fingerprints", [])

    selection_mode = "balanced"
    cooldown_multiplier = 1.0
    underexplored_bonus = 20
    backend_fingerprint_bonus = 10
    backend_fingerprint_cooldown = 12
    publish_every_cycles = 1
    novelty_cycle_priority = "normal"
    summary = "Use a balanced policy until stronger hindsight accumulates."
    evidence: list[str] = []

    if under_explored:
        selection_mode = "exploit_underexplored"
        underexplored_bonus = 30
        summary = "Bias the lab toward under-explored promising mechanisms."
        evidence.append("policy:underexplored_promising")
    if over_explored:
        cooldown_multiplier = 1.5
        summary = "Increase cooldown pressure on over-explored mechanisms while favoring promising lines."
        evidence.append("policy:overexplored_cooldown")
    if over_backend:
        backend_fingerprint_cooldown = 18
        summary = "Cool down backend change types that hindsight says have been over-explored."
        evidence.append("policy:backend_fingerprint_cooldown")
    if under_backend:
        backend_fingerprint_bonus = 16
        if selection_mode == "balanced":
            summary = "Bias the lab toward backend science changes that hindsight says were under-explored but promising."
        evidence.append("policy:backend_fingerprint_bonus")
    if top_outcomes.get("train_error", 0) >= 1 or top_failure_modes.get("trace_capture_gap", 0) >= 1:
        selection_mode = "stabilize"
        cooldown_multiplier = max(cooldown_multiplier, 1.8)
        backend_fingerprint_cooldown = max(backend_fingerprint_cooldown, 20)
        publish_every_cycles = 1
        summary = "Stabilize the lab after brittle outcomes before pushing wider exploration."
        evidence.append("policy:stabilize_after_errors")
    elif top_outcomes.get("dead_end", 0) >= 3:
        publish_every_cycles = 2
        evidence.append("policy:slower_publish_for_dead_ends")
    if bool(diversity.get("novelty_step_recommended")):
        novelty_cycle_priority = "high"
        publish_every_cycles = 1
        summary = "A novelty cycle is due; publish and surface the next branch shift immediately."
        evidence.append("policy:novelty_cycle_priority")

    environment_hint = str(hardware.get("environment_hint", "")).strip()
    preferred_runner_backend = "simulated"
    if bool(backend.get("command_backend_configured")):
        preferred_runner_backend = "command"
        summary = "Use the configured command backend so the lab learns from real execution traces."
        evidence.append("policy:command_backend_preferred")
    elif environment_hint == "local_macos":
        preferred_runner_backend = "simulated"
        evidence.append("policy:local_backend_simulated")

    # --- Import 2 & 5: process classification and throughput signals ---
    process_stats = hindsight.get("process_classification_counts", {})
    stalled_count = int(process_stats.get("stalled", 0))
    crashed_count = int(process_stats.get("crashed_early", 0))
    if stalled_count >= 2:
        selection_mode = "stabilize"
        cooldown_multiplier = max(cooldown_multiplier, 2.0)
        summary = "Multiple stalled processes detected; stabilize and investigate backend health."
        evidence.append("policy:stale_process_pressure")
    if crashed_count >= 2:
        cooldown_multiplier = max(cooldown_multiplier, 1.5)
        summary = "Multiple early crashes detected; prefer safer follow-ups."
        evidence.append("policy:crash_pressure")

    throughput_summary = hindsight.get("throughput_summary", {})
    avg_saved = float(throughput_summary.get("avg_time_saved", 0))
    if avg_saved > 60:
        evidence.append("policy:efficient_polling")
    avg_wall = float(throughput_summary.get("avg_wall_clock", 0))
    if avg_wall > 0 and avg_saved / max(avg_wall, 1) < 0.05:
        evidence.append("policy:low_polling_savings")

    if policy_adjustments:
        summary = policy_adjustments[0]
    if str(external_review.get("status", "")) == "reviewed" and external_review.get("lab_advice"):
        summary = str(external_review.get("situation_summary", summary)) or summary
        evidence.append("policy:external_review_active")

    payload = {
        "summary": summary,
        "selection_mode": selection_mode,
        "cooldown_multiplier": cooldown_multiplier,
        "underexplored_bonus": underexplored_bonus,
        "backend_fingerprint_bonus": backend_fingerprint_bonus,
        "backend_fingerprint_cooldown": backend_fingerprint_cooldown,
        "preferred_runner_backend": preferred_runner_backend,
        "publish_every_cycles": publish_every_cycles,
        "novelty_cycle_priority": novelty_cycle_priority,
        "policy_adjustments": policy_adjustments[:5],
        "evidence": evidence,
        "candidate_count": int(index.get("candidate_count", 0)),
        "hardware_context": hardware,
        "backend_context": backend,
        "external_review_context": {
            "status": external_review.get("status", ""),
            "trigger_reason": external_review.get("trigger_reason", ""),
            "reviewer": external_review.get("reviewer", ""),
        },
        "hindsight_summary": hindsight.get("summary", ""),
        "diversity_summary": diversity.get("summary", ""),
    }
    if str(os.environ.get("HARNESS_LAB_LLM_POLICY_ENABLED", "")).strip().lower() in {"1", "true", "yes"}:
        llm_payload = run_claude_json(
            _llm_policy_prompt(index, hindsight, diversity, hardware, backend, external_review, payload),
            cwd=candidates_dir.parent.parent,
        )
        normalized = _normalize_llm_policy_payload(llm_payload or {}, payload)
        if normalized:
            return normalized
    return payload


def write_policy(candidates_dir: Path, memory_dir: Path, output_path: Path | None = None) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    write_backend_profile(memory_dir)
    path = output_path or (memory_dir / "policy.json")
    write_json(path, build_policy(candidates_dir, memory_dir))
    return path


def read_policy(memory_dir: Path) -> dict:
    path = memory_dir / "policy.json"
    if not path.exists():
        return default_policy()
    return json.loads(path.read_text(encoding="utf-8"))
