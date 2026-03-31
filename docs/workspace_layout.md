# Workspace Layout

`harness-lab` treats the candidate workspace as the primary research object.

Each candidate gets a self-contained filesystem bundle:

```text
artifacts/candidates/<candidate_id>/
  workspace.json
  proposal.json
  source/
  patches/
  traces/
  benchmark/
  execution/
    plan.json
  audit/
  outcome/
    result.json
  diagnosis/
    summary.json
  memory/
    bootstrap_snapshot.json
```

## Purpose Of Each Directory

- `source/`
  - source snapshot or selected source files for the candidate
  - includes `manifest.json` plus a copied `repo_snapshot/` tree
- `patches/`
  - diffs against the parent candidate or baseline
  - includes `summary.json` and `against_parent.patch`
- `traces/`
  - raw execution logs, tool traces, and agent traces
  - includes backend command metadata in `run.json`
- `benchmark/`
  - benchmark outputs and scalar metrics
- `execution/`
  - execution plan, evidence collection steps, and success criteria
- `audit/`
  - larger-set or cross-condition evaluation outputs
- `outcome/`
  - structured result of benchmark and audit execution
- `diagnosis/`
  - structured failure analysis and counterfactual notes
- `memory/`
  - links or exports from cross-run synthesis and prior evidence
  - includes `bootstrap_snapshot.json`, a compact scientific situation report for the candidate

## Minimal Files

- `workspace.json`
  - identity and path layout for the candidate bundle
- `proposal.json`
  - the proposed harness change and expected failure mode addressed
- `execution/plan.json`
  - how the candidate should be benchmarked, audited, and traced
- `outcome/result.json`
  - what actually happened after execution
- `diagnosis/summary.json`
  - structured diagnosis stub or completed diagnosis

The intended loop is now:

```text
proposal -> source snapshot -> parent diff -> execution plan -> raw traces -> outcome -> diagnosis reconciliation -> memory index
```

## Initial Command

Create a candidate workspace with:

```bash
PYTHONPATH=src python3 scripts/create_candidate.py cand_0001
```

This is the first concrete step toward a filesystem-native Meta-Harness style loop.
