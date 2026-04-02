# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T04:20:45+00:00`
- cycles_completed: `36`
- genesis seed: `cand_0001`
- last candidate: `cand_0334`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0334`
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
- `cand_0334`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3818179047287495`
- `cand_0333`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3585172984597409`
- `cand_0332`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.41029974976391587`
- `cand_0331`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30686888118056277`
- `cand_0330`: outcome `dead_end`; diagnosis `complete`; benchmark `0.348135404293185`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.361128, audit averaged 0.336826, and the mean transfer gap was 0.024302.`
- recent benchmark avg: `0.3611278476852308`
- recent audit avg: `0.3368259471660352`
- recent transfer gap avg: `0.024301900519195573`
- `cand_0334`: benchmark `0.3818179047287495`, audit `0.33493781377662935`, gap `0.046880090952120146`
- `cand_0333`: benchmark `0.3585172984597409`, audit `0.3175108029016555`, gap `0.04100649555808539`
- `cand_0332`: benchmark `0.41029974976391587`, audit `0.35923581843548724`, gap `0.051063931328428624`
- `cand_0331`: benchmark `0.30686888118056277`, audit `0.3548833239705644`, gap `-0.04801444279000161`
- `cand_0330`: benchmark `0.348135404293185`, audit `0.3175619767458397`, gap `0.030573427547345322`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (226 candidate(s), avg transfer gap 0.037798).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 722.4 MB on average, leaving most VRAM unused. 35 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `35`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0334`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0334`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=8, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `226`, audit_blocked `140`, avg_gap `0.037797966320773785`
- loss: `science_loss` (available); attempts `211`, audit_blocked `126`, avg_gap `0.03772936486885311`
- eval: `science_eval` (available); attempts `218`, audit_blocked `132`, avg_gap `0.037613426064640056`
- config: `science_config` (available); attempts `211`, audit_blocked `126`, avg_gap `0.03772936486885311`
- train: `science_train` (targeted); attempts `204`, audit_blocked `119`, avg_gap `0.03762439572486406`

### Recent Module Evidence
- `science_backend`: attempts `226`, audit_blocked `140`, avg_gap `0.037797966320773785`
- `science_model`: attempts `226`, audit_blocked `140`, avg_gap `0.037797966320773785`
- `science_eval`: attempts `218`, audit_blocked `132`, avg_gap `0.037613426064640056`
- `science_config`: attempts `211`, audit_blocked `126`, avg_gap `0.03772936486885311`

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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
