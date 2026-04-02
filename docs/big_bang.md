# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T04:53:40+00:00`
- cycles_completed: `39`
- genesis seed: `cand_0001`
- last candidate: `cand_0337`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0337`
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
- `cand_0337`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30629321323502756`
- `cand_0336`: outcome `keeper`; diagnosis `complete`; benchmark `0.3404962969400935`
- `cand_0335`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3232360976110454`
- `cand_0334`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3818179047287495`
- `cand_0333`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3585172984597409`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.342072, audit averaged 0.311379, and the mean transfer gap was 0.030693.`
- recent benchmark avg: `0.34207216219493136`
- recent audit avg: `0.31137890639303184`
- recent transfer gap avg: `0.0306932558018995`
- `cand_0337`: benchmark `0.30629321323502756`, audit `0.27926578076077113`, gap `0.02702743247425643`
- `cand_0336`: benchmark `0.3404962969400935`, audit `0.34684687968070926`, gap `-0.006350582740615784`
- `cand_0335`: benchmark `0.3232360976110454`, audit `0.27833325484539406`, gap `0.04490284276565132`
- `cand_0334`: benchmark `0.3818179047287495`, audit `0.33493781377662935`, gap `0.046880090952120146`
- `cand_0333`: benchmark `0.3585172984597409`, audit `0.3175108029016555`, gap `0.04100649555808539`

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
- summary: `Recent backend evolution is concentrated in science_backend (229 candidate(s), avg transfer gap 0.037564).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 874.6 MB on average, leaving most VRAM unused. 38 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `38`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0337`
- train: `batch_size=3, eval_batch_size=3, grad_clip=0.85`

### Effective Backend Settings
- source_candidate: `cand_0337`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=0.85, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `229`, audit_blocked `141`, avg_gap `0.037563582955758935`
- loss: `science_loss` (targeted); attempts `214`, audit_blocked `127`, avg_gap `0.03747879433144644`
- eval: `science_eval` (available); attempts `221`, audit_blocked `133`, avg_gap `0.03737230062742257`
- config: `science_config` (available); attempts `214`, audit_blocked `127`, avg_gap `0.03747879433144644`
- train: `science_train` (available); attempts `207`, audit_blocked `120`, avg_gap `0.037365961327731276`

### Recent Module Evidence
- `science_backend`: attempts `229`, audit_blocked `141`, avg_gap `0.037563582955758935`
- `science_model`: attempts `229`, audit_blocked `141`, avg_gap `0.037563582955758935`
- `science_eval`: attempts `221`, audit_blocked `133`, avg_gap `0.03737230062742257`
- `science_config`: attempts `214`, audit_blocked `127`, avg_gap `0.03747879433144644`

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
- summary: `The lab has stayed on `science_train` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
