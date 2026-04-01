# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T09:16:42+00:00`
- last_heartbeat: `2026-04-01T10:30:20+00:00`
- cycles_completed: `7`
- genesis seed: `cand_0001`
- last candidate: `cand_0228`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `7`

## Latest Step
- candidate: `cand_0228`
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
- `cand_0228`: outcome `improved`; diagnosis `complete`; benchmark `0.2755627412073406`
- `cand_0227`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33497287478847104`
- `cand_0226`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3611682584278251`
- `cand_0225`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36804312468236894`
- `cand_0224`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3378123307088491`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.335512, audit averaged 0.306001, and the mean transfer gap was 0.029510.`
- recent benchmark avg: `0.33551186596297095`
- recent audit avg: `0.30600145923201266`
- recent transfer gap avg: `0.029510406730958283`
- `cand_0228`: benchmark `0.2755627412073406`, audit `0.30889219018925673`, gap `-0.03332944898191614`
- `cand_0227`: benchmark `0.33497287478847104`, audit `0.32848591429130014`, gap `0.006486960497170902`
- `cand_0226`: benchmark `0.3611682584278251`, audit `0.277784229999773`, gap `0.08338402842805209`
- `cand_0225`: benchmark `0.36804312468236894`, audit `0.2784978771929737`, gap `0.08954524748939524`
- `cand_0224`: benchmark `0.3378123307088491`, audit `0.33634708448675976`, gap `0.0014652462220893225`

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
- summary: `Recent backend evolution is concentrated in science_backend (120 candidate(s), avg transfer gap 0.038103).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038103. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 589.9 MB on average, leaving most VRAM unused. 6 scored candidate(s) have landed since structural commit `2be55f0`.`
- scored_candidates_since_change: `6`
- last_structural_commit: `2be55f0`
### Chosen Lever Values
- source_candidate: `cand_0228`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0228`
- model: `hidden_dim=96, global_dim=192, instance_dim=12, k_neighbors=8, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `120`, audit_blocked `97`, avg_gap `0.03810267443787699`
- loss: `science_loss` (available); attempts `105`, audit_blocked `83`, avg_gap `0.03801254224977465`
- eval: `science_eval` (available); attempts `112`, audit_blocked `89`, avg_gap `0.03777417340325338`
- config: `science_config` (available); attempts `105`, audit_blocked `83`, avg_gap `0.03801254224977465`
- train: `science_train` (available); attempts `98`, audit_blocked `76`, avg_gap `0.03782035811055218`

### Recent Module Evidence
- `science_backend`: attempts `120`, audit_blocked `97`, avg_gap `0.03810267443787699`
- `science_model`: attempts `120`, audit_blocked `97`, avg_gap `0.03810267443787699`
- `science_eval`: attempts `112`, audit_blocked `89`, avg_gap `0.03777417340325338`
- `science_config`: attempts `105`, audit_blocked `83`, avg_gap `0.03801254224977465`

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
