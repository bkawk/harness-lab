from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

from harness_lab.backend import read_backend_profile
from harness_lab.budget import read_budget
from harness_lab.hindsight import read_hindsight
from harness_lab.human_feedback import read_human_feedback
from harness_lab.memory import read_json
from harness_lab.policy import read_policy
from harness_lab.workspace import write_json


def mutation_brief_path(memory_dir: Path) -> Path:
    return memory_dir / "mutation_brief.json"


def next_change_markdown_path(repo_dir: Path) -> Path:
    return repo_dir / "docs" / "next_change.md"


def _failure_mode_target(hindsight: dict, top_request: dict) -> tuple[str, str] | None:
    recent_failures = [
        str(item.get("label", "")).strip()
        for item in hindsight.get("recent_top_failure_modes", [])
        if str(item.get("label", "")).strip()
    ]
    top_request_kind = str(top_request.get("kind", "")).strip()
    if any(label in {"boundary_transfer_weak", "boundary_smoke:gap_too_wide", "audit_boundary_f1_weak"} for label in recent_failures):
        return "science_loss", "Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust."
    if any(label in {"transfer_smoke:gap_too_wide", "transfer_smoke_score_below_floor", "hard_transfer_smoke:gap_too_wide"} for label in recent_failures):
        return "science_eval", "Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target."
    if any(label in {"transfer_collapse", "transfer_regression", "hard_transfer_regression", "local_only_gain"} for label in recent_failures):
        return "science_model", "Recent failures point to transfer behavior that likely depends on model capacity and representation quality."
    if top_request_kind == "vram_headroom":
        return "science_train", "The top live pressure is unused VRAM headroom, so a bounded batch-size move is the best next target before larger architectural jumps."
    return None


def _pick_target_module(memory_dir: Path, hindsight: dict, top_request: dict) -> tuple[str, str]:
    failure_target = _failure_mode_target(hindsight, top_request)
    if failure_target is not None:
        return failure_target
    module_summary = read_json(memory_dir / "backend_module_summary.json") if (memory_dir / "backend_module_summary.json").exists() else {}
    modules = list(module_summary.get("modules", []))
    if not modules:
        return "science_backend", "No split backend module has enough evidence yet."
    chosen = modules[0]
    if str(chosen.get("module", "")).strip() == "science_backend":
        for item in modules[1:]:
            if str(item.get("module", "")).strip():
                chosen = item
                break
    module_name = str(chosen.get("module", "")).strip() or "science_backend"
    gap = chosen.get("avg_transfer_gap")
    if isinstance(gap, (int, float)):
        return module_name, f"Recent backend edits are concentrated in `{module_name}` with average transfer gap {float(gap):.6f}."
    return module_name, f"Recent backend edits are concentrated in `{module_name}`."


def _build_problem_statement(top_request: dict, hindsight: dict) -> str:
    return (
        str(top_request.get("summary", "")).strip()
        or str(hindsight.get("summary", "")).strip()
        or "No dominant mutation target yet."
    )


def _build_module_rationale(module_rationale: str, likely_issue: str) -> str:
    if not likely_issue:
        return module_rationale
    if likely_issue == "vram_headroom":
        return f"{module_rationale} Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation."
    return f"{module_rationale} Secondary signal: current science-debug issue is `{likely_issue}`, but it is not the main reason for this recommendation."


