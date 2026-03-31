# Next Change

- summary: `Current priority is `evaluation` with selection mode `stabilize`.`
- recommended_action: `targeted_mutation`
- target_module: `science_model`

## Problem
- `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit. Current science-debug issue: vram_headroom.`

## Options
- [Recommended] `Mutate science_model`: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.039262.`
- [Option] `Wait for more data`: `Recent evidence may still be too thin or too noisy; a few more scored candidates could produce a cleaner signal.`

## Evidence
- `artifacts/memory/hindsight.json`
- `artifacts/memory/science_summary.json`
- `artifacts/memory/backend_module_summary.json`

## Guardrails
- `This brief does not authorize or trigger code changes by itself.`
- `Prefer one explicit backend module over broad multi-file edits.`
- `Preserve real science backend execution, traces, and fallback behavior.`
- `Use focused tests plus one real candidate run for verification.`

## Verification
- `Run focused tests for the target module and adjacent seams.`
- `Verify py_compile passes for touched files.`
- `Confirm the next candidate writes real science traces instead of fallback artifacts.`

## Note
- `This brief is generated for review only. It does not authorize or trigger code changes by itself.`
