# Next Change

- summary: Current priority is `vram_headroom` with selection mode `stabilize`.
- recommended_action: `targeted_mutation`
- target_module: `science_train`

## Problem
- Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.

## Why This Module
- The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.

## Secondary Context
- Recent real-backend runs are only using about 807.5 MB on average, leaving most VRAM unused. 7 scored candidate(s) have landed since structural commit `d21d25b`.

## Options
- [Recommended] Mutate science_train: The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.
- [Option] Wait on broad mutation: Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Evidence
- `artifacts/memory/science_debug_summary.json`
- `artifacts/memory/hardware_profile.json`
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
