# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T04:42:49+00:00`
- cycles_completed: `38`
- genesis seed: `cand_0001`
- last candidate: `cand_0336`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0336`
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
- `cand_0336`: outcome `keeper`; diagnosis `complete`; benchmark `0.3404962969400935`
- `cand_0335`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3232360976110454`
- `cand_0334`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3818179047287495`
- `cand_0333`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3585172984597409`
- `cand_0332`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.41029974976391587`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.362873, audit averaged 0.327373, and the mean transfer gap was 0.035501.`
- recent benchmark avg: `0.36287346950070903`
- recent audit avg: `0.3273729139279751`
- recent transfer gap avg: `0.03550055557273394`
- `cand_0336`: benchmark `0.3404962969400935`, audit `0.34684687968070926`, gap `-0.006350582740615784`
- `cand_0335`: benchmark `0.3232360976110454`, audit `0.27833325484539406`, gap `0.04490284276565132`
- `cand_0334`: benchmark `0.3818179047287495`, audit `0.33493781377662935`, gap `0.046880090952120146`
- `cand_0333`: benchmark `0.3585172984597409`, audit `0.3175108029016555`, gap `0.04100649555808539`
- `cand_0332`: benchmark `0.41029974976391587`, audit `0.35923581843548724`, gap `0.051063931328428624`

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
- summary: `Recent backend evolution is concentrated in science_backend (228 candidate(s), avg transfer gap 0.037615).`
- recommended_action: `targeted_mutation`
- target_module: `science_train`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `The top live pressure is unused VRAM headroom, so favor explicit train-capacity moves first. Start with batch_size and eval_batch_size before drifting back to loss tuning. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 832.4 MB on average, leaving most VRAM unused. 37 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `37`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0336`
- train: `batch_size=4, eval_batch_size=4`

### Effective Backend Settings
- source_candidate: `cand_0336`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=4, eval_batch_size=4, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `228`, audit_blocked `140`, avg_gap `0.037615485174879636`
- loss: `science_loss` (available); attempts `213`, audit_blocked `126`, avg_gap `0.03753409254233104`
- eval: `science_eval` (available); attempts `220`, audit_blocked `132`, avg_gap `0.03742535123333624`
- config: `science_config` (available); attempts `213`, audit_blocked `126`, avg_gap `0.03753409254233104`
- train: `science_train` (targeted); attempts `206`, audit_blocked `119`, avg_gap `0.0374227664313218`

### Recent Module Evidence
- `science_backend`: attempts `228`, audit_blocked `140`, avg_gap `0.037615485174879636`
- `science_model`: attempts `228`, audit_blocked `140`, avg_gap `0.037615485174879636`
- `science_eval`: attempts `220`, audit_blocked `132`, avg_gap `0.03742535123333624`
- `science_config`: attempts `213`, audit_blocked `126`, avg_gap `0.03753409254233104`

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
