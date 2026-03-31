from __future__ import annotations

import json
from pathlib import Path

from harness_lab.backend import read_backend_profile, write_backend_profile
from harness_lab.diversity import read_diversity
from harness_lab.hardware import read_hardware_profile
from harness_lab.hindsight import read_hindsight
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


def build_policy(candidates_dir: Path, memory_dir: Path) -> dict:
    candidate_index_path = memory_dir / "candidate_index.json"
    if not candidate_index_path.exists():
        write_candidate_index(candidates_dir, candidate_index_path)
    index = read_json(candidate_index_path) if candidate_index_path.exists() else {"candidate_count": 0}
    hindsight = read_hindsight(memory_dir)
    diversity = read_diversity(memory_dir)
    hardware = read_hardware_profile(memory_dir)
    backend = read_backend_profile(memory_dir)

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

    if policy_adjustments:
        summary = policy_adjustments[0]

    return {
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
        "hindsight_summary": hindsight.get("summary", ""),
        "diversity_summary": diversity.get("summary", ""),
    }


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
