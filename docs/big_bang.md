# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T08:45:54+00:00`
- last_heartbeat: `2026-04-01T08:55:57+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0219`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0219`
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
- `cand_0219`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34268582758993893`
- `cand_0218`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0217`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0216`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0215`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.39496752181409667`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 2 scored candidates, benchmark averaged 0.368827, audit averaged 0.315112, and the mean transfer gap was 0.053714.`
- recent benchmark avg: `0.3688266747020178`
- recent audit avg: `0.3151124351527974`
- recent transfer gap avg: `0.05371423954922039`
- `cand_0219`: benchmark `0.34268582758993893`, audit `0.3044089050067349`, gap `0.03827692258320403`
- `cand_0215`: benchmark `0.39496752181409667`, audit `0.3258159652988599`, gap `0.06915155651523675`

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
- summary: `Recent backend evolution is concentrated in science_backend (111 candidate(s), avg transfer gap 0.038718).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038718. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 0 scored candidate(s) have landed since structural commit `5b04832`.`
- secondary_context: `Recent real-backend runs are only using about 590.2 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `5b04832`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `5b04832`
### Chosen Lever Values
- source_candidate: `cand_0219`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0219`
- model: `hidden_dim=96, global_dim=192, instance_dim=12, k_neighbors=8, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `111`, audit_blocked `90`, avg_gap `0.03871765269435787`
- loss: `science_loss` (available); attempts `96`, audit_blocked `76`, avg_gap `0.03871819450724304`
- eval: `science_eval` (available); attempts `103`, audit_blocked `82`, avg_gap `0.03841379486161446`
- config: `science_config` (available); attempts `96`, audit_blocked `76`, avg_gap `0.03871819450724304`
- train: `science_train` (available); attempts `89`, audit_blocked `69`, avg_gap `0.038568536526626805`

### Recent Module Evidence
- `science_backend`: attempts `111`, audit_blocked `90`, avg_gap `0.03871765269435787`
- `science_model`: attempts `111`, audit_blocked `90`, avg_gap `0.03871765269435787`
- `science_eval`: attempts `103`, audit_blocked `82`, avg_gap `0.03841379486161446`
- `science_config`: attempts `96`, audit_blocked `76`, avg_gap `0.03871819450724304`

## External Review
- status: `idle`
- trigger_reason: `-`
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
