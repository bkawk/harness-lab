# Initial Harness Modularization

## Why This Matters

`initial_harness` is still the dominant scientific basin in `harness-lab`.
The lab keeps revisiting it because most of the real backend science still lives inside one dense file:

- model definition
- local geometry
- local/global fusion
- instance modulation
- loss recipe
- config derivation
- training loop
- transfer smoke gating
- outcome classification

That makes the backend usable, but not yet cleanly evolvable.

The goal of this plan is to turn `initial_harness` from one broad mutable blob into a small set of explicit backend modules that:

- humans can improve deliberately
- Claude can reason about more clearly
- backend fingerprints can track more precisely
- the lab can eventually evolve with less ambiguity

## Current Shape

Today the main implementation lives in:

- [science_backend.py](/Volumes/bkawk/projects/harness-lab/src/harness_lab/science_backend.py)

Within that file, the practical module boundaries already exist conceptually:

1. feature encoder
- `point_encoder`
- `knn_indices`
- `gather_neighbors`
- local edge construction

2. fusion path
- `local_mlp`
- `global_proj`
- fused representation assembly

3. prediction heads
- classifier
- param head
- boundary head
- instance head

4. instance conditioning
- `instance_class_proj`
- `instance_modulation_scale`

5. loss recipe
- classification loss
- parameter regression loss
- boundary loss
- instance contrastive-style loss

6. evaluation / audit gate
- benchmark eval
- multi-slice smoke eval
- audit gating
- outcome classification

7. training/runtime policy
- config derivation
- budget handling
- OOM backoff
- time-budget / eval-reserve handling

These are already the right module seams.
The work is to make them explicit in code.

## Target Module Boundaries

The first modularization pass should create these explicit backend units:

### 1. `science_model.py`

Own:

- model class
- local encoder helpers
- fusion logic
- prediction heads

Sub-boundaries inside it:

- local encoder
- fusion block
- head bundle
- instance conditioning path

### 2. `science_loss.py`

Own:

- `compute_instance_loss`
- `compute_loss`

Why:

- lets the lab reason about loss changes separately from architecture changes
- lets fingerprints become more specific than generic `loss_recipe_changed`

### 3. `science_config.py`

Own:

- `ScienceConfig`
- `derive_config`
- budget overrides
- OOM-aware config backoff policy

Why:

- separates “what to run” from “how the backend works”
- makes budget and hardware adaptation a first-class evolvable surface

### 4. `science_eval.py`

Own:

- benchmark eval
- multi-slice smoke eval
- audit gate
- outcome classification

Why:

- this is now the top human bottleneck area
- it needs to be independently inspectable and evolvable

### 5. `science_train.py`

Own:

- training loop
- progress tracing
- eval-reserve handling
- result assembly

Why:

- separates runtime flow from model/loss/eval semantics
- makes it easier to add later candidate-internal iteration or early stopping

## First Refactor Pass

The first pass should be structural, not ambitious.

That means:

- move code without changing behavior intentionally
- preserve current outputs and traces
- keep `run_science_backend(...)` as the stable public entrypoint

Suggested order:

1. extract loss functions into `science_loss.py`
2. extract model + local/fusion/head code into `science_model.py`
3. extract config derivation + OOM backoff into `science_config.py`
4. extract eval gating into `science_eval.py`
5. leave orchestration in `science_backend.py` as a thin composition layer

After that, optionally:

6. rename `science_backend.py` to a thinner runner/orchestrator later

## Fingerprint Upgrades

Once the structure is explicit, backend fingerprints should move from broad text matching to module-aware signals.

The next fingerprint families should map to:

- `local_encoder_changed`
- `fusion_block_changed`
- `head_bundle_changed`
- `instance_conditioning_changed`
- `loss_recipe_changed`
- `eval_gate_changed`
- `runtime_policy_changed`

This is important because the current `initial_harness` dominance is partly a naming problem.
The lab needs to distinguish:

- “I changed the same basin again”
from
- “I changed a specific submodule inside that basin”

## What Not To Do In Pass One

Do not yet:

- redesign the full model
- change training semantics aggressively
- add dynamic code generation
- collapse everything into a plugin system
- add speculative abstractions with no current use

Pass one should be about:

- explicit module seams
- preserved behavior
- clearer evidence

## How This Helps The Lab

After this modularization, the lab should be able to:

- propose backend changes against named modules instead of generic `initial_harness`
- produce more meaningful fingerprints and hindsight
- ask more precise human questions
- eventually evolve backend structure with less ambiguity

This also directly addresses the useful external-review suggestion:

- expose `initial_harness` as a more explicit evolvable backend module

## Acceptance Criteria

We should consider the first modularization pass successful if:

- `run_science_backend(...)` still works with current candidate flow
- recent smoke/eval tests still pass
- traces and result artifacts remain compatible
- backend fingerprints can distinguish at least:
  - local encoder
  - fusion
  - loss
  - eval gate
  - runtime policy
- `initial_harness` no longer behaves like one opaque scientific object

## Recommended Next Implementation Slice

Start with:

- extract `compute_instance_loss(...)` and `compute_loss(...)` into `science_loss.py`

Why first:

- smallest clean seam
- low behavioral risk
- immediately useful for future backend evolution
- easy to test in isolation
