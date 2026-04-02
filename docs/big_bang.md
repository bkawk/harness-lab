# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T03:36:08+00:00`
- cycles_completed: `32`
- genesis seed: `cand_0001`
- last candidate: `cand_0330`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0330`
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
- `cand_0330`: outcome `dead_end`; diagnosis `complete`; benchmark `0.348135404293185`
- `cand_0329`: outcome `keeper`; diagnosis `complete`; benchmark `0.30550183895481997`
- `cand_0328`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3896409037905773`
- `cand_0327`: outcome `dead_end`; diagnosis `complete`; benchmark `0.5031005280065836`
- `cand_0326`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36317450514364247`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.381911, audit averaged 0.323520, and the mean transfer gap was 0.058391.`
- recent benchmark avg: `0.38191063603776165`
- recent audit avg: `0.3235199779509596`
- recent transfer gap avg: `0.05839065808680203`
- `cand_0330`: benchmark `0.348135404293185`, audit `0.3175619767458397`, gap `0.030573427547345322`
- `cand_0329`: benchmark `0.30550183895481997`, audit `0.3040924480694087`, gap `0.0014093908854112547`
- `cand_0328`: benchmark `0.3896409037905773`, audit `0.3249630918464863`, gap `0.064677811944091`
- `cand_0327`: benchmark `0.5031005280065836`, audit `0.3501051192766679`, gap `0.15299540872991568`
- `cand_0326`: benchmark `0.36317450514364247`, audit `0.3208772538163956`, gap `0.042297251327246876`

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
- summary: `Recent backend evolution is concentrated in science_backend (222 candidate(s), avg transfer gap 0.038104).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 719.5 MB on average, leaving most VRAM unused. 31 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `31`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0330`
- train: `batch_size=4, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0330`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `222`, audit_blocked `138`, avg_gap `0.03810383327627868`
- loss: `science_loss` (targeted); attempts `207`, audit_blocked `124`, avg_gap `0.0380571319968683`
- eval: `science_eval` (available); attempts `214`, audit_blocked `130`, avg_gap `0.03792833415569788`
- config: `science_config` (available); attempts `207`, audit_blocked `124`, avg_gap `0.0380571319968683`
- train: `science_train` (available); attempts `200`, audit_blocked `117`, avg_gap `0.03796281338310738`

### Recent Module Evidence
- `science_backend`: attempts `222`, audit_blocked `138`, avg_gap `0.03810383327627868`
- `science_model`: attempts `222`, audit_blocked `138`, avg_gap `0.03810383327627868`
- `science_eval`: attempts `214`, audit_blocked `130`, avg_gap `0.03792833415569788`
- `science_config`: attempts `207`, audit_blocked `124`, avg_gap `0.0380571319968683`

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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
