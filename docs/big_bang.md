# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T09:16:42+00:00`
- last_heartbeat: `2026-04-01T12:26:56+00:00`
- cycles_completed: `18`
- genesis seed: `cand_0001`
- last candidate: `cand_0239`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `18`

## Latest Step
- candidate: `cand_0239`
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
- `cand_0239`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3088403526545396`
- `cand_0238`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29249757131017395`
- `cand_0237`: outcome `improved`; diagnosis `complete`; benchmark `0.2658084345931639`
- `cand_0236`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3329986764163364`
- `cand_0235`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3583763005625271`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.311704, audit averaged 0.286252, and the mean transfer gap was 0.025452.`
- recent benchmark avg: `0.31170426710734817`
- recent audit avg: `0.2862518203237875`
- recent transfer gap avg: `0.025452446783560734`
- `cand_0239`: benchmark `0.3088403526545396`, audit `0.23352010126097195`, gap `0.07532025139356763`
- `cand_0238`: benchmark `0.29249757131017395`, audit `0.29138060674689525`, gap `0.0011169645632786995`
- `cand_0237`: benchmark `0.2658084345931639`, audit `0.30813718195382933`, gap `-0.04232874736066544`
- `cand_0236`: benchmark `0.3329986764163364`, audit `0.3254096805490543`, gap `0.007588995867282122`
- `cand_0235`: benchmark `0.3583763005625271`, audit `0.27281153110818646`, gap `0.08556476945434066`

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
- summary: `Recent backend evolution is concentrated in science_backend (131 candidate(s), avg transfer gap 0.037372).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.037372. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 594.0 MB on average, leaving most VRAM unused. 17 scored candidate(s) have landed since structural commit `2be55f0`.`
- scored_candidates_since_change: `17`
- last_structural_commit: `2be55f0`
### Chosen Lever Values
- source_candidate: `cand_0239`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0239`
- model: `hidden_dim=128, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.1, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `131`, audit_blocked `107`, avg_gap `0.037372146492276895`
- loss: `science_loss` (available); attempts `116`, audit_blocked `93`, avg_gap `0.037194882821445535`
- eval: `science_eval` (available); attempts `123`, audit_blocked `99`, avg_gap `0.037023728384582386`
- config: `science_config` (available); attempts `116`, audit_blocked `93`, avg_gap `0.037194882821445535`
- train: `science_train` (available); attempts `109`, audit_blocked `86`, avg_gap `0.03696623817245684`

### Recent Module Evidence
- `science_backend`: attempts `131`, audit_blocked `107`, avg_gap `0.037372146492276895`
- `science_model`: attempts `131`, audit_blocked `107`, avg_gap `0.037372146492276895`
- `science_eval`: attempts `123`, audit_blocked `99`, avg_gap `0.037023728384582386`
- `science_config`: attempts `116`, audit_blocked `93`, avg_gap `0.037194882821445535`

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
