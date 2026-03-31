# Proposal Schema

`harness-lab` proposals should not be blank placeholders. They should carry forward the causal story from memory and diagnosis into the next candidate.

Each candidate keeps its proposal at:

```text
artifacts/candidates/<candidate_id>/proposal.json
```

## Core Fields

- `candidate_id`
- `parent_id`
- `status`
  - `draft`
  - `candidate`
  - later:
    - `provisional`
    - `curated`
- `rationale`
  - concise explanation of why this follow-up exists
- `target`
  - `harness_component`
  - `expected_failure_mode`
  - `novelty_basis`
- `changes`
  - structured list of proposed interventions
- `memory_context`
  - explicit evidence carried in from prior candidates

## Initial Drafting Rule

The first proposal engine is intentionally simple:

- choose a parent from diagnosed history
- rank parent candidates explicitly through synthesis
- read its diagnosis summary and counterfactuals
- build proposal changes from those counterfactuals
- attach a novelty basis grounded in the candidate index

That makes proposal generation:

- filesystem-native
- evidence-linked
- reproducible

## Initial CLI

Draft the next proposal with:

```bash
PYTHONPATH=src python3 scripts/draft_proposal.py cand_0002
```

Optionally force a parent:

```bash
PYTHONPATH=src python3 scripts/draft_proposal.py cand_0003 --parent-id cand_0001
```
