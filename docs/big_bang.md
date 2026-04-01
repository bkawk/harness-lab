# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-01T22:45:57+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0304`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0304`
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
- `cand_0304`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37033046079396026`
- `cand_0303`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3405501245086008`
- `cand_0302`: outcome `dead_end`; diagnosis `complete`; benchmark `0.41320331208073857`
- `cand_0301`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34707212997570036`
- `cand_0300`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29574560126772687`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.353380, audit averaged 0.287068, and the mean transfer gap was 0.066312.`
- recent benchmark avg: `0.3533803257253454`
- recent audit avg: `0.28706815458154245`
- recent transfer gap avg: `0.06631217114380293`
- `cand_0304`: benchmark `0.37033046079396026`, audit `0.30993773677756464`, gap `0.060392724016395616`
- `cand_0303`: benchmark `0.3405501245086008`, audit `0.2907379130458192`, gap `0.049812211462781586`
- `cand_0302`: benchmark `0.41320331208073857`, audit `0.31541424042073174`, gap `0.09778907166000683`
- `cand_0301`: benchmark `0.34707212997570036`, audit `0.28642407490251676`, gap `0.060648055073183604`
- `cand_0300`: benchmark `0.29574560126772687`, audit `0.23282680776107983`, gap `0.06291879350664703`

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
- summary: `Recent backend evolution is concentrated in science_backend (196 candidate(s), avg transfer gap 0.037035).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 721.6 MB on average, leaving most VRAM unused. 5 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `5`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0304`
- model: `hidden_dim=160, k_neighbors=10`

### Effective Backend Settings
- source_candidate: `cand_0304`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=10, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `196`, audit_blocked `131`, avg_gap `0.037034992167621315`
- loss: `science_loss` (available); attempts `181`, audit_blocked `117`, avg_gap `0.03688524624626271`
- eval: `science_eval` (available); attempts `188`, audit_blocked `123`, avg_gap `0.03677904086296469`
- config: `science_config` (available); attempts `181`, audit_blocked `117`, avg_gap `0.03688524624626271`
- train: `science_train` (targeted); attempts `174`, audit_blocked `110`, avg_gap `0.0367198910710883`

### Recent Module Evidence
- `science_backend`: attempts `196`, audit_blocked `131`, avg_gap `0.037034992167621315`
- `science_model`: attempts `196`, audit_blocked `131`, avg_gap `0.037034992167621315`
- `science_eval`: attempts `188`, audit_blocked `123`, avg_gap `0.03677904086296469`
- `science_config`: attempts `181`, audit_blocked `117`, avg_gap `0.03688524624626271`

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
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
