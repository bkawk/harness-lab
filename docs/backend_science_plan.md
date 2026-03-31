# Backend Science Plan

## Why This Exists

`harness-lab` now has a strong control plane:
- candidate workspaces
- memory
- hindsight
- policy
- budgeting
- diversity pressure
- a real repo-native science backend

But the current science backend is still simpler than the stronger evolved `mesh-para` training core.

So the next goal is not "more meta."
It is to make the science backend good enough that the lab's self-evolution pressure has something strong to work on.

## Comparison To `mesh-para`

What `mesh-para` already had in its stronger phase:
- explicit local geometry aggregation with k-NN neighborhoods
- richer local/global feature fusion
- class-conditioned instance modulation
- a training loop already shaped by many benchmark iterations

What `harness-lab` currently has:
- a compact repo-native point model
- global pooling only
- simpler instance embedding
- cleaner dataset and audit handling
- much stronger research memory and control logic

Expected result:
- short term: `harness-lab` may underperform `mesh-para` on raw score
- medium term: `harness-lab` should improve faster and more sanely
- long term: the best path is to combine `harness-lab`'s control plane with a backend science core that absorbs the strongest lessons from `mesh-para`

## Main Principle

Do not copy `mesh-para` wholesale.

Instead:
1. identify the strongest scientific ingredients
2. port them deliberately into the repo-native backend
3. keep the new backend clean, observable, and easy for the lab to evolve

The backend science should not be frozen.

The right target is:
- strong enough to be a good seed
- modular enough to evolve afterward

So the plan is not:
- hand-design the final science backend and lock it forever

The plan is:
- strengthen the initial backend deliberately
- expose the scientific substructures clearly
- let the lab evolve those substructures once the seed is good enough

## Phase 1: Reach Feature Parity With The Best Old Ideas

### 1. Local Geometry Encoder
Add an explicit neighborhood-aware local encoder to the science backend.

Target:
- port the core idea of k-NN local aggregation from `mesh-para`
- keep it compact enough to fit the current wall-clock budget

Why:
- this is the single biggest architectural gap versus the old training loop

Success signal:
- benchmark and audit both rise without the transfer gap getting worse

### 2. Richer Local + Global Fusion
Move beyond pure global pooling.

Target:
- combine:
  - pointwise features
  - local neighborhood features
  - global pooled context

Why:
- the current backend is probably leaving geometric signal on the table

Success signal:
- better macro IoU and better parameter score at the same wall-clock budget

### 3. Class-Conditioned Instance Path
Strengthen the instance head with class-conditioned modulation.

Target:
- borrow the idea, not the exact implementation, from the stronger `mesh-para` loop

Why:
- the current instance path is too plain relative to the problem structure

Success signal:
- more stable boundary/instance behavior
- fewer local-only gains

## Phase 2: Improve Scientific Signal Quality

### 4. Better Outcome Classification
Current outcome labels are useful but still coarse.

Add:
- overfit-like pattern
- transfer win
- transfer collapse
- unstable training
- undertrained

Why:
- the meta loop can only get smarter if the science backend reports richer failure structure

### 5. Stronger Metrics In `science_metrics.json`
Keep:
- benchmark score
- audit score

Add:
- boundary F1 or precision/recall style indicators
- class-wise IoU slices
- instance quality proxy
- train-vs-val drift indicators

Why:
- future hindsight should reason about mechanism-level behavior, not just one scalar

### 6. Better Benchmark / Audit Separation
Preserve the current split discipline and strengthen it.

Add:
- explicit small benchmark subset metadata
- explicit audit subset metadata
- maybe a secondary tougher audit slice later

Why:
- `mesh-para` taught us that local wins are not enough

## Phase 3: Make The Backend Easier To Evolve

### 7. Modular Science Components
Refactor the backend so the lab can evolve distinct units rather than one big file.

Candidate modules:
- feature encoder
- local geometry block
- fusion block
- loss recipe
- outcome classifier

Why:
- the lab will make better edits if the backend structure matches the real scientific degrees of freedom
- this is the step that turns backend science from "fixed implementation" into "evolvable scientific substrate"

### 8. Backend Diff Fingerprints
Write a structured summary of what a candidate changed in the science backend.

Examples:
- `local_encoder_changed`
- `loss_recipe_changed`
- `instance_path_changed`
- `fusion_changed`

Why:
- hindsight and policy can then reason over meaningful scientific change types

### 9. Time-Budget-Aware Model Variants
Support multiple backend shapes under the same science budget.

Examples:
- compact local model
- richer local model
- transfer-stability-focused model

Why:
- the lab should learn which model family uses the 10-minute budget best

## Phase 4: Close The Loop With Real Scientific Judgment

### 10. Promote Backend Mechanisms, Not Just Generic Parents
Once the backend has real scientific submodules, the lab should rank:
- local geometry changes
- fusion changes
- loss changes
- transfer-stability changes

Why:
- this is where the Meta-Harness control plane starts becoming a real science engine

### 11. Add Backend-Specific Hindsight
Ask questions like:
- should the lab have prioritized local geometry earlier?
- which loss changes helped benchmark but hurt audit?
- which backend mechanisms are saturated?

Why:
- general hindsight is good
- backend-specific hindsight is where real scientific leverage begins

## Recommended Build Order

1. Add local geometry encoder
2. Add richer local/global fusion
3. Add class-conditioned instance path
4. Expand science metrics and failure labels
5. Split the backend into clearer modules
6. Add backend diff fingerprints
7. Add backend-specific hindsight and promotion logic

## What Good Looks Like

We should expect the path to look like this:

1. first, `harness-lab` becomes roughly competitive with the stronger old `mesh-para` backend
2. then, the backend itself becomes a real object of evolution rather than a static seed
3. then, its better memory and control plane starts making it improve faster than `mesh-para` did
4. only after that should we expect clearly better long-run results, not immediately

So the immediate target is not "instant breakthrough."
It is:
- scientific parity first
- then backend evolvability
- then scientific acceleration
