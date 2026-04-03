# Code Change Brief

- summary: Current priority is `vram_headroom` with selection mode `stabilize`.
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- target_file: `src/harness_lab/science_train.py`

## Target Functions
- `run_training_cycle`
- `write_science_progress`
- `peak_vram_mb`

## Problem
- Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.

## Why This Module
- The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.

## Code Hypothesis
- The current opportunity is more likely to improve through train-side capacity use than through loss or eval changes first.

## Decision State
- `iterate`
- `science_train` is already the active recent seam with outcomes ['keeper', 'dead_end', 'keeper', 'audit_blocked'], so keep iterating on that line rather than issuing a brand-new brief.

## Proposed Change
- Raise bounded train-side capacity, such as batch_size or eval_batch_size, without altering model, loss, or eval semantics.

## Execution Contract
- Add, remove, or refactor code within the target module when that is the smallest clean way to express the bounded change.
- Add or update adjacent focused tests that directly cover the target module change.

## Scope Limits
- Keep the write scope to `science_train` plus adjacent focused tests unless the brief explicitly names another seam.
- Do not turn a bounded module change into a multi-module refactor in the same patch.

## Do Not Change
- Do not change science_eval or loss semantics in the same patch.
- Do not remove progress, metrics, or backend result traces.
- Do not rewrite these fixed surfaces in the same patch: Time-based training schedule and eval reserve discipline; Benchmark -> smoke -> audit execution order; Evidence and trace writing for science outcomes.

## Acceptance Checks
- The train change should visibly alter effective batch/log settings without breaking wall-clock reserve discipline.
- The next candidate should still write progress and result artifacts through the normal command backend.

## Focused Tests
- `tests/test_science_train.py`

## Verification
- Run focused tests for the target module and adjacent seams.
- Verify py_compile passes for touched files.
- Confirm the next candidate writes real science traces instead of fallback artifacts.

## Abort Conditions
- Abort if the change requires touching more than the target module plus adjacent tests.
- Abort if the intended effect cannot be verified with focused tests and one real candidate run.
- Abort if the post-change evidence is still too thin and the wait option is the recommended path.

## Failure Behavior
- Abort the attempt if compile checks or focused tests fail.
- Do not auto-publish or auto-promote a failed attempt.
- Do not silently roll back and hide the failure; instead leave the failed attempt visible to human review.

## Wait Option
- Wait on broad mutation: Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Evidence
- `artifacts/memory/science_debug_summary.json`
- `artifacts/memory/hardware_profile.json`
- `artifacts/memory/backend_module_summary.json`
- `src/harness_lab/science_train.py`
- `failure_to_code:vram_headroom`

## Note
- This brief is generated for review only. It should sharpen code-change planning, not authorize autonomous code edits.
