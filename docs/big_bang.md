# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T05:49:10+00:00`
- cycles_completed: `44`
- genesis seed: `cand_0001`
- last candidate: `cand_0342`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0342`
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
- `cand_0342`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3528256253964448`
- `cand_0341`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4371920677268424`
- `cand_0340`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36952832702851973`
- `cand_0339`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.308285079735548`
- `cand_0338`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3611726846734127`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.365801, audit averaged 0.301498, and the mean transfer gap was 0.064303.`
- recent benchmark avg: `0.3658007569121535`
- recent audit avg: `0.30149782404546405`
- recent transfer gap avg: `0.06430293286668946`
- `cand_0342`: benchmark `0.3528256253964448`, audit `0.3245052110688219`, gap `0.02832041432762289`
- `cand_0341`: benchmark `0.4371920677268424`, audit `0.33252857891992843`, gap `0.10466348880691395`
- `cand_0340`: benchmark `0.36952832702851973`, audit `0.3409990904445357`, gap `0.02852923658398404`
- `cand_0339`: benchmark `0.308285079735548`, audit `0.26521584236735496`, gap `0.043069237368193014`
- `cand_0338`: benchmark `0.3611726846734127`, audit `0.24424039742667927`, gap `0.11693228724673341`

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
- summary: `Recent backend evolution is concentrated in science_backend (234 candidate(s), avg transfer gap 0.038203).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 834.8 MB on average, leaving most VRAM unused. 43 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `43`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0342`
- loss: `instance_loss_weight=0.06, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0342`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `234`, audit_blocked `143`, avg_gap `0.038203280322049143`
- loss: `science_loss` (targeted); attempts `219`, audit_blocked `129`, avg_gap `0.03816659275542703`
- eval: `science_eval` (available); attempts `226`, audit_blocked `135`, avg_gap `0.03804221685227995`
- config: `science_config` (available); attempts `219`, audit_blocked `129`, avg_gap `0.03816659275542703`
- train: `science_train` (available); attempts `212`, audit_blocked `122`, avg_gap `0.038082370145256755`

### Recent Module Evidence
- `science_backend`: attempts `234`, audit_blocked `143`, avg_gap `0.038203280322049143`
- `science_model`: attempts `234`, audit_blocked `143`, avg_gap `0.038203280322049143`
- `science_eval`: attempts `226`, audit_blocked `135`, avg_gap `0.03804221685227995`
- `science_config`: attempts `219`, audit_blocked `129`, avg_gap `0.03816659275542703`

## External Review
- status: `cooldown`
- trigger_reason: `dead_end_streak`
- reviewer: `heuristic`
- summary: `After 340 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `transfer_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
