# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T18:46:24+00:00`
- cycles_completed: `40`
- genesis seed: `cand_0001`
- last candidate: `cand_0415`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0415`
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
- active_candidate: `cand_0415`
- backend_status: `finished`
- backend_pid: `2382552`
- backend_started_at: `2026-04-02T18:36:21+00:00`
- backend_last_poll_at: `2026-04-02T18:46:23+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0415`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32371262780650617`
- `cand_0414`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3800623005671471`
- `cand_0413`: outcome `keeper`; diagnosis `complete`; benchmark `0.30254038153970464`
- `cand_0412`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3180151642097889`
- `cand_0411`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2833612396168427`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.321538, audit averaged 0.316460, and the mean transfer gap was 0.005078.`
- recent benchmark avg: `0.3215383427479979`
- recent audit avg: `0.3164600446589441`
- recent transfer gap avg: `0.005078298089053778`
- `cand_0415`: benchmark `0.32371262780650617`, audit `0.31048100248486277`, gap `0.013231625321643403`
- `cand_0414`: benchmark `0.3800623005671471`, audit `0.32273896793729334`, gap `0.057323332629853785`
- `cand_0413`: benchmark `0.30254038153970464`, audit `0.3248414639537579`, gap `-0.022301082414053264`
- `cand_0412`: benchmark `0.3180151642097889`, audit `0.3346500970331049`, gap `-0.016634932823315962`
- `cand_0411`: benchmark `0.2833612396168427`, audit `0.28958869188570174`, gap `-0.006227452268859068`

## Hindsight
- summary: `In the recent scored window, the lab saw 4 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- summary: `Recent backend evolution is concentrated in science_backend (306 candidate(s), avg transfer gap 0.037110).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 727.9 MB on average, leaving most VRAM unused. 30 scored candidate(s) have landed since structural commit `4d32d84`.`
- scored_candidates_since_change: `30`
- last_structural_commit: `4d32d84`
### Chosen Lever Values
- source_candidate: `cand_0415`
- loss: `instance_loss_weight=0.08, instance_margin=0.4`

### Effective Backend Settings
- source_candidate: `cand_0415`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.4`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `306`, audit_blocked `168`, avg_gap `0.03710955314689722`
- loss: `science_loss` (targeted); attempts `291`, audit_blocked `154`, avg_gap `0.03702380407841081`
- eval: `science_eval` (available); attempts `298`, audit_blocked `160`, avg_gap `0.03695610697217774`
- config: `science_config` (available); attempts `291`, audit_blocked `154`, avg_gap `0.03702380407841081`
- train: `science_train` (available); attempts `284`, audit_blocked `147`, avg_gap `0.0369303398766417`

### Recent Module Evidence
- `science_backend`: attempts `306`, audit_blocked `168`, avg_gap `0.03710955314689722`
- `science_model`: attempts `306`, audit_blocked `168`, avg_gap `0.03710955314689722`
- `science_eval`: attempts `298`, audit_blocked `160`, avg_gap `0.03695610697217774`
- `science_config`: attempts `291`, audit_blocked `154`, avg_gap `0.03702380407841081`

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

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `targeted_mutation`
- target_file: `src/harness_lab/science_loss.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_loss.py, tests/test_science_loss.py`
- focused_tests: `tests/test_science_loss.py`
- verification_status: `No verification run recorded yet.`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
