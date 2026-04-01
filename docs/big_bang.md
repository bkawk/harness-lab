# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T13:40:56+00:00`
- last_heartbeat: `2026-04-01T14:45:19+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0254`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0254`
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
- `cand_0254`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3687962834685289`
- `cand_0253`: outcome `dead_end`; diagnosis `complete`; benchmark `0.30600007176038846`
- `cand_0252`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3606567678547835`
- `cand_0251`: outcome `dead_end`; diagnosis `complete`; benchmark `0.31747032273278625`
- `cand_0250`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3289862775067053`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.336382, audit averaged 0.307116, and the mean transfer gap was 0.029266.`
- recent benchmark avg: `0.33638194466463844`
- recent audit avg: `0.30711618773163724`
- recent transfer gap avg: `0.02926575693300123`
- `cand_0254`: benchmark `0.3687962834685289`, audit `0.3141337039756543`, gap `0.05466257949287456`
- `cand_0253`: benchmark `0.30600007176038846`, audit `0.2908975094695538`, gap `0.015102562290834676`
- `cand_0252`: benchmark `0.3606567678547835`, audit `0.3095993536613364`, gap `0.051057414193447115`
- `cand_0251`: benchmark `0.31747032273278625`, audit `0.3103895433766079`, gap `0.007080779356178346`
- `cand_0250`: benchmark `0.3289862775067053`, audit `0.31056082817503383`, gap `0.01842544933167145`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Mechanisms initial_harness, science_model, budget_policy_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `11`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (146 candidate(s), avg transfer gap 0.036658).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.036658. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 678.8 MB on average, leaving most VRAM unused. 5 scored candidate(s) have landed since structural commit `48bbe21`.`
- scored_candidates_since_change: `5`
- last_structural_commit: `48bbe21`
### Chosen Lever Values
- source_candidate: `cand_0254`
- model: `instance_dim=24`

### Effective Backend Settings
- source_candidate: `cand_0254`
- model: `hidden_dim=96, global_dim=256, instance_dim=24, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `146`, audit_blocked `115`, avg_gap `0.0366578957415318`
- loss: `science_loss` (available); attempts `131`, audit_blocked `101`, avg_gap `0.036413917270188105`
- eval: `science_eval` (available); attempts `138`, audit_blocked `107`, avg_gap `0.03629711482163062`
- config: `science_config` (available); attempts `131`, audit_blocked `101`, avg_gap `0.036413917270188105`
- train: `science_train` (available); attempts `124`, audit_blocked `94`, avg_gap `0.03616074088182159`

### Recent Module Evidence
- `science_backend`: attempts `146`, audit_blocked `115`, avg_gap `0.0366578957415318`
- `science_model`: attempts `146`, audit_blocked `115`, avg_gap `0.0366578957415318`
- `science_eval`: attempts `138`, audit_blocked `107`, avg_gap `0.03629711482163062`
- `science_config`: attempts `131`, audit_blocked `101`, avg_gap `0.036413917270188105`

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
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
