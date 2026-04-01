# Next Change

- summary: Current priority is `non_self_evolving` with selection mode `stabilize`.
- recommended_action: `targeted_mutation`
- target_module: `science_loss`

## Problem
- Consider strengthening the non-self-evolving seed around `hard_transfer_regression` if that failure mode keeps dominating.

## Why This Module
- Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.

## Secondary Context
- Recent real-backend runs are only using about 601.9 MB on average, leaving most VRAM unused. 6 scored candidate(s) have landed since structural commit `a225c8b`.

## Options
- [Recommended] Mutate science_loss: Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.
- [Option] Wait on broad mutation: Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.

## Evidence
- `artifacts/memory/candidate_index.json`
- `artifacts/memory/hindsight.json`
- `artifacts/memory/policy.json`
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
