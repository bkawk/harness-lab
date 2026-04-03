# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T13:48:01+00:00`
- cycles_completed: `94`
- genesis seed: `cand_0001`
- last candidate: `cand_0518`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `13`

## Latest Step
- candidate: `cand_0518`
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
- active_candidate: `cand_0518`
- backend_status: `finished`
- backend_pid: `2655180`
- backend_started_at: `2026-04-03T13:37:59+00:00`
- backend_last_poll_at: `2026-04-03T13:48:00+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0518`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34899316296241`
- `cand_0517`: outcome `dead_end`; diagnosis `complete`; benchmark `0.31749318679441496`
- `cand_0516`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.290025840469457`
- `cand_0515`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3858972793087505`
- `cand_0514`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39102550481999565`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.346687, audit averaged 0.306410, and the mean transfer gap was 0.040277.`
- recent benchmark avg: `0.3466869948710056`
- recent audit avg: `0.3064099198089941`
- recent transfer gap avg: `0.04027707506201152`
- `cand_0518`: benchmark `0.34899316296241`, audit `0.29628510949509784`, gap `0.052708053467312166`
- `cand_0517`: benchmark `0.31749318679441496`, audit `0.33155102993264246`, gap `-0.0140578431382275`
- `cand_0516`: benchmark `0.290025840469457`, audit `0.2493468139534316`, gap `0.040679026516025396`
- `cand_0515`: benchmark `0.3858972793087505`, audit `0.31233859378247064`, gap `0.07355868552627987`
- `cand_0514`: benchmark `0.39102550481999565`, audit `0.34252805188132796`, gap `0.048497452938667696`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 7 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

## Budget
- summary: `Mechanisms initial_harness, science_train, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (409 candidate(s), avg transfer gap 0.034847).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 795.2 MB on average, leaving most VRAM unused. 59 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `59`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0518`
- model: `hidden_dim=160, instance_modulation_scale=0.15`

### Effective Backend Settings
- source_candidate: `cand_0518`
- model: `hidden_dim=160, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `409`, audit_blocked `204`, avg_gap `0.03484738608943367`
- loss: `science_loss` (available); attempts `394`, audit_blocked `190`, avg_gap `0.03469865918078552`
- eval: `science_eval` (available); attempts `401`, audit_blocked `196`, avg_gap `0.03468732957244846`
- config: `science_config` (available); attempts `394`, audit_blocked `190`, avg_gap `0.03469865918078552`
- train: `science_train` (targeted); attempts `387`, audit_blocked `183`, avg_gap `0.034586307960240696`

### Recent Module Evidence
- `science_backend`: attempts `409`, audit_blocked `204`, avg_gap `0.03484738608943367`
- `science_model`: attempts `409`, audit_blocked `204`, avg_gap `0.03484738608943367`
- `science_eval`: attempts `401`, audit_blocked `196`, avg_gap `0.03468732957244846`
- `science_config`: attempts `394`, audit_blocked `190`, avg_gap `0.03469865918078552`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_train.py`
- target_purpose: `Owns the wall-clock training loop, progress tracing, benchmark/smoke/audit order, and final evidence assembly.`
- key_functions: `run_training_cycle, write_science_progress, peak_vram_mb`
- levered_surfaces: `batch_size, eval_batch_size, grad_clip, log_interval`
- fixed_surfaces: `Time-based training schedule and eval reserve discipline; Benchmark -> smoke -> audit execution order; Evidence and trace writing for science outcomes`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- decision_state: `switch`
- decision_reason: ``science_train` is already active in the recent scored window but is repeating dead-end outcomes without a keeper signal, so switch seams instead of issuing another brief here.`
- target_file: `src/harness_lab/science_train.py`
- target_functions: `run_training_cycle, write_science_progress, peak_vram_mb`
- proposed_change: `Raise bounded train-side capacity, such as batch_size or eval_batch_size, without altering model, loss, or eval semantics.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `targeted_mutation`
- target_file: `src/harness_lab/science_train.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_train.py, tests/test_science_train.py`
- focused_tests: `tests/test_science_train.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `switch`, so autonomous code mutation stays blocked.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 1 ranked requests for human help.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
