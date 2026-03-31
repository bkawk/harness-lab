# External Review

`harness-lab` can occasionally ask for bounded outside perspective without turning into an oracle-dependent system.

The artifact lives at:

- `artifacts/memory/external_review.json`

It has two outputs:

- `lab_advice`
  - advice the lab is allowed to incorporate into proposals and policy context
- `human_advice`
  - advice for the non-self-evolving parts that should stay under human review

The trigger is self-directed but budgeted:

- repeated `dead_end`
- repeated `train_error`
- repeated `audit_blocked`
- no keeper after enough candidates
- hindsight exhaustion signals

And it is rate-limited:

- one review every `10` candidates by default

By default the repo ships with a heuristic reviewer so a fresh clone has a working review loop.

Tier 2 adds an optional bounded Claude reviewer ahead of that heuristic fallback.

Enable it with:

- `HARNESS_LAB_LLM_REVIEW_ENABLED=1`

Optional related knobs:

- `HARNESS_LAB_CLAUDE_BIN`
- `HARNESS_LAB_LLM_TIMEOUT_SECONDS`

When enabled, the review fallback chain is:

1. Claude review
2. external review command
3. heuristic review

If you want a real LLM peer-review path later, set:

- `HARNESS_LAB_EXTERNAL_REVIEW_COMMAND`

That command receives paths to:

- `candidate_index.json`
- `hindsight.json`
- `policy.json`
- `science_summary.json`

and should write a JSON result to:

- `HARNESS_LAB_EXTERNAL_REVIEW_RESULT_PATH`

Refresh the artifact manually with:

```bash
PYTHONPATH=src python3 scripts/build_external_review.py
```
