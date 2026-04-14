# Code Change Brief

- summary: Current priority is `evaluation`, but only 0 scored candidate(s) have landed since the last structural change, so broad mutation should wait while conservative lever nudges remain allowed.
- recommended_action: `wait`
- target_module: `science_eval`
- target_file: `src/harness_lab/science_eval.py`

## Target Functions
- `should_run_full_audit`
- `classify_smoke_block`
- `classify_outcome`

## Problem
- Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.

## Why This Module
- Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.

## Code Hypothesis
- The current problem is more likely to improve through sharper smoke/audit discrimination than through changing model or loss pressure first.

## Decision State
- `wait`
- Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Proposed Change
- Tighten or clarify smoke and audit classification so severe non-robustness fails earlier while borderline promising runs remain distinguishable.

## Execution Contract
- Add, remove, or refactor code within the target module when that is the smallest clean way to express the bounded change.
- Add or update adjacent focused tests that directly cover the target module change.

## Scope Limits
- Keep the write scope to `science_eval` plus adjacent focused tests unless the brief explicitly names another seam.
- Do not turn a bounded module change into a multi-module refactor in the same patch.

## Do Not Change
- Do not change model or loss behavior in the same patch.
- Do not modify dataset preparation or runner backend behavior.
- Do not rewrite these fixed surfaces in the same patch: Hard-fail rules for severe smoke regressions; Keeper/improved/audit_blocked/dead_end classification bands; Primary failure-mode attribution ordering.

## Acceptance Checks
- The eval change distinguishes severe failures earlier without collapsing moderate candidates into dead_end too aggressively.
- Smoke and audit traces should still be written normally for eligible candidates.

## Focused Tests
- `tests/test_science_smoke_gate.py`
- `tests/test_science_eval.py`

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
- `src/harness_lab/science_eval.py`
- `failure_to_code:boundary_smoke:gap_too_wide`

## Note
- This brief is generated for review only. It should sharpen code-change planning, not authorize autonomous code edits.
