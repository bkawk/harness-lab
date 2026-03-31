# LLM Integration Tiers for harness-lab

## Overview

This document describes 5 progressive tiers of LLM integration, from the current
heuristic-only state to full meta-harness-level autonomy. Each tier builds on the
previous one.

```
Tier 1          Tier 2              Tier 3              Tier 4              Meta-harness
  |               |                   |                   |                   |
3 calls         8-12 calls          12-18 calls         18-30 calls         20-50 calls
Commentator     Search strategist   Code author         Iterative debugger  Full agent
```

All tiers use `claude -p` on the Max plan — no API costs.

---

## Tier 1: LLM Advises (already planned)

**~3 LLM calls per cycle, ~$0.10-0.30**

The LLM annotates decisions already made by heuristics:

- Writes better proposal rationales (replaces template concatenation)
- Enriches diagnosis with causal analysis (replaces canned counterfactuals)
- Generates nuanced policy adjustments (replaces hard-coded threshold rules)

Heuristics remain the primary driver. LLM adds prose quality without
changing decisions.

### Files changed

- `src/harness_lab/proposal.py` — rationale generation
- `src/harness_lab/diagnosis.py` — counterfactual and summary enrichment
- `src/harness_lab/hindsight.py` — policy adjustment prose
- New: `src/harness_lab/llm.py` — shared `claude -p` wrapper with fallback

---

## Tier 2: LLM Drives Search Strategy

**~8-12 LLM calls per cycle, ~$0.50-2.00**

The LLM becomes the decision-maker for search strategy. Heuristics become
fallback validators.

### What the LLM does

1. **Authors proposals holistically** — reads the full bootstrap snapshot (parent
   diagnosis, hindsight, budget, diversity, hardware, external review) and writes
   the proposal's `changes`, `target`, and `rationale` as a coherent document.
   Replaces the independent `_*_change_items` functions that currently generate
   contradictory change items. (~1-2 calls)

2. **Selects parents with reasoning** — receives the ranked candidate index with
   diagnosis summaries and returns a justified parent choice plus branching
   strategy. Replaces point-based scoring in `score_parent_candidate`. (~1 call)

3. **Generates diagnoses** — reads outcome, benchmark/audit summaries, training
   traces, and the proposal's stated expectations. Produces causal summary,
   severity, mechanism, failure modes, counterfactuals, and testable hypotheses.
   Replaces rule-based `reconcile_diagnosis_from_outcome`. (~1-2 calls)

4. **Writes hindsight narrative** — reads full mechanism stats and backend
   fingerprint stats, produces nuanced policy adjustments instead of threshold-
   based rules like "3 attempts with 0 positive = over-explored". (~1 call)

5. **Synthesizes policy** — reads hindsight, diversity, hardware, backend, and
   external review, then produces the full policy dict including `selection_mode`,
   `cooldown_multiplier`, and all tuning knobs. Replaces if-else chains. (~1 call)

6. **Enriches execution plans** — reads the proposal and diagnosis, writes
   benchmark/audit steps tailored to the specific hypothesis. (~1 call)

7. **Judges diversity** — reviews recent mechanism sequence and reasons about
   whether the current line is converging productively or genuinely stuck. Replaces
   `streak >= 3` threshold. (~1 call)

8. **Authors external reviews** — when triggered, produces `lab_advice` and
   `human_advice` with strategic reasoning. (~1 call, conditional)

### What stays programmatic

- Candidate workspace creation, file I/O, JSON read/write
- Evidence capture (repo snapshots, diffs, fingerprinting)
- Runner execution (subprocess management, polling, stale detection)
- The actual science backend (PyTorch training loop)
- Budget arithmetic (allowed/consumed/remaining)
- The big_bang supervisor loop (timing, publishing, heartbeats)
- Dataset management

### What this unlocks

- **Cross-cutting reasoning**: The LLM can see that a budget constraint, a
  diversity signal, and a hindsight finding all point to the same conclusion,
  and craft a single coherent proposal strategy.
- **Richer diagnoses**: Counterfactuals become genuine hypotheses rather than
  template strings like "Revise {mechanism} with a smaller follow-up."
- **Adaptive policy**: The policy can express judgments the if-else chains cannot,
  e.g., "this mechanism has been tried 2 times with mediocre results, but both
  times the learning rate was too high; try once more with a lower LR."
- **Context-aware parent selection**: The LLM reasons about lineage quality and
  which failure mode is most tractable, rather than summing fixed-weight points.

