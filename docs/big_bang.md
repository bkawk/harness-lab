# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T08:39:40+00:00`
- last_heartbeat: `2026-04-02T10:43:37+00:00`
- cycles_completed: `11`
- genesis seed: `cand_0001`
- last candidate: `cand_0371`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0371`
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
- active_candidate: `cand_0371`
- backend_status: `finished`
- backend_pid: `2366378`
- backend_started_at: `2026-04-02T10:33:35+00:00`
- backend_last_poll_at: `2026-04-02T10:43:36+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0371`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3195577977504781`
- `cand_0370`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.295831730420671`
- `cand_0369`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3208132422122258`
- `cand_0368`: outcome `dead_end`; diagnosis `complete`; benchmark `0.38643093195620987`
- `cand_0367`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4232336556853806`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.349173, audit averaged 0.307197, and the mean transfer gap was 0.041977.`
- recent benchmark avg: `0.34917347160499307`
- recent audit avg: `0.3071968943274591`
- recent transfer gap avg: `0.04197657727753394`
- `cand_0371`: benchmark `0.3195577977504781`, audit `0.3038780651767483`, gap `0.015679732573729788`
- `cand_0370`: benchmark `0.295831730420671`, audit `0.2699019837943698`, gap `0.02592974662630121`
- `cand_0369`: benchmark `0.3208132422122258`, audit `0.28593972851389304`, gap `0.03487351369833275`
- `cand_0368`: benchmark `0.38643093195620987`, audit `0.3311649105529011`, gap `0.055266021403308774`
- `cand_0367`: benchmark `0.4232336556853806`, audit `0.3450997835993834`, gap `0.0781338720859972`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `After 370 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (262 candidate(s), avg transfer gap 0.038511).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 831.9 MB on average, leaving most VRAM unused. 7 scored candidate(s) have landed since structural commit `4c8bac2`.`
- scored_candidates_since_change: `7`
- last_structural_commit: `4c8bac2`
### Chosen Lever Values
- source_candidate: `cand_0371`
- train: `eval_batch_size=3, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0371`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=3, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `262`, audit_blocked `152`, avg_gap `0.03851146566140653`
- loss: `science_loss` (targeted); attempts `247`, audit_blocked `138`, avg_gap `0.03849849999592567`
- eval: `science_eval` (available); attempts `254`, audit_blocked `144`, avg_gap `0.03837853999603432`
- config: `science_config` (available); attempts `247`, audit_blocked `138`, avg_gap `0.03849849999592567`
- train: `science_train` (available); attempts `240`, audit_blocked `131`, avg_gap `0.03843477122220623`

### Recent Module Evidence
- `science_backend`: attempts `262`, audit_blocked `152`, avg_gap `0.03851146566140653`
- `science_model`: attempts `262`, audit_blocked `152`, avg_gap `0.03851146566140653`
- `science_eval`: attempts `254`, audit_blocked `144`, avg_gap `0.03837853999603432`
- `science_config`: attempts `247`, audit_blocked `138`, avg_gap `0.03849849999592567`

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
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 370 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `The lab has stayed on `science_train` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
