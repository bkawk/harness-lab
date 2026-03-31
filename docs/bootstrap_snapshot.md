# Bootstrap Snapshot

`harness-lab` now gives each new candidate a compact scientific situation report before proposal drafting.

The artifact lives at:

- `artifacts/candidates/<candidate_id>/memory/bootstrap_snapshot.json`

It is the closest direct analogue to the Meta-Harness environment bootstrap idea, but adapted to research:

- current dataset context
- science leaders and trend summary
- hindsight summary
- policy, budget, and diversity summaries
- backend and hardware context
- bounded external review status
- recent candidate outcomes
- current mechanism and backend-fingerprint counts

This lets a new candidate begin from a strong local picture instead of rediscovering the lab state indirectly.

Write one manually with:

```bash
PYTHONPATH=src python3 scripts/build_bootstrap_snapshot.py cand_0002 --dataset-id abc_boundary512
```