### Risks

- **Latency**: ~60-90s overhead on a 600s training cycle (~10-15%)
- **Consistency**: LLM outputs must conform to existing JSON schemas; need
  validation layers
- **Regression risk**: Heuristics are deterministic and testable; LLM needs
  fallback paths

### Files changed

Everything from Tier 1, plus:
- `src/harness_lab/proposal.py` — LLM replaces `_proposal_change_items`,
  `_novelty_basis_from_memory`, `_choose_parent_for_branching`
- `src/harness_lab/synthesis.py` — LLM replaces `score_parent_candidate`
- `src/harness_lab/diagnosis.py` — LLM replaces `reconcile_diagnosis_from_outcome`
- `src/harness_lab/hindsight.py` — LLM replaces `build_hindsight`
- `src/harness_lab/policy.py` — LLM replaces `build_policy`
- `src/harness_lab/execution.py` — LLM replaces `plan_execution_for_candidate`
- `src/harness_lab/diversity.py` — LLM replaces `build_diversity`
- `src/harness_lab/external_review.py` — LLM replaces `_heuristic_review_payload`

---

## Tier 3: LLM Writes Science Code

**~12-18 LLM calls per cycle, ~$2-5**

The LLM gains control over the science code itself, not just the search strategy.

### What the LLM adds (on top of Tier 2)

1. **Mutates the model** — reads `science_backend.py`, the proposal's changes,
   and parent metrics. Writes diffs to `CompactPointModel.__init__`,
   `CompactPointModel.forward`, `compute_loss`, or `derive_config`. Can try
   architectural changes (attention, skip connections, different aggregation)
   that the fixed config menu cannot express. (~2-4 calls: plan, write, review)

2. **Derives configs with reasoning** — replaces hash-based config selection with
   informed choices: "parent had transfer collapse with LR 3e-4, so try 1.5e-4
   with stronger weight decay." (~1 call)

3. **Fingerprints diffs semantically** — replaces keyword-matched fingerprints
   like "local_encoder_changed" with "added skip connections to local encoder
   to preserve gradient flow." (~1 call)

4. **Refines outcome classification** — can override rigid threshold rules when
   context warrants it: "this looks like audit_blocked by the rules, but the
   transfer gap is shrinking and boundary F1 is strong — label it improving."
   (~1 call)

### What stays programmatic

- PyTorch training loop structure (the loop stays fixed; the LLM mutates the
  model/loss/config inside it)
- Runner subprocess management, polling, stale detection
- Workspace management, evidence capture mechanics
- Dataset preparation and loading
- Budget arithmetic, big_bang supervisor

### What this unlocks

- **Genuine architecture search**: Try attention mechanisms, different activation
  functions, novel loss recipes — changes that require understanding PyTorch
- **Science-aware hyperparameter tuning**: Reason about the loss landscape based
  on prior training curves, not just pick from fixed choices
- **Semantic lineage tracking**: "Increased boundary loss weight to address weak
  boundary F1" instead of binary "loss_recipe_changed"

### Risks

- **Code safety**: LLM-generated PyTorch code could crash, hang, or NaN. The
  stale-process timeout (600s) is a safety net, but need additional guards —
  syntax validation, import restriction, output shape checking
- **Mutation quality**: Most mutations will be bad. The evolutionary loop handles
  dead ends, but the dead-end ratio may increase initially
- **Determinism loss**: `derive_config` is currently deterministic; LLM-authored
  configs are stochastic

### Files changed

Everything from Tier 2, plus:
- `src/harness_lab/science_backend.py` — `derive_config` becomes LLM-driven;
  mutation layer around `CompactPointModel` and `compute_loss`
- `src/harness_lab/evidence.py` — `_science_backend_fingerprints` replaced by
  LLM semantic analysis
- `src/harness_lab/runner.py` — pre-execution validation for mutated code
- New: `src/harness_lab/mutation.py` — code mutation planning, generation,
  validation, application
- New: `src/harness_lab/sandbox.py` — safety checks for LLM-generated code

---

## Tier 4: LLM Iterates Within a Candidate

**~18-30 LLM calls per cycle, ~$3-8**

The candidate lifecycle becomes a mini-loop. The LLM can react to results and
retry within a single candidate, bounded to 2-3 refinement rounds.

### What the LLM adds (on top of Tier 3)

1. **Reads training traces mid-run** — reviews stdout/stderr logs and
   `science_metrics.json` to extract structured insights: "loss plateaued at
   step 400 before boundary loss started dominating", "gradient norms spiked
   in epoch 3 suggesting the local encoder is unstable." (~1-2 calls)

