# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-05T02:29:21+00:00`
- cycles_completed: `292`
- genesis seed: `cand_0001`
- last candidate: `cand_0716`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `38`

## Latest Step
- candidate: `cand_0716`
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
- active_candidate: `cand_0716`
- backend_status: `finished`
- backend_pid: `2729909`
- backend_started_at: `2026-04-05T02:19:18+00:00`
- backend_last_poll_at: `2026-04-05T02:29:20+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0716`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36887444849436013`
- `cand_0715`: outcome `dead_end`; diagnosis `complete`; benchmark `0.30483020133200694`
- `cand_0714`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3583761155096592`
- `cand_0713`: outcome `dead_end`; diagnosis `complete`; benchmark `0.419090860864476`
- `cand_0712`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3668779257860467`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0485` -> gap `0.00016547110388953623`
- best stable: `cand_0677` -> audit `0.3845551107118892`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.363610, audit averaged 0.335917, and the mean transfer gap was 0.027693.`
- recent benchmark avg: `0.3636099103973098`
- recent audit avg: `0.3359165576766353`
- recent transfer gap avg: `0.027693352720674524`
- `cand_0716`: benchmark `0.36887444849436013`, audit `0.3432151063613472`, gap `0.025659342133012908`
- `cand_0715`: benchmark `0.30483020133200694`, audit `0.3183870002980156`, gap `-0.013556798966008643`
- `cand_0714`: benchmark `0.3583761155096592`, audit `0.34612018547582457`, gap `0.012255930033834628`
- `cand_0713`: benchmark `0.419090860864476`, audit `0.3431912118355593`, gap `0.07589964902891672`
- `cand_0712`: benchmark `0.3668779257860467`, audit `0.3286692844124297`, gap `0.038208641373617014`

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
- summary: `Mechanisms initial_harness, science_loss, science_train exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (607 candidate(s), avg transfer gap 0.035166).`
- recommended_action: `wait`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 940.5 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_0716`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0716`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `607`, audit_blocked `278`, avg_gap `0.035166163416383095`
- loss: `science_loss` (available); attempts `592`, audit_blocked `264`, avg_gap `0.03507777602817912`
- eval: `science_eval` (available); attempts `599`, audit_blocked `270`, avg_gap `0.03506639107013497`
- config: `science_config` (available); attempts `592`, audit_blocked `264`, avg_gap `0.03507777602817912`
- train: `science_train` (targeted); attempts `585`, audit_blocked `257`, avg_gap `0.035010288518624616`

### Recent Module Evidence
- `science_backend`: attempts `607`, audit_blocked `278`, avg_gap `0.035166163416383095`
- `science_model`: attempts `607`, audit_blocked `278`, avg_gap `0.035166163416383095`
- `science_eval`: attempts `599`, audit_blocked `270`, avg_gap `0.03506639107013497`
- `science_config`: attempts `592`, audit_blocked `264`, avg_gap `0.03507777602817912`

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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
