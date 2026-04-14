# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-14T08:00:09+00:00`
- cycles_completed: `1482`
- genesis seed: `cand_0001`
- last candidate: `cand_1906`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `231`

## Latest Step
- candidate: `cand_1906`
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
- active_candidate: `cand_1906`
- backend_status: `finished`
- backend_pid: `2977809`
- backend_started_at: `2026-04-14T07:50:04+00:00`
- backend_last_poll_at: `2026-04-14T08:00:06+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_1906`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32158203444162353`
- `cand_1905`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3029182930509789`
- `cand_1904`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3745853125190235`
- `cand_1903`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3251722039304938`
- `cand_1902`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3374945719632534`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_1625` -> gap `-0.00015162972740001557`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.332350, audit averaged 0.322548, and the mean transfer gap was 0.009802.`
- recent benchmark avg: `0.33235048318107463`
- recent audit avg: `0.32254846661245706`
- recent transfer gap avg: `0.009802016568617521`
- `cand_1906`: benchmark `0.32158203444162353`, audit `0.3063844384316158`, gap `0.015197596010007752`
- `cand_1905`: benchmark `0.3029182930509789`, audit `0.3428307814542024`, gap `-0.039912488403223534`
- `cand_1904`: benchmark `0.3745853125190235`, audit `0.30583935554893016`, gap `0.06874595697009334`
- `cand_1903`: benchmark `0.3251722039304938`, audit `0.3020478861065385`, gap `0.023124317823955298`
- `cand_1902`: benchmark `0.3374945719632534`, audit `0.35563987152099863`, gap `-0.018145299557745243`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (1797 candidate(s), avg transfer gap 0.032177).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 756.8 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_1906`
- train: `batch_size=3, grad_clip=1.2`

### Effective Backend Settings
- source_candidate: `cand_1906`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0003, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=2, grad_clip=1.2, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `1797`, audit_blocked `752`, avg_gap `0.03217670709718506`
- loss: `science_loss` (available); attempts `1782`, audit_blocked `738`, avg_gap `0.032124466172162566`
- eval: `science_eval` (available); attempts `1789`, audit_blocked `744`, avg_gap `0.032130867311506724`
- config: `science_config` (available); attempts `1782`, audit_blocked `738`, avg_gap `0.032124466172162566`
- train: `science_train` (targeted); attempts `1775`, audit_blocked `731`, avg_gap `0.03209115457514545`

### Recent Module Evidence
- `science_backend`: attempts `1797`, audit_blocked `752`, avg_gap `0.03217670709718506`
- `science_model`: attempts `1797`, audit_blocked `752`, avg_gap `0.03217670709718506`
- `science_eval`: attempts `1789`, audit_blocked `744`, avg_gap `0.032130867311506724`
- `science_config`: attempts `1782`, audit_blocked `738`, avg_gap `0.032124466172162566`

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
- summary: `The lab has stayed on `science_train` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