2. **Proposes repair mutations** — after a failed or underperforming run, the
   LLM diagnoses the issue from traces and proposes a targeted fix. A second
   training run executes with the repair. (~3-5 calls per refinement round)

3. **Compares across lineages** — reads source snapshots of multiple previous
   candidates (not just the parent), compares diffs, identifies which code
   changes correlated with improvement vs regression. (~2-3 calls)

4. **Adapts execution strategy** — adjusts time budget based on early metrics,
   skips audit if benchmark is clearly dead, requests warm-start re-runs.
   (~1-2 calls)

5. **Writes dashboard narrative** — replaces template markdown with a genuine
   situation report: what the lab has learned, what it is stuck on, what it
   plans to try, what human intervention would help most. (~1 call)

6. **Self-evaluates** — reviews its own previous proposals and diagnoses against
   actual outcomes, adjusts its reasoning strategy. Meta-hindsight applied to
   the LLM's own quality. (~1 call)

### What stays programmatic

- PyTorch training loop execution
- Subprocess management (though LLM influences what runs)
- File I/O, workspace management
- Dataset preparation
- Git operations, publishing
- big_bang cycle timing and heartbeats

### What this unlocks

- **Closed-loop learning within a single candidate**: Detect a failing run,
  diagnose from traces, fix, re-run — without waiting for a full cycle
- **Cross-lineage reasoning**: "Candidates 5 and 8 both tried attention in
  the local encoder and both had transfer collapse — this architecture doesn't
  generalize"
- **Intelligent resource allocation**: Skip expensive audit for obviously-dead
  candidates, extend budgets for promising runs
- **Human-readable progress**: Dashboard becomes genuinely informative

### Risks

- **Cycle time**: Refinement loops could 2-3x cycle time, reducing throughput
  (candidates/hour) even as hit rate improves
- **Runaway costs**: Need hard cap on refinement iterations (max 2-3 rounds)
- **Complexity**: Candidate lifecycle is no longer linear; workspace data model
  must support multiple runs per candidate
- **Feedback instability**: LLM evaluating its own outputs can oscillate; needs
  grounding against numeric outcomes

### Files changed

Everything from Tier 3, plus:
- `src/harness_lab/loop.py` — `advance_candidate_loop` gets refinement sub-loop
- `src/harness_lab/runner.py` — multi-run support, warm-start, conditional audit
- `src/harness_lab/big_bang.py` — LLM-authored dashboard, refinement budgets
- `src/harness_lab/evidence.py` — cross-lineage comparison, multi-run traces
- `src/harness_lab/outcome.py` — multi-run outcomes (best-of-N, post-refinement)
- `src/harness_lab/workspace.py` — data model for multi-run candidates
- New: `src/harness_lab/trace_reader.py` — structured extraction from training logs
- New: `src/harness_lab/refinement.py` — refinement loop logic, convergence
  detection, repair mutation orchestration

---

## Summary Table

| Aspect | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Meta-harness |
|---|---|---|---|---|---|
| LLM calls/cycle | 3 | 8-12 | 12-18 | 18-30 | 20-50 |
| LLM role | Commentator | Search strategist | Code author | Iterative debugger | Full agent |
| Heuristics role | Primary | Fallback | Fallback | Fallback | Absent |
| Code mutations | No | No | Yes | Yes + repair | Full control |
| Inner loop | No | No | No | Yes (2-3 rounds) | Yes (unbounded) |
| Cost/cycle | ~$0.10-0.30 | ~$0.50-2.00 | ~$2-5 | ~$3-8 | ~$5-15 |

| | Decides *what* to try | Writes *code* | Reacts to *results* | Inner loop |
|---|---|---|---|---|
| Tier 1 | No | No | No | No |
| Tier 2 | Yes | No | No | No |
| Tier 3 | Yes | Yes | No | No |
| Tier 4 | Yes | Yes | Yes | Yes |

## Recommendation

Start with Tier 2. It is the biggest improvement per unit of risk — the search
strategy is where the heuristics are most brittle (hardcoded thresholds, template
strings, contradictory change items). It does not touch science code execution,
so risk is low. If proposals get worse, the existing heuristics are right there
as fallback.

Tier 3 is the exciting one but needs safety infrastructure (code validation,
sandboxing) before it is safe. Tier 2 gives time to build that while already
getting better proposals.
