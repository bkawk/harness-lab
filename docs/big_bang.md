# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T06:11:03+00:00`
- cycles_completed: `46`
- genesis seed: `cand_0001`
- last candidate: `cand_0344`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0344`
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
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0344`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3639524579646608`
- `cand_0343`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39182056896791795`
- `cand_0342`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3528256253964448`
- `cand_0341`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4371920677268424`
- `cand_0340`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36952832702851973`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.383064, audit averaged 0.326704, and the mean transfer gap was 0.056360.`
- recent benchmark avg: `0.3830638094168771`
- recent audit avg: `0.3267038683065328`
- recent transfer gap avg: `0.056359941110344335`
- `cand_0344`: benchmark `0.3639524579646608`, audit `0.32176946411148605`, gap `0.042182993853174755`
- `cand_0343`: benchmark `0.39182056896791795`, audit `0.3137169969878919`, gap `0.07810357198002604`
- `cand_0342`: benchmark `0.3528256253964448`, audit `0.3245052110688219`, gap `0.02832041432762289`
- `cand_0341`: benchmark `0.4371920677268424`, audit `0.33252857891992843`, gap `0.10466348880691395`
- `cand_0340`: benchmark `0.36952832702851973`, audit `0.3409990904445357`, gap `0.02852923658398404`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (236 candidate(s), avg transfer gap 0.038411).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 728.5 MB on average, leaving most VRAM unused. 45 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `45`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0344`
- model: `global_dim=256, hidden_dim=160`

### Effective Backend Settings
- source_candidate: `cand_0344`
- model: `hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `236`, audit_blocked `144`, avg_gap `0.0384112424319501`
- loss: `science_loss` (targeted); attempts `221`, audit_blocked `130`, avg_gap `0.03838970636112422`
- eval: `science_eval` (available); attempts `228`, audit_blocked `136`, avg_gap `0.03825996134552449`
- config: `science_config` (available); attempts `221`, audit_blocked `130`, avg_gap `0.03838970636112422`
- train: `science_train` (available); attempts `214`, audit_blocked `123`, avg_gap `0.03831459027969195`

### Recent Module Evidence
- `science_backend`: attempts `236`, audit_blocked `144`, avg_gap `0.0384112424319501`
- `science_model`: attempts `236`, audit_blocked `144`, avg_gap `0.0384112424319501`
- `science_eval`: attempts `228`, audit_blocked `136`, avg_gap `0.03825996134552449`
- `science_config`: attempts `221`, audit_blocked `130`, avg_gap `0.03838970636112422`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
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
