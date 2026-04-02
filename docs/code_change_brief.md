# Code Change Brief

- summary: Current priority is `evaluation`, but only 0 scored candidate(s) have landed since the last structural change, so broad mutation should wait while conservative lever nudges remain allowed.
- recommended_action: `wait`
- target_module: `science_loss`
- target_file: `src/harness_lab/science_loss.py`

## Target Functions
- `compute_instance_loss`
- `compute_loss`

## Problem
- Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.

## Why This Module
- Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 0 scored candidate(s) have landed since structural commit `8eb05e7`.

## Proposed Change
- Adjust transfer-sensitive loss pressure in a bounded way so boundary and instance structure hold up better on transfer slices.

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

## Wait Option
- Wait on broad mutation: Only 0 scored candidate(s) have landed since the last structural change; wait on broad mutation until at least 3 post-change scored candidates exist, but conservative lever nudges are still allowed.

## Evidence
- `artifacts/memory/hindsight.json`
- `artifacts/memory/science_summary.json`
- `artifacts/memory/backend_module_summary.json`
- `src/harness_lab/science_loss.py`

## Note
- This brief is generated for review only. It should sharpen code-change planning, not authorize autonomous code edits.
