# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T11:55:24+00:00`
- cycles_completed: `84`
- genesis seed: `cand_0001`
- last candidate: `cand_0508`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `11`

## Latest Step
- candidate: `cand_0508`
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
- active_candidate: `cand_0508`
- backend_status: `finished`
- backend_pid: `2652511`
- backend_started_at: `2026-04-03T11:45:21+00:00`
- backend_last_poll_at: `2026-04-03T11:55:24+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0508`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39413133893371766`
- `cand_0507`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31295082447370204`
- `cand_0506`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4158922620068207`
- `cand_0505`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4179873445287302`
- `cand_0504`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3350810187507207`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.375209, audit averaged 0.320172, and the mean transfer gap was 0.055037.`
- recent benchmark avg: `0.37520855773873824`
- recent audit avg: `0.32017159768328657`
- recent transfer gap avg: `0.05503696005545168`
- `cand_0508`: benchmark `0.39413133893371766`, audit `0.32161995642080704`, gap `0.07251138251291062`
- `cand_0507`: benchmark `0.31295082447370204`, audit `0.31047888303229054`, gap `0.002471941441411496`
- `cand_0506`: benchmark `0.4158922620068207`, audit `0.31092843358861516`, gap `0.10496382841820556`
- `cand_0505`: benchmark `0.4179873445287302`, audit `0.3078415074109127`, gap `0.1101458371178175`
- `cand_0504`: benchmark `0.3350810187507207`, audit `0.3499892079638075`, gap `-0.014908189213086787`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_loss, science_train exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (399 candidate(s), avg transfer gap 0.034882).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 781.6 MB on average, leaving most VRAM unused. 49 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `49`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0508`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0508`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `399`, audit_blocked `202`, avg_gap `0.03488238431734966`
- loss: `science_loss` (available); attempts `384`, audit_blocked `188`, avg_gap `0.03473084019430699`
- eval: `science_eval` (available); attempts `391`, audit_blocked `194`, avg_gap `0.03471865952440188`
- config: `science_config` (available); attempts `384`, audit_blocked `188`, avg_gap `0.03473084019430699`
- train: `science_train` (targeted); attempts `377`, audit_blocked `181`, avg_gap `0.0346159003711374`

### Recent Module Evidence
- `science_backend`: attempts `399`, audit_blocked `202`, avg_gap `0.03488238431734966`
- `science_model`: attempts `399`, audit_blocked `202`, avg_gap `0.03488238431734966`
- `science_eval`: attempts `391`, audit_blocked `194`, avg_gap `0.03471865952440188`
- `science_config`: attempts `384`, audit_blocked `188`, avg_gap `0.03473084019430699`

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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
