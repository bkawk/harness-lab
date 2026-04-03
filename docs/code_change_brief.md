# Code Change Brief

- summary: Current priority is `module_surface` with selection mode `stabilize`.
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- target_file: `src/harness_lab/science_loss.py`

## Target Functions
- `compute_instance_loss`
- `compute_loss`

## Problem
- Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.

## Why This Module
- Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.

## Code Hypothesis
- The current transfer problem is more likely to improve through stronger transfer-sensitive loss pressure than through changing evaluation thresholds alone.

## Decision State
- `iterate`
- `science_loss` is already the active recent seam with outcomes ['keeper', 'dead_end', 'audit_blocked'], so keep iterating on that line rather than issuing a brand-new brief.

## Proposed Change
- Increase transfer-sensitive boundary or instance pressure modestly, for example by strengthening boundary_loss_weight or instance_margin, without changing eval thresholds.

## Execution Contract
- Add, remove, or refactor code within the target module when that is the smallest clean way to express the bounded change.
- Add or update adjacent focused tests that directly cover the target module change.

## Scope Limits
- Keep the write scope to `science_loss` plus adjacent focused tests unless the brief explicitly names another seam.
- Do not turn a bounded module change into a multi-module refactor in the same patch.

## Do Not Change
- Do not change science_eval thresholds in the same patch.
- Do not broaden into model architecture rewrites or dataset changes.
- Do not rewrite these fixed surfaces in the same patch: Cross-entropy plus smooth-L1 plus BCE loss recipe; Instance similarity and same-class negative construction; Loss-term composition order.

## Acceptance Checks
- The loss change remains bounded to transfer-sensitive pressure and does not silently rewrite evaluation logic.
- The next real candidate should produce clearer transfer behavior without breaking trace emission or outcome writing.

## Focused Tests
- `tests/test_science_loss.py`

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
- `artifacts/memory/candidate_index.json`
- `artifacts/memory/hindsight.json`
- `artifacts/memory/policy.json`
- `artifacts/memory/backend_module_summary.json`
- `src/harness_lab/science_loss.py`
- `failure_to_code:boundary_smoke:gap_too_wide`

## Note
- This brief is generated for review only. It should sharpen code-change planning, not authorize autonomous code edits.
