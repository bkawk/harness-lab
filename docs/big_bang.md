# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T09:16:42+00:00`
- last_heartbeat: `2026-04-01T09:58:32+00:00`
- cycles_completed: `4`
- genesis seed: `cand_0001`
- last candidate: `cand_0225`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `4`

## Latest Step
- candidate: `cand_0225`
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
- `cand_0225`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36804312468236894`
- `cand_0224`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3378123307088491`
- `cand_0223`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3306176623249132`
- `cand_0222`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3234491172910994`
- `cand_0221`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.339981, audit averaged 0.296864, and the mean transfer gap was 0.043116.`
- recent benchmark avg: `0.33998055875180766`
- recent audit avg: `0.29686447817280864`
- recent transfer gap avg: `0.043116080578999016`
- `cand_0225`: benchmark `0.36804312468236894`, audit `0.2784978771929737`, gap `0.08954524748939524`
- `cand_0224`: benchmark `0.3378123307088491`, audit `0.33634708448675976`, gap `0.0014652462220893225`
- `cand_0223`: benchmark `0.3306176623249132`, audit `0.287004544693982`, gap `0.043613117630931175`
- `cand_0222`: benchmark `0.3234491172910994`, audit `0.28560840631751905`, gap `0.03784071097358033`

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
- summary: `Recent backend evolution is concentrated in science_backend (117 candidate(s), avg transfer gap 0.038648).`
- recommended_action: `targeted_mutation`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038648. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 589.9 MB on average, leaving most VRAM unused. 3 scored candidate(s) have landed since structural commit `2be55f0`.`
- scored_candidates_since_change: `3`
- last_structural_commit: `2be55f0`
### Chosen Lever Values
- source_candidate: `cand_0225`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0225`
- model: `hidden_dim=96, global_dim=192, instance_dim=12, k_neighbors=8, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `117`, audit_blocked `95`, avg_gap `0.038647641262125325`
- loss: `science_loss` (available); attempts `102`, audit_blocked `81`, avg_gap `0.03863749971505744`
- eval: `science_eval` (available); attempts `109`, audit_blocked `87`, avg_gap `0.03835357116107434`
- config: `science_config` (available); attempts `102`, audit_blocked `81`, avg_gap `0.03863749971505744`
- train: `science_train` (available); attempts `95`, audit_blocked `74`, avg_gap `0.038489999691591587`

### Recent Module Evidence
- `science_backend`: attempts `117`, audit_blocked `95`, avg_gap `0.038647641262125325`
- `science_model`: attempts `117`, audit_blocked `95`, avg_gap `0.038647641262125325`
- `science_eval`: attempts `109`, audit_blocked `87`, avg_gap `0.03835357116107434`
- `science_config`: attempts `102`, audit_blocked `81`, avg_gap `0.03863749971505744`

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
