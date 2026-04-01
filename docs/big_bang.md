# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T16:31:30+00:00`
- last_heartbeat: `2026-04-01T16:41:49+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0266`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0266`
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
- `cand_0266`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3659021804282816`
- `cand_0265`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.450557453846711`
- `cand_0264`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3265916891220915`
- `cand_0263`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0262`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0265` -> `0.450557453846711`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.381017, audit averaged 0.325995, and the mean transfer gap was 0.055022.`
- recent benchmark avg: `0.38101710779902803`
- recent audit avg: `0.32599468775028684`
- recent transfer gap avg: `0.05502242004874117`
- `cand_0266`: benchmark `0.3659021804282816`, audit `0.33883619788137753`, gap `0.027065982546904066`
- `cand_0265`: benchmark `0.450557453846711`, audit `0.3505268118616605`, gap `0.10003064198505046`
- `cand_0264`: benchmark `0.3265916891220915`, audit `0.2886210535078225`, gap `0.037970635614269`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- tracked_mechanisms: `12`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (158 candidate(s), avg transfer gap 0.036043).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 2 scored candidate(s) have landed since structural commit `e1cb6e3`.`
- secondary_context: `Recent real-backend runs are only using about 642.4 MB on average, leaving most VRAM unused. 2 scored candidate(s) have landed since structural commit `e1cb6e3`.`
- scored_candidates_since_change: `2`
- last_structural_commit: `e1cb6e3`
### Chosen Lever Values
- source_candidate: `cand_0266`
- loss: `instance_margin=0.4`

### Effective Backend Settings
- source_candidate: `cand_0266`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.4`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `158`, audit_blocked `122`, avg_gap `0.03604269343387561`
- loss: `science_loss` (targeted); attempts `143`, audit_blocked `108`, avg_gap `0.035748187198239856`
- eval: `science_eval` (available); attempts `150`, audit_blocked `114`, avg_gap `0.03566932161034933`
- config: `science_config` (available); attempts `143`, audit_blocked `108`, avg_gap `0.035748187198239856`
- train: `science_train` (available); attempts `136`, audit_blocked `101`, avg_gap `0.03547516478480384`

### Recent Module Evidence
- `science_backend`: attempts `158`, audit_blocked `122`, avg_gap `0.03604269343387561`
- `science_model`: attempts `158`, audit_blocked `122`, avg_gap `0.03604269343387561`
- `science_eval`: attempts `150`, audit_blocked `114`, avg_gap `0.03566932161034933`
- `science_config`: attempts `143`, audit_blocked `108`, avg_gap `0.035748187198239856`

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
- summary: `The humans recently addressed 2 lab request(s).`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
