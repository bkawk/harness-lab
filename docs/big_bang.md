# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-03T04:12:36+00:00`
- cycles_completed: `42`
- genesis seed: `cand_0001`
- last candidate: `cand_0466`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0466`
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
- active_candidate: `cand_0466`
- backend_status: `finished`
- backend_pid: `2395972`
- backend_started_at: `2026-04-03T04:02:34+00:00`
- backend_last_poll_at: `2026-04-03T04:12:36+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0466`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33485144855971183`
- `cand_0465`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3945716054801879`
- `cand_0464`: outcome `keeper`; diagnosis `complete`; benchmark `0.3215029879937584`
- `cand_0463`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3494029675098201`
- `cand_0462`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3162958489259673`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0455` -> audit `0.37001045360546564`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.343325, audit averaged 0.306574, and the mean transfer gap was 0.036751.`
- recent benchmark avg: `0.3433249716938891`
- recent audit avg: `0.30657394297512547`
- recent transfer gap avg: `0.03675102871876362`
- `cand_0466`: benchmark `0.33485144855971183`, audit `0.2775716683119625`, gap `0.05727978024774932`
- `cand_0465`: benchmark `0.3945716054801879`, audit `0.2995474245039067`, gap `0.09502418097628118`
- `cand_0464`: benchmark `0.3215029879937584`, audit `0.309440642511061`, gap `0.012062345482697412`
- `cand_0463`: benchmark `0.3494029675098201`, audit `0.3559340561318377`, gap `-0.006531088622017622`
- `cand_0462`: benchmark `0.3162958489259673`, audit `0.29037592341685947`, gap `0.025919925509107822`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, science_loss, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (357 candidate(s), avg transfer gap 0.036100).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 807.5 MB on average, leaving most VRAM unused. 7 scored candidate(s) have landed since structural commit `d21d25b`.`
- scored_candidates_since_change: `7`
- last_structural_commit: `d21d25b`
### Chosen Lever Values
- source_candidate: `cand_0466`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.2`

### Effective Backend Settings
- source_candidate: `cand_0466`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.08, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.2, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `357`, audit_blocked `190`, avg_gap `0.036099881875852155`
- loss: `science_loss` (available); attempts `342`, audit_blocked `176`, avg_gap `0.03598256888310193`
- eval: `science_eval` (available); attempts `349`, audit_blocked `182`, avg_gap `0.0359451619230434`
- config: `science_config` (available); attempts `342`, audit_blocked `176`, avg_gap `0.03598256888310193`
- train: `science_train` (targeted); attempts `335`, audit_blocked `169`, avg_gap `0.03588052948041903`

### Recent Module Evidence
- `science_backend`: attempts `357`, audit_blocked `190`, avg_gap `0.036099881875852155`
- `science_model`: attempts `357`, audit_blocked `190`, avg_gap `0.036099881875852155`
- `science_eval`: attempts `349`, audit_blocked `182`, avg_gap `0.0359451619230434`
- `science_config`: attempts `342`, audit_blocked `176`, avg_gap `0.03598256888310193`

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
- decision_state: `iterate`
- decision_reason: ``science_train` is already the active recent seam with outcomes ['keeper', 'dead_end', 'dead_end'], so keep iterating on that line rather than issuing a brand-new brief.`
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
- reason: `Decision state is `iterate`, so autonomous code mutation stays blocked.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
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
