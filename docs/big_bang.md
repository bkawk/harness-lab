# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T17:50:34+00:00`
- last_heartbeat: `2026-04-01T18:11:46+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0277`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0277`
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
- `cand_0277`: outcome `dead_end`; diagnosis `complete`; benchmark `0.36251520353125916`
- `cand_0276`: outcome `dead_end`; diagnosis `complete`; benchmark `0.32872138855302646`
- `cand_0275`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0274`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3960477918974155`
- `cand_0273`: outcome `-`; diagnosis `empty`; benchmark `None`

## Science Leaders
- best benchmark: `cand_0265` -> `0.450557453846711`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.362428, audit averaged 0.306588, and the mean transfer gap was 0.055840.`
- recent benchmark avg: `0.36242812799390034`
- recent audit avg: `0.3065881631925903`
- recent transfer gap avg: `0.05583996480131007`
- `cand_0277`: benchmark `0.36251520353125916`, audit `0.3068873039989968`, gap `0.05562789953226238`
- `cand_0276`: benchmark `0.32872138855302646`, audit `0.31617162449503344`, gap `0.012549764057993018`
- `cand_0274`: benchmark `0.3960477918974155`, audit `0.2967055610837407`, gap `0.09934223081367483`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 4 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (169 candidate(s), avg transfer gap 0.036016).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 2 scored candidate(s) have landed since structural commit `a225c8b`.`
- secondary_context: `Recent real-backend runs are only using about 599.1 MB on average, leaving most VRAM unused. 2 scored candidate(s) have landed since structural commit `a225c8b`.`
- scored_candidates_since_change: `2`
- last_structural_commit: `a225c8b`
### Chosen Lever Values
- source_candidate: `cand_0277`
- loss: `instance_loss_weight=0.06, instance_margin=0.33`

### Effective Backend Settings
- source_candidate: `cand_0277`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.06, instance_margin=0.33`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `169`, audit_blocked `125`, avg_gap `0.036015883009385644`
- loss: `science_loss` (targeted); attempts `154`, audit_blocked `111`, avg_gap `0.035733960338724446`
- eval: `science_eval` (available); attempts `161`, audit_blocked `117`, avg_gap `0.03565964775277911`
- config: `science_config` (available); attempts `154`, audit_blocked `111`, avg_gap `0.035733960338724446`
- train: `science_train` (available); attempts `147`, audit_blocked `104`, avg_gap `0.035475202247158076`

### Recent Module Evidence
- `science_backend`: attempts `169`, audit_blocked `125`, avg_gap `0.036015883009385644`
- `science_model`: attempts `169`, audit_blocked `125`, avg_gap `0.036015883009385644`
- `science_eval`: attempts `161`, audit_blocked `117`, avg_gap `0.03565964775277911`
- `science_config`: attempts `154`, audit_blocked `111`, avg_gap `0.035733960338724446`

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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
