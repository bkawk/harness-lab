# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T11:21:05+00:00`
- last_heartbeat: `2026-04-02T14:43:29+00:00`
- cycles_completed: `18`
- genesis seed: `cand_0001`
- last candidate: `cand_0393`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0393`
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
- active_candidate: `cand_0393`
- backend_status: `finished`
- backend_pid: `2374443`
- backend_started_at: `2026-04-02T14:33:27+00:00`
- backend_last_poll_at: `2026-04-02T14:43:29+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0393`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3627436836157032`
- `cand_0392`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3435297974328567`
- `cand_0391`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3132285381922586`
- `cand_0390`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3432851878462814`
- `cand_0389`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2960954506350956`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.331777, audit averaged 0.306572, and the mean transfer gap was 0.025205.`
- recent benchmark avg: `0.3317765315444391`
- recent audit avg: `0.3065719909091509`
- recent transfer gap avg: `0.025204540635288247`
- `cand_0393`: benchmark `0.3627436836157032`, audit `0.31140796359184814`, gap `0.05133572002385506`
- `cand_0392`: benchmark `0.3435297974328567`, audit `0.3496829889023191`, gap `-0.00615319146946236`
- `cand_0391`: benchmark `0.3132285381922586`, audit `0.344813289292644`, gap `-0.03158475110038539`
- `cand_0390`: benchmark `0.3432851878462814`, audit `0.3131957289352084`, gap `0.030089458911073008`
- `cand_0389`: benchmark `0.2960954506350956`, audit `0.2137599838237347`, gap `0.08233546681136092`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `2`
- novelty_cycle_priority: `normal`

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
- summary: `Recent backend evolution is concentrated in science_backend (284 candidate(s), avg transfer gap 0.038870).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 800.8 MB on average, leaving most VRAM unused. 8 scored candidate(s) have landed since structural commit `4d32d84`.`
- scored_candidates_since_change: `8`
- last_structural_commit: `4d32d84`
### Chosen Lever Values
- source_candidate: `cand_0393`
- train: `batch_size=3, eval_batch_size=4`

### Effective Backend Settings
- source_candidate: `cand_0393`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.05, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0004, weight_decay=0.0001, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=4, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `284`, audit_blocked `160`, avg_gap `0.038870364015143086`
- loss: `science_loss` (available); attempts `269`, audit_blocked `146`, avg_gap `0.0388794685826931`
- eval: `science_eval` (available); attempts `276`, audit_blocked `152`, avg_gap `0.03876045715384693`
- config: `science_config` (available); attempts `269`, audit_blocked `146`, avg_gap `0.0388794685826931`
- train: `science_train` (targeted); attempts `262`, audit_blocked `139`, avg_gap `0.03883292901221608`

### Recent Module Evidence
- `science_backend`: attempts `284`, audit_blocked `160`, avg_gap `0.038870364015143086`
- `science_model`: attempts `284`, audit_blocked `160`, avg_gap `0.038870364015143086`
- `science_eval`: attempts `276`, audit_blocked `152`, avg_gap `0.03876045715384693`
- `science_config`: attempts `269`, audit_blocked `146`, avg_gap `0.0388794685826931`

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
- target_file: `src/harness_lab/science_loss.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_loss.py, tests/test_science_loss.py`
- focused_tests: `tests/test_science_loss.py`
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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
