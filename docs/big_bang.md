# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-01T23:30:12+00:00`
- cycles_completed: `10`
- genesis seed: `cand_0001`
- last candidate: `cand_0308`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0308`
- dataset: `abc_boundary512` via `reused_prepared_dataset`
- seed action: `existing`
- proposal status: `candidate`
- outcome status: `complete`
- diagnosis status: `complete`
- next top parent: `cand_0087`
- published: `False`
- commit: `-`
- cycle mode: `novelty_cycle`

## Active Backend
- active_candidate: `-`
- backend_status: `-`
- backend_pid: `-`
- backend_started_at: `-`
- backend_last_poll_at: `-`
- backend_poll_interval_seconds: `-`

## Recent Candidates
- `cand_0308`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39786773820750965`
- `cand_0307`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3235196550416018`
- `cand_0306`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3737575430679745`
- `cand_0305`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3508775996186074`
- `cand_0304`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37033046079396026`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.363271, audit averaged 0.318944, and the mean transfer gap was 0.044326.`
- recent benchmark avg: `0.36327059934593076`
- recent audit avg: `0.3189442314613024`
- recent transfer gap avg: `0.04432636788462828`
- `cand_0308`: benchmark `0.39786773820750965`, audit `0.30055282234037983`, gap `0.09731491586712981`
- `cand_0307`: benchmark `0.3235196550416018`, audit `0.3058384246273219`, gap `0.01768123041427988`
- `cand_0306`: benchmark `0.3737575430679745`, audit `0.33931162210034604`, gap `0.03444592096762844`
- `cand_0305`: benchmark `0.3508775996186074`, audit `0.33908055146089977`, gap `0.011797048157707657`
- `cand_0304`: benchmark `0.37033046079396026`, audit `0.30993773677756464`, gap `0.060392724016395616`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (200 candidate(s), avg transfer gap 0.037110).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 768.9 MB on average, leaving most VRAM unused. 9 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `9`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0308`
- model: `global_dim=256, hidden_dim=160`

### Effective Backend Settings
- source_candidate: `cand_0308`
- model: `hidden_dim=160, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `200`, audit_blocked `133`, avg_gap `0.03710984443468566`
- loss: `science_loss` (targeted); attempts `185`, audit_blocked `119`, avg_gap `0.03697032780167696`
- eval: `science_eval` (available); attempts `192`, audit_blocked `125`, avg_gap `0.03686360943754485`
- config: `science_config` (available); attempts `185`, audit_blocked `119`, avg_gap `0.03697032780167696`
- train: `science_train` (available); attempts `178`, audit_blocked `112`, avg_gap `0.03681313490954539`

### Recent Module Evidence
- `science_backend`: attempts `200`, audit_blocked `133`, avg_gap `0.03710984443468566`
- `science_model`: attempts `200`, audit_blocked `133`, avg_gap `0.03710984443468566`
- `science_eval`: attempts `192`, audit_blocked `125`, avg_gap `0.03686360943754485`
- `science_config`: attempts `185`, audit_blocked `119`, avg_gap `0.03697032780167696`

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
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
