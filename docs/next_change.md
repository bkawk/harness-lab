# Next Change

- summary: Current priority is `evaluation`, but only 0 scored candidate(s) have landed since the last structural change, so broad mutation should wait while conservative lever nudges remain allowed.
- recommended_action: `wait`
- target_module: `science_loss`

## Problem
- Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.

## Why This Module
- Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.

## Secondary Context
- Recent real-backend runs are only using about 618.5 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.

## Options
- [Option] Mutate science_loss: Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.
- [Recommended] Wait on broad mutation: Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Evidence
- `artifacts/memory/hindsight.json`
- `artifacts/memory/science_summary.json`
- `artifacts/memory/backend_module_summary.json`

## Guardrails
- This brief does not authorize or trigger code changes by itself.
- Prefer one explicit backend module over broad multi-file edits.
- Preserve real science backend execution, traces, and fallback behavior.
- Use focused tests plus one real candidate run for verification.

## Verification
- Run focused tests for the target module and adjacent seams.
- Verify py_compile passes for touched files.
- Confirm the next candidate writes real science traces instead of fallback artifacts.

## Note
- This brief is generated for review only. It does not authorize or trigger code changes by itself.
