# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T08:39:40+00:00`
- last_heartbeat: `2026-04-02T10:09:29+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0368`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0368`
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
- active_candidate: `cand_0368`
- backend_status: `finished`
- backend_pid: `2365649`
- backend_started_at: `2026-04-02T09:59:27+00:00`
- backend_last_poll_at: `2026-04-02T10:09:29+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_0368`: outcome `dead_end`; diagnosis `complete`; benchmark `0.38643093195620987`
- `cand_0367`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4232336556853806`
- `cand_0366`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4470014143254252`
- `cand_0365`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37188505787254345`
- `cand_0364`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3757354205318799`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.400857, audit averaged 0.333969, and the mean transfer gap was 0.066888.`
- recent benchmark avg: `0.4008572960742878`
- recent audit avg: `0.3339689372731761`
- recent transfer gap avg: `0.06688835880111171`
- `cand_0368`: benchmark `0.38643093195620987`, audit `0.3311649105529011`, gap `0.055266021403308774`
- `cand_0367`: benchmark `0.4232336556853806`, audit `0.3450997835993834`, gap `0.0781338720859972`
- `cand_0366`: benchmark `0.4470014143254252`, audit `0.3208932731589951`, gap `0.1261081411664301`
- `cand_0365`: benchmark `0.37188505787254345`, audit `0.3508391375275096`, gap `0.02104592034503383`
- `cand_0364`: benchmark `0.3757354205318799`, audit `0.32184758152709125`, gap `0.05388783900478866`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 7 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (259 candidate(s), avg transfer gap 0.038681).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 791.0 MB on average, leaving most VRAM unused. 4 scored candidate(s) have landed since structural commit `4c8bac2`.`
- scored_candidates_since_change: `4`
- last_structural_commit: `4c8bac2`
### Chosen Lever Values
- source_candidate: `cand_0368`
- model: `hidden_dim=160, k_neighbors=10`

### Effective Backend Settings
- source_candidate: `cand_0368`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=10, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `259`, audit_blocked `150`, avg_gap `0.038681254374823296`
- loss: `science_loss` (available); attempts `244`, audit_blocked `136`, avg_gap `0.03867911345467295`
- eval: `science_eval` (available); attempts `251`, audit_blocked `142`, avg_gap `0.03855265092887099`
- config: `science_config` (available); attempts `244`, audit_blocked `136`, avg_gap `0.03867911345467295`
- train: `science_train` (targeted); attempts `237`, audit_blocked `129`, avg_gap `0.03862051916846583`

### Recent Module Evidence
- `science_backend`: attempts `259`, audit_blocked `150`, avg_gap `0.038681254374823296`
- `science_model`: attempts `259`, audit_blocked `150`, avg_gap `0.038681254374823296`
- `science_eval`: attempts `251`, audit_blocked `142`, avg_gap `0.03855265092887099`
- `science_config`: attempts `244`, audit_blocked `136`, avg_gap `0.03867911345467295`

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
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
