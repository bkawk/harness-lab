from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from harness_lab.abc_dataset import ensure_prepared_dataset
from harness_lab.backend import write_backend_profile
from harness_lab.loop import LoopResult, advance_candidate_loop
from harness_lab.policy import read_policy
from harness_lab.publisher import PublishResult, publish_repo_snapshot

GENESIS_CANDIDATE_ID = "cand_0001"


def next_candidate_id(candidates_dir: Path) -> str:
    candidates_dir.mkdir(parents=True, exist_ok=True)
    max_index = 0
    for path in candidates_dir.iterdir():
        if (
            not path.is_dir()
            or not (path / "workspace.json").exists()
            or not (path / "proposal.json").exists()
        ):
            continue
        name = path.name
        if not name.startswith("cand_"):
            continue
        suffix = name.split("cand_", 1)[1]
        if suffix.isdigit():
            max_index = max(max_index, int(suffix))
    return f"cand_{max_index + 1:04d}"


def candidate_count(candidates_dir: Path) -> int:
    count = 0
    if not candidates_dir.exists():
        return 0
    for path in candidates_dir.iterdir():
        if path.is_dir() and (path / "workspace.json").exists():
            count += 1
    return count


def ensure_seed_candidate(repo_dir: Path, candidates_dir: Path, prepared_dataset_id: str) -> str:
    if candidate_count(candidates_dir) > 0:
        return "existing"
    return "genesis_ready"


@dataclass(frozen=True)
class LabStepResult:
    candidate_id: str
    dataset_action: str
    dataset_id: str
    seed_action: str
    loop: LoopResult
    published: bool
    publish_message: str
    commit_sha: str | None


def run_lab_step(
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
    candidate_id: str | None = None,
    parent_id: str | None = None,
    finalize_outcome: bool = True,
    simulate_outcome: bool = True,
    runner_backend: str = "simulated",
    publish: bool = False,
    publish_message: str | None = None,
) -> LabStepResult:
    dataset_payload = ensure_prepared_dataset(
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
    )
    write_backend_profile(memory_dir)
    seed_action = ensure_seed_candidate(repo_dir, candidates_dir, prepared_dataset_id)
    policy = read_policy(memory_dir)
    effective_runner_backend = runner_backend
    if runner_backend == "auto":
        effective_runner_backend = str(policy.get("preferred_runner_backend", "simulated") or "simulated")

    chosen_candidate_id = candidate_id or next_candidate_id(candidates_dir)
    loop = advance_candidate_loop(
        repo_dir,
        candidates_dir,
        memory_dir,
        chosen_candidate_id,
        parent_id=parent_id,
        finalize_outcome=finalize_outcome,
        simulate_outcome=simulate_outcome,
        runner_backend=effective_runner_backend,
    )

    publish_result = PublishResult(
        created_commit=False,
        pushed=False,
        commit_sha=None,
        message="Publishing skipped.",
    )
    if publish:
        message = publish_message or f"Advance lab with {chosen_candidate_id}"
        publish_result = publish_repo_snapshot(repo_dir, message)

    record = dataset_payload.get("record", {})
    return LabStepResult(
        candidate_id=chosen_candidate_id,
        dataset_action=str(dataset_payload.get("action", "")),
        dataset_id=str(record.get("dataset_id", prepared_dataset_id)),
        seed_action=seed_action,
        loop=loop,
        published=publish_result.pushed,
        publish_message=publish_result.message,
        commit_sha=publish_result.commit_sha,
    )
