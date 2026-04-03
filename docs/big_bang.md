# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T12:40:43+00:00`
- cycles_completed: `88`
- genesis seed: `cand_0001`
- last candidate: `cand_0512`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `12`

## Latest Step
- candidate: `cand_0512`
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
- active_candidate: `cand_0512`
- backend_status: `finished`
- backend_pid: `2653543`
- backend_started_at: `2026-04-03T12:30:40+00:00`
- backend_last_poll_at: `2026-04-03T12:40:42+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0512`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36787226195825184`
- `cand_0511`: outcome `dead_end`; diagnosis `complete`; benchmark `0.38019264028250366`
- `cand_0510`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3372742959685232`
- `cand_0509`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4030299967029688`
- `cand_0508`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39413133893371766`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0491` -> audit `0.3820240880032215`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.376500, audit averaged 0.331079, and the mean transfer gap was 0.045421.`
- recent benchmark avg: `0.376500106769193`
- recent audit avg: `0.33107941989157447`
- recent transfer gap avg: `0.04542068687761854`
- `cand_0512`: benchmark `0.36787226195825184`, audit `0.3359542132521637`, gap `0.031918048706088165`
- `cand_0511`: benchmark `0.38019264028250366`, audit `0.2901210386936207`, gap `0.09007160158888294`
- `cand_0510`: benchmark `0.3372742959685232`, audit `0.3364599916508174`, gap `0.000814304317705794`
- `cand_0509`: benchmark `0.4030299967029688`, audit `0.3712418994404636`, gap `0.0317880972625052`
- `cand_0508`: benchmark `0.39413133893371766`, audit `0.32161995642080704`, gap `0.07251138251291062`

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
- summary: `Mechanisms initial_harness, science_train, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (403 candidate(s), avg transfer gap 0.034923).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 869.0 MB on average, leaving most VRAM unused. 53 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `53`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0512`
- model: `hidden_dim=160, instance_modulation_scale=0.15`

### Effective Backend Settings
- source_candidate: `cand_0512`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `403`, audit_blocked `203`, avg_gap `0.03492287494801037`
- loss: `science_loss` (available); attempts `388`, audit_blocked `189`, avg_gap `0.034774607487876696`
- eval: `science_eval` (available); attempts `395`, audit_blocked `195`, avg_gap `0.03476183923258203`
- config: `science_config` (available); attempts `388`, audit_blocked `189`, avg_gap `0.034774607487876696`
- train: `science_train` (targeted); attempts `381`, audit_blocked `182`, avg_gap `0.03466185037225031`

### Recent Module Evidence
- `science_backend`: attempts `403`, audit_blocked `203`, avg_gap `0.03492287494801037`
- `science_model`: attempts `403`, audit_blocked `203`, avg_gap `0.03492287494801037`
- `science_eval`: attempts `395`, audit_blocked `195`, avg_gap `0.03476183923258203`
- `science_config`: attempts `388`, audit_blocked `189`, avg_gap `0.034774607487876696`

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
