# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T08:45:54+00:00`
- last_heartbeat: `2026-04-01T09:06:33+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0220`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0220`
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
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0220`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32856356006880877`
- `cand_0219`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34268582758993893`
- `cand_0218`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0217`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0216`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 2 scored candidates, benchmark averaged 0.335625, audit averaged 0.309635, and the mean transfer gap was 0.025990.`
- recent benchmark avg: `0.3356246938293739`
- recent audit avg: `0.3096348678681997`
- recent transfer gap avg: `0.025989825961174134`
- `cand_0220`: benchmark `0.32856356006880877`, audit `0.31486083072966453`, gap `0.013702729339144237`
- `cand_0219`: benchmark `0.34268582758993893`, audit `0.3044089050067349`, gap `0.03827692258320403`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- summary: `Mechanisms initial_harness, science_model, budget_policy_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `9`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (112 candidate(s), avg transfer gap 0.038472).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038472. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 1 scored candidate(s) have landed since structural commit `5b04832`.`
- secondary_context: `Recent real-backend runs are only using about 590.9 MB on average, leaving most VRAM unused. 1 scored candidate(s) have landed since structural commit `5b04832`.`
- scored_candidates_since_change: `1`
- last_structural_commit: `5b04832`
### Chosen Lever Values
- source_candidate: `cand_0220`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0220`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `112`, audit_blocked `91`, avg_gap `0.03847240834773812`
- loss: `science_loss` (available); attempts `97`, audit_blocked `77`, avg_gap `0.03843392785760555`
- eval: `science_eval` (available); attempts `104`, audit_blocked `83`, avg_gap `0.038150911185843496`
- config: `science_config` (available); attempts `97`, audit_blocked `77`, avg_gap `0.03843392785760555`
- train: `science_train` (available); attempts `90`, audit_blocked `70`, avg_gap `0.03826155125270727`

### Recent Module Evidence
- `science_backend`: attempts `112`, audit_blocked `91`, avg_gap `0.03847240834773812`
- `science_model`: attempts `112`, audit_blocked `91`, avg_gap `0.03847240834773812`
- `science_eval`: attempts `104`, audit_blocked `83`, avg_gap `0.038150911185843496`
- `science_config`: attempts `97`, audit_blocked `77`, avg_gap `0.03843392785760555`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 2 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `science_model` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
