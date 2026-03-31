# Reconciliation

`harness-lab` should not depend on a human to manually translate execution outcomes back into diagnosis.

The reconciliation step updates:

- `diagnosis/summary.json`

from:

- `outcome/result.json`
- `proposal.json`

## What It Does

- maps outcome labels into diagnosis severity
- carries benchmark and audit summaries into a new causal summary
- updates failure modes from observed execution failures
- preserves or seeds counterfactual next steps

## Initial CLI

```bash
PYTHONPATH=src python3 scripts/reconcile_diagnosis.py cand_0002
```