def _last_structural_commit(repo_dir: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--format=%H%x09%s", "-50"],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return ""
    for line in result.stdout.splitlines():
        sha, _, subject = line.partition("\t")
        title = subject.strip()
        if not sha or not title:
            continue
        if title.startswith("big-bang:"):
            continue
        return sha.strip()
    return ""


def _commit_timestamp(repo_dir: Path, commit_sha: str) -> datetime | None:
    if not commit_sha:
        return None
    try:
        result = subprocess.run(
            ["git", "show", "-s", "--format=%cI", commit_sha],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    text = result.stdout.strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def _scored_candidates_since_commit(memory_dir: Path, commit_sha: str, *, repo_dir: Path) -> list[dict]:
    index_path = memory_dir / "candidate_index.json"
    if not commit_sha or not index_path.exists():
        return []
    commit_time = _commit_timestamp(repo_dir, commit_sha)
    if commit_time is None:
        return []
    index = read_json(index_path)
    items: list[dict] = []
    for candidate in index.get("candidates", []):
        benchmark = candidate.get("benchmark_score")
        audit = candidate.get("audit_score")
        if benchmark is None and audit is None:
            continue
        created_at = str(candidate.get("created_at", "")).strip()
        if not created_at:
            continue
        try:
            created_time = datetime.fromisoformat(created_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            continue
        if created_time > commit_time:
            items.append(candidate)
    return items


def build_mutation_brief(candidates_dir: Path, memory_dir: Path) -> dict:
    min_scored_candidates_after_change = 3
    human_feedback = read_human_feedback(memory_dir)
    hindsight = read_hindsight(memory_dir)
    policy = read_policy(memory_dir)
    budget = read_budget(memory_dir)
    backend = read_backend_profile(memory_dir)
    science_summary = read_json(memory_dir / "science_summary.json") if (memory_dir / "science_summary.json").exists() else {}
    science_debug = read_json(memory_dir / "science_debug_summary.json") if (memory_dir / "science_debug_summary.json").exists() else {}
    backend_module_summary = read_json(memory_dir / "backend_module_summary.json") if (memory_dir / "backend_module_summary.json").exists() else {}

    top_request = next(iter(human_feedback.get("items", [])), {})
    target_module, module_rationale = _pick_target_module(memory_dir, hindsight, top_request)
    likely_issue = str(science_debug.get("likely_issue", "")).strip()
    problem_statement = _build_problem_statement(top_request, hindsight)
    module_rationale = _build_module_rationale(module_rationale, likely_issue)
    repo_dir = memory_dir.parent.parent
    last_structural_commit = _last_structural_commit(repo_dir)
    scored_since_change = _scored_candidates_since_commit(memory_dir, last_structural_commit, repo_dir=repo_dir)
    enough_recent_signal = len(scored_since_change) >= min_scored_candidates_after_change
    scored_since_change_note = (
        f"{len(scored_since_change)} scored candidate(s) have landed since structural commit `{last_structural_commit[:7]}`."
        if last_structural_commit
        else "The last structural change could not be identified, so recent-signal gating is conservative."
    )
    if not enough_recent_signal:
        module_rationale = (
            f"{module_rationale} Hold off on broad mutation until the post-change sample is less thin. "
            f"Small conservative lever nudges are still allowed. {scored_since_change_note}"
        )
    wait_reason = (
        f"Only {len(scored_since_change)} scored candidate(s) have landed since the last structural change; "
        f"wait on broad mutation until at least {min_scored_candidates_after_change} post-change scored candidates exist, "
        "but conservative lever nudges are still allowed."
        if last_structural_commit and not enough_recent_signal
        else "Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate."
    )

    supporting_evidence = [str(item) for item in top_request.get("evidence", [])[:5]]
    if not supporting_evidence and science_debug:
        supporting_evidence.append("artifacts/memory/science_debug_summary.json")
    if backend_module_summary:
        supporting_evidence.append("artifacts/memory/backend_module_summary.json")
    supporting_evidence = list(dict.fromkeys(supporting_evidence))

    return {
        "summary": (
            f"Current priority is `{str(top_request.get('kind', '') or 'unknown')}` with selection mode `{policy.get('selection_mode', '') or 'unknown'}`."
            if enough_recent_signal
            else f"Current priority is `{str(top_request.get('kind', '') or 'unknown')}`, but only {len(scored_since_change)} scored candidate(s) have landed since the last structural change, so broad mutation should wait while conservative lever nudges remain allowed."
        ),
        "recommended_action": "targeted_mutation" if enough_recent_signal else "wait",
        "target_module": target_module,
        "last_structural_commit": last_structural_commit,
        "scored_candidates_since_change": len(scored_since_change),
        "problem_statement": problem_statement,
        "module_rationale": module_rationale,
        "science_trend_summary": str(science_summary.get("trend_summary", "")).strip(),
        "science_debug_summary": (
            f"{str(science_debug.get('summary', '')).strip()} {scored_since_change_note}".strip()
            if str(science_debug.get("summary", "")).strip()
            else scored_since_change_note
        ),
        "supporting_evidence": supporting_evidence,
        "guardrails": [
            "This brief does not authorize or trigger code changes by itself.",
            "Prefer one explicit backend module over broad multi-file edits.",
            "Preserve real science backend execution, traces, and fallback behavior.",
            "Use focused tests plus one real candidate run for verification.",
        ],
        "verification_plan": [
            "Run focused tests for the target module and adjacent seams.",
            "Verify py_compile passes for touched files.",
            "Confirm the next candidate writes real science traces instead of fallback artifacts.",
        ],
        "context": {
            "human_feedback_top": top_request,
            "hindsight_summary": hindsight.get("summary", ""),
            "policy_summary": policy.get("summary", ""),
            "budget_summary": budget.get("summary", ""),
            "backend_summary": backend.get("summary", ""),
            "backend_module_summary": backend_module_summary,
            "last_structural_commit": last_structural_commit,
            "scored_candidates_since_change": len(scored_since_change),
        },
        "options": [
            {
                "kind": "targeted_mutation",
                "title": f"Mutate {target_module}",
                "recommended": enough_recent_signal,
                "why": module_rationale,
            },
            {
                "kind": "wait",
                "title": "Wait on broad mutation",
                "recommended": not enough_recent_signal,
                "why": wait_reason,
            },
        ],
    }


def write_mutation_brief(candidates_dir: Path, memory_dir: Path) -> Path:
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = mutation_brief_path(memory_dir)
    write_json(path, build_mutation_brief(candidates_dir, memory_dir))
    return path


def render_next_change_markdown(repo_dir: Path, memory_dir: Path) -> Path:
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    path = next_change_markdown_path(repo_dir)
    brief = read_json(mutation_brief_path(memory_dir)) if mutation_brief_path(memory_dir).exists() else {}
    option_lines = [
        f"- {'[Recommended]' if item.get('recommended') else '[Option]'} {item.get('title', '')}: {item.get('why', '')}"
        for item in brief.get("options", [])
    ] or ["- [Option] Wait for more data: No mutation brief has been generated yet."]
    evidence_lines = [f"- `{item}`" for item in brief.get("supporting_evidence", [])[:6]] or ["- `No supporting evidence recorded yet.`"]
    guardrail_lines = [f"- {item}" for item in brief.get("guardrails", [])[:6]] or ["- No guardrails recorded yet."]
    verification_lines = [f"- {item}" for item in brief.get("verification_plan", [])[:6]] or ["- No verification plan recorded yet."]
    content = "\n".join(
        [
            "# Next Change",
            "",
            f"- summary: {brief.get('summary', 'No mutation brief generated yet.')}",
            f"- recommended_action: `{brief.get('recommended_action', 'wait')}`",
            f"- target_module: `{brief.get('target_module', '-') or '-'}`",
            "",
            "## Problem",
            f"- {brief.get('problem_statement', 'No problem statement yet.')}",
            "",
            "## Why This Module",
            f"- {brief.get('module_rationale', 'No module rationale yet.')}",
            "",
            "## Secondary Context",
            f"- {brief.get('science_debug_summary', 'No secondary science-debug context recorded yet.') or 'No secondary science-debug context recorded yet.'}",
            "",
            "## Options",
            *option_lines,
            "",
            "## Evidence",
            *evidence_lines,
            "",
            "## Guardrails",
            *guardrail_lines,
            "",
            "## Verification",
            *verification_lines,
            "",
            "## Note",
            "- This brief is generated for review only. It does not authorize or trigger code changes by itself.",
        ]
    )
    path.write_text(content + "\n", encoding="utf-8")
    return path
