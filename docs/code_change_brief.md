# Code Change Brief

- summary: Current priority is `evaluation`, but only 0 scored candidate(s) have landed since the last structural change, so broad mutation should wait while conservative lever nudges remain allowed.
- recommended_action: `wait`
- target_module: `science_model`
- target_file: `src/harness_lab/science_model.py`

## Target Functions
- `CompactPointModel.__init__`
- `CompactPointModel.forward`
- `knn_indices`
- `gather_neighbors`

## Problem
- Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.

## Why This Module
- Recent failures point to transfer behavior that likely depends on model capacity and representation quality. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.

## Code Hypothesis
- The current transfer problem is more likely to improve through representation-capacity or local-context changes than through threshold-only evaluation changes.

## Decision State
- `wait`
- Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Proposed Change
- Increase or rebalance representation capacity in a narrow way, such as local-context width or neighborhood strength, without touching smoke thresholds or runner behavior.

## Execution Contract
- Add, remove, or refactor code within the target module when that is the smallest clean way to express the bounded change.
- Add or update adjacent focused tests that directly cover the target module change.

## Scope Limits
- Keep the write scope to `science_model` plus adjacent focused tests unless the brief explicitly names another seam.
- Do not turn a bounded module change into a multi-module refactor in the same patch.

## Do Not Change
- Do not change science_eval smoke thresholds in the same patch.
- Do not alter runner wall-clock or fallback behavior.
- Do not rewrite these fixed surfaces in the same patch: Point encoder and classifier topology; Fusion layout combining point, local, and global features; Instance pathway structure and normalization.

## Acceptance Checks
- The target module still produces real science traces and completes benchmark/smoke/audit in the normal backend path.
- The change remains bounded to model-capacity or local-context behavior rather than broad training-policy changes.

## Focused Tests
- `tests/test_science_model.py`

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
- `artifacts/memory/hindsight.json`
- `artifacts/memory/science_summary.json`
- `artifacts/memory/backend_module_summary.json`
- `src/harness_lab/science_model.py`
- `failure_to_code:boundary_smoke:gap_too_wide`

## Note
- This brief is generated for review only. It should sharpen code-change planning, not authorize autonomous code edits.
