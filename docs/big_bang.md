# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T13:40:56+00:00`
- last_heartbeat: `2026-04-01T15:07:18+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0256`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0256`
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
- `cand_0256`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2829415365286318`
- `cand_0255`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32164046189516404`
- `cand_0254`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3687962834685289`
- `cand_0253`: outcome `dead_end`; diagnosis `complete`; benchmark `0.30600007176038846`
- `cand_0252`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3606567678547835`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.328007, audit averaged 0.299545, and the mean transfer gap was 0.028462.`
- recent benchmark avg: `0.3280070243014993`
- recent audit avg: `0.29954513009026107`
- recent transfer gap avg: `0.028461894211238258`
- `cand_0256`: benchmark `0.2829415365286318`, audit `0.2678857235138864`, gap `0.0150558130147454`
- `cand_0255`: benchmark `0.32164046189516404`, audit `0.3152093598308745`, gap `0.00643110206428954`
- `cand_0254`: benchmark `0.3687962834685289`, audit `0.3141337039756543`, gap `0.05466257949287456`
- `cand_0253`: benchmark `0.30600007176038846`, audit `0.2908975094695538`, gap `0.015102562290834676`
- `cand_0252`: benchmark `0.3606567678547835`, audit `0.3095993536613364`, gap `0.051057414193447115`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- tracked_mechanisms: `11`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (148 candidate(s), avg transfer gap 0.036271).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.036271. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 676.9 MB on average, leaving most VRAM unused. 7 scored candidate(s) have landed since structural commit `48bbe21`.`
- scored_candidates_since_change: `7`
- last_structural_commit: `48bbe21`
### Chosen Lever Values
- source_candidate: `cand_0256`
- model: `global_dim=256`

### Effective Backend Settings
- source_candidate: `cand_0256`
- model: `hidden_dim=128, global_dim=256, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `148`, audit_blocked `116`, avg_gap `0.03627111308180024`
- loss: `science_loss` (available); attempts `133`, audit_blocked `102`, avg_gap `0.03598607627467693`
- eval: `science_eval` (available); attempts `140`, audit_blocked `108`, avg_gap `0.035891501213978036`
- config: `science_config` (available); attempts `133`, audit_blocked `102`, avg_gap `0.03598607627467693`
- train: `science_train` (available); attempts `126`, audit_blocked `95`, avg_gap `0.03571087745983391`

### Recent Module Evidence
- `science_backend`: attempts `148`, audit_blocked `116`, avg_gap `0.03627111308180024`
- `science_model`: attempts `148`, audit_blocked `116`, avg_gap `0.03627111308180024`
- `science_eval`: attempts `140`, audit_blocked `108`, avg_gap `0.035891501213978036`
- `science_config`: attempts `133`, audit_blocked `102`, avg_gap `0.03598607627467693`

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
- summary: `The lab has stayed on `science_model` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
