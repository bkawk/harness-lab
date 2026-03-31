# Project Plan

## What `harness-lab` Is Now

`harness-lab` is no longer a blank Meta-Harness-inspired scaffold.
It is now a living research system with:

- first-class candidate workspaces
- source snapshots, diffs, traces, outcomes, and diagnosis
- memory, hindsight, policy, budget, diversity, and human-feedback layers
- a real repo-native science backend
- a long-running `big-bang` supervisor
- the GitHub repo acting as the main dashboard
- bounded Claude participation in the strategic loop

The concrete research target is still the same:
- learn systems that can map triangle meshes toward structured parametric or CAD-like representations

The repo is the harness for getting there, not the finished model.

## Core Program

The governing bet is still the Meta-Harness bet:

- preserve filesystem-native evidence instead of only scores
- let the lab reason from traces, diffs, and lineage
- evolve the harness as well as the model
- keep a durable memory of what changed and why

But the working stance now is sharper:

1. Build a strong enough seed backend for real science.
2. Let the lab evolve search strategy around that backend.
3. Then make the backend itself more directly evolvable.

So the program is not “more meta at all costs.”
It is:

- evidence first
- science second
- autonomy only where the evidence can support it

## Current Live State

Today the lab already has:

- candidate bootstrap snapshots and richer decision bundles
- polled command execution with live backend traces
- external review with separate `lab_advice` and `human_advice`
- `What The Lab Wants` and `What We Did`
- bounded Claude-driven Tier 2 strategy integration
- a realistic wall-clock training budget
- repo-native ABC dataset acquisition and prepared dataset builds
- named evaluation slices for benchmark, smoke, and audit-style evaluation

This means the main question is no longer “how do we scaffold the lab?”
It is:

- how do we make the live loop more scientifically effective and more reliable?

## Immediate Priorities

### 1. Let science run and trust evidence more than instinct

The lab is now far enough along that the next improvements should be driven by:

- candidate outcomes
- human-feedback ranking
- trend changes after interventions
- whether recent fixes actually lower recurring requests

That means we should increasingly:

- implement the top human request
- let the lab run
- re-check whether the request fades or persists

### 2. Stabilize `big-bang`

The live loop still has intermittent stale-heartbeat / mid-cycle hang behavior.

So a standing near-term priority is:

- make the supervisor and publish path more robust
- ensure stale or hung subprocesses cannot silently stall the repo dashboard
- improve restart confidence

### 3. Improve unresolved human bottlenecks

The lab’s current human-facing requests are the best guide to what still sits outside the self-evolving loop.

Typical examples:

- evaluation / transfer stability pressure
- backend startup and progress detection
- dataset slice quality
- later: explicit VRAM pressure if the evidence supports it

## LLM Integration Roadmap

### Tier 2: Bounded LLM search strategy

Tier 2 is live and is the current operating mode.

Claude can now participate, with heuristic fallback, in:

- external review
- proposal authoring
- parent selection
- diagnosis reconciliation
- execution planning
- hindsight synthesis
- policy synthesis

What remains programmatic:

- candidate workspace creation
- file I/O and JSON structure
- evidence capture
- subprocess management
- the actual science backend execution
- budgeting arithmetic
- supervisor timing and publishing
- dataset management

Why Tier 2 is the right present stage:

- it improves brittle search logic
- it preserves safe fallbacks
- it does not yet hand raw code mutation to the LLM

### Tier 3: LLM writes science code

Tier 3 is not live yet.

This is the stage where the lab starts mutating backend science directly:

- model structure
- config derivation
- loss behavior
- semantic backend change summaries
- outcome interpretation around scientific context

Before Tier 3, we still want:

- stronger validation and sandboxing for generated code
- clearer modular backend boundaries
- better hardware / memory evidence

Important Tier 3 addition:

- explicit VRAM and memory-pressure observability
- peak VRAM
- OOMs
- memory-capped config downgrades

That evidence should feed:

- candidate traces
- human feedback
- future backend decisions

### Tier 4: Iteration within a candidate

Tier 4 is also not live yet.

This is the stage where a candidate stops being a single-shot run and becomes a bounded mini-loop:

- read mid-run traces
- diagnose failure
- attempt repair
- re-run inside the same candidate budget

This is powerful, but it raises:

- cycle-time cost
- complexity
- data-model complexity for multi-run candidates
- the risk of unstable self-evaluation

So Tier 4 should follow only after Tier 3 has solid safety rails.

## Backend Science Roadmap

The backend science should not stay fixed.

But it also should not be handed over to open-ended evolution too early.

The right order is:

1. strengthen the seed backend deliberately
2. make the backend modular enough to evolve
3. let the lab evolve it scientifically

### Backend goals

- reach rough scientific parity with the strongest old `mesh-para` ideas
- keep the backend cleaner and more observable than the old stack
- expose real scientific substructures the lab can later mutate

### Backend roadmap

1. Local geometry
- maintain and improve neighborhood-aware local encoding

2. Local/global fusion
- strengthen how local and global geometry interact

3. Class-conditioned instance behavior
- continue refining structure-aware instance modulation

4. Better metrics and outcome quality
- transfer, boundary, class-slice, and drift-aware signals

5. Modular backend structure
- expose clearer units:
  - local encoder
  - fusion block
  - loss recipe
  - outcome classifier

6. Backend-aware evidence
- richer fingerprints
- later semantic diff summaries
- hardware / memory pressure evidence

7. Backend-specific hindsight and promotion
- let the lab reason about scientific mechanisms, not just generic parents

## What We Are Explicitly Not Doing

We are still not:

- copying `mesh-para` wholesale
- restoring the old monitor-app model as the main dashboard
- giving the LLM unconstrained code control yet
- treating every human intervention as fully resolved the moment it lands

We want:

- selective inheritance from `mesh-para`
- bounded Claude participation
- a repo-centered lab
- unresolved problems to stay visible until evidence says they are truly improving

## Success Criteria

Near-term success:

- `big-bang` runs reliably
- the repo remains a truthful dashboard
- the lab’s top requests change in response to real interventions
- the science summary shows real keepers and better transfer behavior

Medium-term success:

- Tier 2 produces better strategic choices than heuristics alone
- backend changes become more targeted and interpretable
- the human-feedback queue becomes narrower and more specific over time

Long-term success:

- the backend itself becomes an evolvable scientific object
- the lab improves faster than the older `mesh-para` loop did
- the repo becomes a durable record of an actually learning research system
