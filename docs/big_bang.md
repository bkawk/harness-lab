# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-20T13:32:49+00:00`
- cycles_completed: `2282`
- genesis seed: `cand_0001`
- last candidate: `cand_2706`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `378`

## Latest Step
- candidate: `cand_2706`
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
- active_candidate: `cand_2706`
- backend_status: `finished`
- backend_pid: `3166317`
- backend_started_at: `2026-04-20T13:22:43+00:00`
- backend_last_poll_at: `2026-04-20T13:32:46+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2706`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3676201679067038`
- `cand_2705`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36245065241854385`
- `cand_2704`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3775650726117212`
- `cand_2703`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3277599491306634`
- `cand_2702`: outcome `improved`; diagnosis `complete`; benchmark `0.2971985179000136`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_2357` -> gap `-0.00011202849963909411`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.346519, audit averaged 0.304701, and the mean transfer gap was 0.041818.`
- recent benchmark avg: `0.34651887199352915`
- recent audit avg: `0.3047010882164038`
- recent transfer gap avg: `0.04181778377712535`
- `cand_2706`: benchmark `0.3676201679067038`, audit `0.31167285301252956`, gap `0.05594731489417426`
- `cand_2705`: benchmark `0.36245065241854385`, audit `0.3127343274932394`, gap `0.04971632492530448`
- `cand_2704`: benchmark `0.3775650726117212`, audit `0.31145888545369443`, gap `0.06610618715802674`
- `cand_2703`: benchmark `0.3277599491306634`, audit `0.26240198565875394`, gap `0.06535796347190947`
- `cand_2702`: benchmark `0.2971985179000136`, audit `0.3252373894638018`, gap `-0.028038871563788204`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (2597 candidate(s), avg transfer gap 0.031556).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 677.0 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2706`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_2706`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `2597`, audit_blocked `1105`, avg_gap `0.03155561698807058`
- loss: `science_loss` (available); attempts `2582`, audit_blocked `1091`, avg_gap `0.031516345294431466`
- eval: `science_eval` (available); attempts `2589`, audit_blocked `1097`, avg_gap `0.0315221709114109`
- config: `science_config` (available); attempts `2582`, audit_blocked `1091`, avg_gap `0.031516345294431466`
- train: `science_train` (targeted); attempts `2575`, audit_blocked `1084`, avg_gap `0.031491832295241294`

### Recent Module Evidence
- `science_backend`: attempts `2597`, audit_blocked `1105`, avg_gap `0.03155561698807058`
- `science_model`: attempts `2597`, audit_blocked `1105`, avg_gap `0.03155561698807058`
- `science_eval`: attempts `2589`, audit_blocked `1097`, avg_gap `0.0315221709114109`
- `science_config`: attempts `2582`, audit_blocked `1091`, avg_gap `0.031516345294431466`

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
- status: `cooldown`
- trigger_reason: `dead_end_streak`
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
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
