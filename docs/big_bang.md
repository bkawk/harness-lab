# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T19:43:12+00:00`
- last_heartbeat: `2026-04-01T20:16:42+00:00`
- cycles_completed: `3`
- genesis seed: `cand_0001`
- last candidate: `cand_0290`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0290`
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
- `cand_0290`: outcome `dead_end`; diagnosis `complete`; benchmark `0.41502353790129975`
- `cand_0289`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3195024282628329`
- `cand_0288`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29751565834820354`
- `cand_0287`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30164153260394605`
- `cand_0286`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.333421, audit averaged 0.301830, and the mean transfer gap was 0.031591.`
- recent benchmark avg: `0.3334207892790706`
- recent audit avg: `0.3018298044356894`
- recent transfer gap avg: `0.03159098484338115`
- `cand_0290`: benchmark `0.41502353790129975`, audit `0.34066080928357856`, gap `0.0743627286177212`
- `cand_0289`: benchmark `0.3195024282628329`, audit `0.34546743047364925`, gap `-0.025965002210816324`
- `cand_0288`: benchmark `0.29751565834820354`, audit `0.286603647057389`, gap `0.010912011290814538`
- `cand_0287`: benchmark `0.30164153260394605`, audit `0.23458733092814085`, gap `0.0670542016758052`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 6 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

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
- summary: `Recent backend evolution is concentrated in science_backend (182 candidate(s), avg transfer gap 0.036106).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 639.5 MB on average, leaving most VRAM unused. 4 scored candidate(s) have landed since structural commit `0ab69b5`.`
- scored_candidates_since_change: `4`
- last_structural_commit: `0ab69b5`
### Chosen Lever Values
- source_candidate: `cand_0290`
- loss: `instance_margin=0.4, param_loss_weight=0.24`

### Effective Backend Settings
- source_candidate: `cand_0290`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.24, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.4`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `182`, audit_blocked `127`, avg_gap `0.0361063130844371`
- loss: `science_loss` (targeted); attempts `167`, audit_blocked `113`, avg_gap `0.03585276018986848`
- eval: `science_eval` (available); attempts `174`, audit_blocked `119`, avg_gap `0.03577864978227374`
- config: `science_config` (available); attempts `167`, audit_blocked `113`, avg_gap `0.03585276018986848`
- train: `science_train` (available); attempts `160`, audit_blocked `106`, avg_gap `0.03561895961562818`

### Recent Module Evidence
- `science_backend`: attempts `182`, audit_blocked `127`, avg_gap `0.0361063130844371`
- `science_model`: attempts `182`, audit_blocked `127`, avg_gap `0.0361063130844371`
- `science_eval`: attempts `174`, audit_blocked `119`, avg_gap `0.03577864978227374`
- `science_config`: attempts `167`, audit_blocked `113`, avg_gap `0.03585276018986848`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 1 ranked requests for human help.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
