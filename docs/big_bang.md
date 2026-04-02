# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T08:39:40+00:00`
- last_heartbeat: `2026-04-02T09:02:06+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0362`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0362`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `normal_cycle`

## Active Backend
- active_candidate: `cand_0362`
- backend_status: `finished`
- backend_pid: `2363729`
- backend_started_at: `2026-04-02T08:52:03+00:00`
- backend_last_poll_at: `2026-04-02T09:02:05+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0362`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.337714704348196`
- `cand_0361`: outcome `dead_end`; diagnosis `complete`; benchmark `0.307674957775385`
- `cand_0360`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0359`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0358`: outcome `dead_end`; diagnosis `complete`; benchmark `0.35542966485598787`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.333606, audit averaged 0.347312, and the mean transfer gap was -0.013706.`
- recent benchmark avg: `0.333606442326523`
- recent audit avg: `0.34731234397971517`
- recent transfer gap avg: `-0.013705901653192151`
- `cand_0362`: benchmark `0.337714704348196`, audit `0.3916055693412892`, gap `-0.0538908649930932`
- `cand_0361`: benchmark `0.307674957775385`, audit `0.3215055063436993`, gap `-0.013830548568314283`
- `cand_0358`: benchmark `0.35542966485598787`, audit `0.32882595625415684`, gap `0.026603708601831033`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (253 candidate(s), avg transfer gap 0.038052).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 607.9 MB on average, leaving most VRAM unused. 3 scored candidate(s) have landed since structural commit `8eb05e7`.`
- scored_candidates_since_change: `3`
- last_structural_commit: `8eb05e7`
### Chosen Lever Values
- source_candidate: `cand_0360`
- loss: `boundary_loss_weight=0.12, instance_margin=0.4`

### Effective Backend Settings
- source_candidate: `cand_0362`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.08, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `253`, audit_blocked `150`, avg_gap `0.03805178147193506`
- loss: `science_loss` (targeted); attempts `238`, audit_blocked `136`, avg_gap `0.03800761452244502`
- eval: `science_eval` (available); attempts `245`, audit_blocked `142`, avg_gap `0.037896291896821546`
- config: `science_config` (available); attempts `238`, audit_blocked `136`, avg_gap `0.03800761452244502`
- train: `science_train` (available); attempts `231`, audit_blocked `129`, avg_gap `0.03792413324981997`

### Recent Module Evidence
- `science_backend`: attempts `253`, audit_blocked `150`, avg_gap `0.03805178147193506`
- `science_model`: attempts `253`, audit_blocked `150`, avg_gap `0.03805178147193506`
- `science_eval`: attempts `245`, audit_blocked `142`, avg_gap `0.037896291896821546`
- `science_config`: attempts `238`, audit_blocked `136`, avg_gap `0.03800761452244502`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_loss.py`
- target_purpose: `Combines classification, parameter, boundary, and instance-separation losses into the training objective.`
- key_functions: `compute_instance_loss, compute_loss`
- levered_surfaces: `param_loss_weight, boundary_loss_weight, instance_loss_weight, instance_margin`
- fixed_surfaces: `Cross-entropy plus smooth-L1 plus BCE loss recipe; Instance similarity and same-class negative construction; Loss-term composition order`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- target_file: `src/harness_lab/science_loss.py`
- target_functions: `compute_instance_loss, compute_loss`
- proposed_change: `Increase transfer-sensitive boundary or instance pressure modestly, for example by strengthening boundary_loss_weight or instance_margin, without changing eval thresholds.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 360 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
