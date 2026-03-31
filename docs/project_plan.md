# Project Plan

## Goal

Build a new research lab oriented around Meta-Harness style optimization:
- the proposer should inspect raw filesystem evidence
- the search target should be the harness, not just a named strategy
- the system should accumulate causal research memory, not only scores

## What We Are Not Doing

We are not copying `mesh-para` wholesale.

We are intentionally not starting with:
- old artifact trees
- old strategy packs
- old monitor assumptions
- old boundary-centric search loops

We will borrow ideas selectively rather than inherit everything.

## Core Principles

1. Full-trace access
- Every candidate should have a workspace containing source, logs, scores, diffs, and audit outputs.

2. Harness-first search
- Search over prompts, evaluation flow, memory selection, audit policy, context management, and model-side changes together.

3. Diagnosis before proposal
- Proposal generation should start from explicit failure analysis grounded in raw traces.

4. Cross-run synthesis
- The lab should synthesize repeated motifs and recurring failure modes across many runs.

5. Promotion with evidence
- New strategies or families should be promoted through measurable gates rather than becoming permanent by accident.

## Initial Architecture

### 1. Candidate Workspace
Each candidate should have a filesystem bundle with:
- source snapshot
- patch/diff against parent
- execution trace
- benchmark result
- audit result
- diagnosis notes

### 2. Proposal Engine
The proposer should consume:
- recent candidate workspaces
- selected historical workspaces
- failure clusters
- promotion memory

It should output:
- proposed harness change
- explicit rationale
- expected failure mode addressed
- novelty vs prior work

### 3. Decision Layer
The manager should rank candidates using:
- expected gain
- uncertainty
- redundancy penalty
- compute cost
- transfer risk

### 4. Memory Layer
Memory should be queryable by:
- failure mode
- touched code region
- audit outcome
- proposal lineage
- harness component

## First Build Steps

1. Define the candidate workspace layout.
2. Build a candidate index so cross-run memory is queryable.
3. Define a structured diagnosis artifact.
4. Add a diagnosis update path so candidates accumulate causal judgment.
5. Define a harness proposal format.
6. Add a proposal drafting path that reads diagnosis and memory.
7. Add a synthesis layer that ranks candidate parents explicitly.
8. Add an execution-plan artifact so candidates carry benchmark and audit intent.
9. Add an outcome artifact so execution writes back structured results.
10. Add reconciliation so outcome evidence feeds diagnosis automatically.
11. Allow controlled self-publishing of tracked lab evolution.
12. Implement a filesystem-native proposer loop.
13. Add a lightweight runner or simulator so the loop can produce outcomes without manual wiring.
14. Separate the loop from specific backends through a runner interface.
15. Make planning and execution hardware-aware so the lab adapts when machines change.
16. Make dataset acquisition, build, and provenance part of the repo, not an implicit side dependency.
17. Add promotion criteria for proposal -> candidate -> curated.
