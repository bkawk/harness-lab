# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T01:00:02+00:00`
- cycles_completed: `18`
- genesis seed: `cand_0001`
- last candidate: `cand_0316`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0316`
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
- `cand_0316`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3520256106046247`
- `cand_0315`: outcome `keeper`; diagnosis `complete`; benchmark `0.33687599408519886`
- `cand_0314`: outcome `dead_end`; diagnosis `complete`; benchmark `0.4331858482994261`
- `cand_0313`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3120048648349257`
- `cand_0312`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3353497352026351`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.353888, audit averaged 0.324332, and the mean transfer gap was 0.029557.`
- recent benchmark avg: `0.3538884106053621`
- recent audit avg: `0.32433150744961986`
- recent transfer gap avg: `0.02955690315574223`
- `cand_0316`: benchmark `0.3520256106046247`, audit `0.2913268292645592`, gap `0.060698781340065455`
- `cand_0315`: benchmark `0.33687599408519886`, audit `0.3156684159182012`, gap `0.021207578166997643`
- `cand_0314`: benchmark `0.4331858482994261`, audit `0.3436628826044774`, gap `0.08952296569494866`
- `cand_0313`: benchmark `0.3120048648349257`, audit `0.30478926710799153`, gap `0.007215597726934142`
- `cand_0312`: benchmark `0.3353497352026351`, audit `0.36621014235286986`, gap `-0.030860407150234748`

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
- summary: `Recent backend evolution is concentrated in science_backend (208 candidate(s), avg transfer gap 0.037335).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 718.8 MB on average, leaving most VRAM unused. 17 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `17`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0316`
- train: `batch_size=3, eval_batch_size=4`

### Effective Backend Settings
- source_candidate: `cand_0316`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=4, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `208`, audit_blocked `134`, avg_gap `0.037334738573812816`
- loss: `science_loss` (available); attempts `193`, audit_blocked `120`, avg_gap `0.03722045656217601`
- eval: `science_eval` (available); attempts `200`, audit_blocked `126`, avg_gap `0.037110040908615693`
- config: `science_config` (available); attempts `193`, audit_blocked `120`, avg_gap `0.03722045656217601`
- train: `science_train` (targeted); attempts `186`, audit_blocked `113`, avg_gap `0.03708183431486263`

### Recent Module Evidence
- `science_backend`: attempts `208`, audit_blocked `134`, avg_gap `0.037334738573812816`
- `science_model`: attempts `208`, audit_blocked `134`, avg_gap `0.037334738573812816`
- `science_eval`: attempts `200`, audit_blocked `126`, avg_gap `0.037110040908615693`
- `science_config`: attempts `193`, audit_blocked `120`, avg_gap `0.03722045656217601`

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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
