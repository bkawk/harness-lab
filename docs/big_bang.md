# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T17:29:00+00:00`
- cycles_completed: `33`
- genesis seed: `cand_0001`
- last candidate: `cand_0408`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0408`
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
- active_candidate: `cand_0408`
- backend_status: `finished`
- backend_pid: `2379920`
- backend_started_at: `2026-04-02T17:18:57+00:00`
- backend_last_poll_at: `2026-04-02T17:28:59+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0408`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2762151021978113`
- `cand_0407`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3858972793087505`
- `cand_0406`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39101079665034877`
- `cand_0405`: outcome `keeper`; diagnosis `complete`; benchmark `0.31971953534912556`
- `cand_0404`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3200723127134295`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.338583, audit averaged 0.306338, and the mean transfer gap was 0.032245.`
- recent benchmark avg: `0.3385830052438931`
- recent audit avg: `0.30633758778688913`
- recent transfer gap avg: `0.03224541745700397`
- `cand_0408`: benchmark `0.2762151021978113`, audit `0.2615393429372923`, gap `0.014675759260519006`
- `cand_0407`: benchmark `0.3858972793087505`, audit `0.31233859378247064`, gap `0.07355868552627987`
- `cand_0406`: benchmark `0.39101079665034877`, audit `0.34253770428565566`, gap `0.048473092364693104`
- `cand_0405`: benchmark `0.31971953534912556`, audit `0.32649386043764034`, gap `-0.0067743250885147765`
- `cand_0404`: benchmark `0.3200723127134295`, audit `0.2887784374913869`, gap `0.03129387522204263`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (299 candidate(s), avg transfer gap 0.038110).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 786.2 MB on average, leaving most VRAM unused. 23 scored candidate(s) have landed since structural commit `4d32d84`.`
- scored_candidates_since_change: `23`
- last_structural_commit: `4d32d84`
### Chosen Lever Values
- source_candidate: `cand_0408`
- train: `batch_size=3, eval_batch_size=3, grad_clip=0.8`

### Effective Backend Settings
- source_candidate: `cand_0408`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=0.8, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `299`, audit_blocked `165`, avg_gap `0.03810999013484607`
- loss: `science_loss` (available); attempts `284`, audit_blocked `151`, avg_gap `0.03807681312264153`
- eval: `science_eval` (available); attempts `291`, audit_blocked `157`, avg_gap `0.037983093280741724`
- config: `science_config` (available); attempts `284`, audit_blocked `151`, avg_gap `0.03807681312264153`
- train: `science_train` (targeted); attempts `277`, audit_blocked `144`, avg_gap `0.03801043284787738`

### Recent Module Evidence
- `science_backend`: attempts `299`, audit_blocked `165`, avg_gap `0.03810999013484607`
- `science_model`: attempts `299`, audit_blocked `165`, avg_gap `0.03810999013484607`
- `science_eval`: attempts `291`, audit_blocked `157`, avg_gap `0.037983093280741724`
- `science_config`: attempts `284`, audit_blocked `151`, avg_gap `0.03807681312264153`

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
