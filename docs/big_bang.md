# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-21T13:59:11+00:00`
- cycles_completed: `2412`
- genesis seed: `cand_0001`
- last candidate: `cand_2836`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `393`

## Latest Step
- candidate: `cand_2836`
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
- active_candidate: `cand_2836`
- backend_status: `finished`
- backend_pid: `3191489`
- backend_started_at: `2026-04-21T13:49:06+00:00`
- backend_last_poll_at: `2026-04-21T13:59:08+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2836`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3641922676738633`
- `cand_2835`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3737142156343696`
- `cand_2834`: outcome `dead_end`; diagnosis `complete`; benchmark `0.341110894161622`
- `cand_2833`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29666267021875736`
- `cand_2832`: outcome `dead_end`; diagnosis `complete`; benchmark `0.35845983857588515`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_2357` -> gap `-0.00011202849963909411`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.346828, audit averaged 0.306587, and the mean transfer gap was 0.040241.`
- recent benchmark avg: `0.3468279772528995`
- recent audit avg: `0.30658710634858133`
- recent transfer gap avg: `0.04024087090431814`
- `cand_2836`: benchmark `0.3641922676738633`, audit `0.34387974418929806`, gap `0.020312523484565248`
- `cand_2835`: benchmark `0.3737142156343696`, audit `0.31895959041046235`, gap `0.05475462522390723`
- `cand_2834`: benchmark `0.341110894161622`, audit `0.2570027393648709`, gap `0.0841081547967511`
- `cand_2833`: benchmark `0.29666267021875736`, audit `0.2993142537711311`, gap `-0.0026515835523737152`
- `cand_2832`: benchmark `0.35845983857588515`, audit `0.3137792040071443`, gap `0.04468063456874083`

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
- summary: `Mechanisms science_loss, science_train, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (2727 candidate(s), avg transfer gap 0.031376).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 889.6 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2836`
- train: `batch_size=4, grad_clip=1.2`

### Effective Backend Settings
- source_candidate: `cand_2836`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=2, grad_clip=1.2, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `2727`, audit_blocked `1158`, avg_gap `0.03137588276852273`
- loss: `science_loss` (available); attempts `2712`, audit_blocked `1144`, avg_gap `0.031337576414592574`
- eval: `science_eval` (available); attempts `2719`, audit_blocked `1150`, avg_gap `0.03134351932438143`
- config: `science_config` (available); attempts `2712`, audit_blocked `1144`, avg_gap `0.031337576414592574`
- train: `science_train` (targeted); attempts `2705`, audit_blocked `1137`, avg_gap `0.03131378689492983`

### Recent Module Evidence
- `science_backend`: attempts `2727`, audit_blocked `1158`, avg_gap `0.03137588276852273`
- `science_model`: attempts `2727`, audit_blocked `1158`, avg_gap `0.03137588276852273`
- `science_eval`: attempts `2719`, audit_blocked `1150`, avg_gap `0.03134351932438143`
- `science_config`: attempts `2712`, audit_blocked `1144`, avg_gap `0.031337576414592574`

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
