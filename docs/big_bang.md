# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T15:14:04+00:00`
- last_heartbeat: `2026-04-01T15:35:13+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0259`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0259`
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
- `cand_0259`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3374651513876822`
- `cand_0258`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32573156546973003`
- `cand_0257`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0256`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2829415365286318`
- `cand_0255`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32164046189516404`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.316945, audit averaged 0.306320, and the mean transfer gap was 0.010625.`
- recent benchmark avg: `0.31694467882030203`
- recent audit avg: `0.306319789903977`
- recent transfer gap avg: `0.010624888916325001`
- `cand_0259`: benchmark `0.3374651513876822`, audit `0.30963691763721723`, gap `0.027828233750464948`
- `cand_0258`: benchmark `0.32573156546973003`, audit `0.3325471586339299`, gap `-0.006815593164199885`
- `cand_0256`: benchmark `0.2829415365286318`, audit `0.2678857235138864`, gap `0.0150558130147454`
- `cand_0255`: benchmark `0.32164046189516404`, audit `0.3152093598308745`, gap `0.00643110206428954`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (151 candidate(s), avg transfer gap 0.035892).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.035892. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 2 scored candidate(s) have landed since structural commit `23dc0ec`.`
- secondary_context: `Recent real-backend runs are only using about 681.4 MB on average, leaving most VRAM unused. 2 scored candidate(s) have landed since structural commit `23dc0ec`.`
- scored_candidates_since_change: `2`
- last_structural_commit: `23dc0ec`
### Chosen Lever Values
- source_candidate: `cand_0259`
- model: `k_neighbors=10`

### Effective Backend Settings
- source_candidate: `cand_0259`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=10, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `151`, audit_blocked `117`, avg_gap `0.03589221907020218`
- loss: `science_loss` (available); attempts `136`, audit_blocked `103`, avg_gap `0.0355683753569467`
- eval: `science_eval` (available); attempts `143`, audit_blocked `109`, avg_gap `0.03549485776208982`
- config: `science_config` (available); attempts `136`, audit_blocked `103`, avg_gap `0.0355683753569467`
- train: `science_train` (available); attempts `129`, audit_blocked `96`, avg_gap `0.03527253733519562`

### Recent Module Evidence
- `science_backend`: attempts `151`, audit_blocked `117`, avg_gap `0.03589221907020218`
- `science_model`: attempts `151`, audit_blocked `117`, avg_gap `0.03589221907020218`
- `science_eval`: attempts `143`, audit_blocked `109`, avg_gap `0.03549485776208982`
- `science_config`: attempts `136`, audit_blocked `103`, avg_gap `0.0355683753569467`

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
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
