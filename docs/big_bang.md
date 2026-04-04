# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-04T09:02:11+00:00`
- cycles_completed: `198`
- genesis seed: `cand_0001`
- last candidate: `cand_0622`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `24`

## Latest Step
- candidate: `cand_0622`
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
- active_candidate: `cand_0622`
- backend_status: `finished`
- backend_pid: `2705264`
- backend_started_at: `2026-04-04T08:52:09+00:00`
- backend_last_poll_at: `2026-04-04T09:02:11+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0622`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4351059754377258`
- `cand_0621`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34687520034605607`
- `cand_0620`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29898045513091537`
- `cand_0619`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.299283287858241`
- `cand_0618`: outcome `dead_end`; diagnosis `complete`; benchmark `0.46178242199506053`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.368405, audit averaged 0.304187, and the mean transfer gap was 0.064218.`
- recent benchmark avg: `0.36840546815359976`
- recent audit avg: `0.3041874487479263`
- recent transfer gap avg: `0.06421801940567341`
- `cand_0622`: benchmark `0.4351059754377258`, audit `0.34395560602436315`, gap `0.09115036941336263`
- `cand_0621`: benchmark `0.34687520034605607`, audit `0.2706385738498391`, gap `0.07623662649621699`
- `cand_0620`: benchmark `0.29898045513091537`, audit `0.29193168644778883`, gap `0.007048768683126538`
- `cand_0619`: benchmark `0.299283287858241`, audit `0.3043097373179068`, gap `-0.005026449459665794`
- `cand_0618`: benchmark `0.46178242199506053`, audit `0.31010164009973384`, gap `0.1516807818953267`

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
- summary: `Recent backend evolution is concentrated in science_backend (513 candidate(s), avg transfer gap 0.035291).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 864.1 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_0622`
- train: `batch_size=3, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0622`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=2, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `513`, audit_blocked `246`, avg_gap `0.03529149693166138`
- loss: `science_loss` (available); attempts `498`, audit_blocked `232`, avg_gap `0.035189105814232444`
- eval: `science_eval` (available); attempts `505`, audit_blocked `238`, avg_gap `0.035174053841900386`
- config: `science_config` (available); attempts `498`, audit_blocked `232`, avg_gap `0.035189105814232444`
- train: `science_train` (targeted); attempts `491`, audit_blocked `225`, avg_gap `0.035109547768027737`

### Recent Module Evidence
- `science_backend`: attempts `513`, audit_blocked `246`, avg_gap `0.03529149693166138`
- `science_model`: attempts `513`, audit_blocked `246`, avg_gap `0.03529149693166138`
- `science_eval`: attempts `505`, audit_blocked `238`, avg_gap `0.035174053841900386`
- `science_config`: attempts `498`, audit_blocked `232`, avg_gap `0.035189105814232444`

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
- decision_state: `wait`
- decision_reason: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`
- target_file: `src/harness_lab/science_train.py`
- target_functions: `run_training_cycle, write_science_progress, peak_vram_mb`
- proposed_change: `Raise bounded train-side capacity, such as batch_size or eval_batch_size, without altering model, loss, or eval semantics.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_train.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_train.py, tests/test_science_train.py`
- focused_tests: `tests/test_science_train.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `wait`, so autonomous code mutation stays blocked. Recommended action is `wait`, not `targeted_mutation`.`
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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
