# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T02:29:07+00:00`
- cycles_completed: `26`
- genesis seed: `cand_0001`
- last candidate: `cand_0324`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0324`
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
- `cand_0324`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3737575430679745`
- `cand_0323`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2976612921570371`
- `cand_0322`: outcome `keeper`; diagnosis `complete`; benchmark `0.3133963693141253`
- `cand_0321`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39580450134444234`
- `cand_0320`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3180179147188944`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.339728, audit averaged 0.314794, and the mean transfer gap was 0.024934.`
- recent benchmark avg: `0.33972752412049473`
- recent audit avg: `0.3147938248018053`
- recent transfer gap avg: `0.024933699318689474`
- `cand_0324`: benchmark `0.3737575430679745`, audit `0.33931162210034604`, gap `0.03444592096762844`
- `cand_0323`: benchmark `0.2976612921570371`, audit `0.2776505563450572`, gap `0.02001073581197993`
- `cand_0322`: benchmark `0.3133963693141253`, audit `0.3271146573056738`, gap `-0.013718287991548506`
- `cand_0321`: benchmark `0.39580450134444234`, audit `0.31604816980178535`, gap `0.07975633154265699`
- `cand_0320`: benchmark `0.3180179147188944`, audit `0.3138441184561639`, gap `0.004173796262730511`

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
- summary: `Mechanisms initial_harness, science_model, science_loss exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (216 candidate(s), avg transfer gap 0.037706).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 798.2 MB on average, leaving most VRAM unused. 25 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `25`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0324`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0324`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `216`, audit_blocked `137`, avg_gap `0.037706163282109136`
- loss: `science_loss` (available); attempts `201`, audit_blocked `123`, avg_gap `0.037626424784648844`
- eval: `science_eval` (targeted); attempts `208`, audit_blocked `129`, avg_gap `0.03750752561138167`
- config: `science_config` (available); attempts `201`, audit_blocked `123`, avg_gap `0.037626424784648844`
- train: `science_train` (available); attempts `194`, audit_blocked `116`, avg_gap `0.03751104227578144`

### Recent Module Evidence
- `science_backend`: attempts `216`, audit_blocked `137`, avg_gap `0.037706163282109136`
- `science_model`: attempts `216`, audit_blocked `137`, avg_gap `0.037706163282109136`
- `science_eval`: attempts `208`, audit_blocked `129`, avg_gap `0.03750752561138167`
- `science_config`: attempts `201`, audit_blocked `123`, avg_gap `0.037626424784648844`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
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
