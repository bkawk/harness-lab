# Next Change

- summary: Current priority is `evaluation`, but only 0 scored candidate(s) have landed since the last structural change.
- recommended_action: `wait`
- target_module: `science_model`

## Problem
- Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.

## Why This Module
- Recent backend edits are concentrated in `science_model` with average transfer gap 0.038046. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.

## Secondary Context
- Recent real-backend runs are only using about 590.4 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.

## Options
- [Option] Mutate science_model: Recent backend edits are concentrated in `science_model` with average transfer gap 0.038046. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.
- [Recommended] Wait for more data: Only 0 scored candidate(s) have landed since the last structural change; wait until at least 5 post-change scored candidates exist.

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
