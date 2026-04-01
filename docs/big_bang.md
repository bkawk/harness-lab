# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T09:16:42+00:00`
- last_heartbeat: `2026-04-01T10:40:56+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0229`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `8`

## Latest Step
- candidate: `cand_0229`
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
- `cand_0229`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2923165936023367`
- `cand_0228`: outcome `improved`; diagnosis `complete`; benchmark `0.2755627412073406`
- `cand_0227`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33497287478847104`
- `cand_0226`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3611682584278251`
- `cand_0225`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36804312468236894`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.326413, audit averaged 0.297625, and the mean transfer gap was 0.028788.`
- recent benchmark avg: `0.3264127185416685`
- recent audit avg: `0.2976249479820544`
- recent transfer gap avg: `0.02878777055961409`
- `cand_0229`: benchmark `0.2923165936023367`, audit `0.29446452823696834`, gap `-0.002147934634631643`
- `cand_0228`: benchmark `0.2755627412073406`, audit `0.30889219018925673`, gap `-0.03332944898191614`
- `cand_0227`: benchmark `0.33497287478847104`, audit `0.32848591429130014`, gap `0.006486960497170902`
- `cand_0226`: benchmark `0.3611682584278251`, audit `0.277784229999773`, gap `0.08338402842805209`
- `cand_0225`: benchmark `0.36804312468236894`, audit `0.2784978771929737`, gap `0.08954524748939524`

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
- summary: `Recent backend evolution is concentrated in science_backend (121 candidate(s), avg transfer gap 0.037737).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.037737. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 587.4 MB on average, leaving most VRAM unused. 7 scored candidate(s) have landed since structural commit `2be55f0`.`
- scored_candidates_since_change: `7`
- last_structural_commit: `2be55f0`
### Chosen Lever Values
- source_candidate: `cand_0229`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0229`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `121`, audit_blocked `98`, avg_gap `0.03773675980994509`
- loss: `science_loss` (available); attempts `106`, audit_blocked `84`, avg_gap `0.03759420394889542`
- eval: `science_eval` (available); attempts `113`, audit_blocked `90`, avg_gap `0.03738278018719569`
- config: `science_config` (available); attempts `106`, audit_blocked `84`, avg_gap `0.03759420394889542`
- train: `science_train` (available); attempts `99`, audit_blocked `77`, avg_gap `0.037371276169595055`

### Recent Module Evidence
- `science_backend`: attempts `121`, audit_blocked `98`, avg_gap `0.03773675980994509`
- `science_model`: attempts `121`, audit_blocked `98`, avg_gap `0.03773675980994509`
- `science_eval`: attempts `113`, audit_blocked `90`, avg_gap `0.03738278018719569`
- `science_config`: attempts `106`, audit_blocked `84`, avg_gap `0.03759420394889542`

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
