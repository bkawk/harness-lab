# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-11T07:23:30+00:00`
- cycles_completed: `1093`
- genesis seed: `cand_0001`
- last candidate: `cand_1517`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `173`

## Latest Step
- candidate: `cand_1517`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Active Backend
- active_candidate: `cand_1517`
- backend_status: `finished`
- backend_pid: `2900315`
- backend_started_at: `2026-04-11T07:13:26+00:00`
- backend_last_poll_at: `2026-04-11T07:23:28+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1517`: outcome `dead_end`; diagnosis `complete`; benchmark `0.40306450911696495`
- `cand_1516`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32315537428000285`
- `cand_1515`: outcome `improved`; diagnosis `complete`; benchmark `0.2889297143205909`
- `cand_1514`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3783542472816218`
- `cand_1513`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3644374459152428`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.351588, audit averaged 0.315987, and the mean transfer gap was 0.035601.`
- recent benchmark avg: `0.3515882581828847`
- recent audit avg: `0.3159872808264622`
- recent transfer gap avg: `0.03560097735642244`
- `cand_1517`: benchmark `0.40306450911696495`, audit `0.37124153758682377`, gap `0.031822971530141186`
- `cand_1516`: benchmark `0.32315537428000285`, audit `0.25921623777359093`, gap `0.06393913650641192`
- `cand_1515`: benchmark `0.2889297143205909`, audit `0.310050125496687`, gap `-0.021120411176096088`
- `cand_1514`: benchmark `0.3783542472816218`, audit `0.3126450296614148`, gap `0.06570921762020704`
- `cand_1513`: benchmark `0.3644374459152428`, audit `0.3267834736137947`, gap `0.037653972301448124`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (1408 candidate(s), avg transfer gap 0.032216).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 942.8 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1517`
- train: `batch_size=4, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_1517`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.08, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1408`, audit_blocked `593`, avg_gap `0.03221607437259832`
- loss: `science_loss` (available); attempts `1393`, audit_blocked `579`, avg_gap `0.032149328254635276`
- eval: `science_eval` (available); attempts `1400`, audit_blocked `585`, avg_gap `0.03215743930684286`
- config: `science_config` (available); attempts `1393`, audit_blocked `579`, avg_gap `0.032149328254635276`
- train: `science_train` (targeted); attempts `1386`, audit_blocked `572`, avg_gap `0.03210658879872262`

### Recent Module Evidence
- `science_backend`: attempts `1408`, audit_blocked `593`, avg_gap `0.03221607437259832`
- `science_model`: attempts `1408`, audit_blocked `593`, avg_gap `0.03221607437259832`
- `science_eval`: attempts `1400`, audit_blocked `585`, avg_gap `0.03215743930684286`
- `science_config`: attempts `1393`, audit_blocked `579`, avg_gap `0.032149328254635276`

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
- summary: `The lab has stayed on `science_train` for 4 recent candidates; inject a novelty step.`
- current_mechanism_streak: `4`
- novelty_step_recommended: `True`
