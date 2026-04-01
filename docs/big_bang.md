# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T19:43:12+00:00`
- last_heartbeat: `2026-04-01T21:35:26+00:00`
- cycles_completed: `10`
- genesis seed: `cand_0001`
- last candidate: `cand_0297`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0297`
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
- `cand_0297`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3374706938391191`
- `cand_0296`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37303324659835074`
- `cand_0295`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29720201562223736`
- `cand_0294`: outcome `dead_end`; diagnosis `complete`; benchmark `0.33998006136930964`
- `cand_0293`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34996466017366057`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.339530, audit averaged 0.304388, and the mean transfer gap was 0.035142.`
- recent benchmark avg: `0.33953013552053546`
- recent audit avg: `0.30438801595777604`
- recent transfer gap avg: `0.035142119562759436`
- `cand_0297`: benchmark `0.3374706938391191`, audit `0.30456284436687675`, gap `0.032907849472242345`
- `cand_0296`: benchmark `0.37303324659835074`, audit `0.3692495721811836`, gap `0.003783674417167149`
- `cand_0295`: benchmark `0.29720201562223736`, audit `0.26414141766380617`, gap `0.03306059795843119`
- `cand_0294`: benchmark `0.33998006136930964`, audit `0.31066645313231545`, gap `0.029313608236994193`
- `cand_0293`: benchmark `0.34996466017366057`, audit `0.2733197924446983`, gap `0.07664486772896228`

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
- summary: `Recent backend evolution is concentrated in science_backend (189 candidate(s), avg transfer gap 0.036507).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 645.8 MB on average, leaving most VRAM unused. 11 scored candidate(s) have landed since structural commit `0ab69b5`.`
- scored_candidates_since_change: `11`
- last_structural_commit: `0ab69b5`
### Chosen Lever Values
- source_candidate: `cand_0297`
- loss: `instance_loss_weight=0.07, param_loss_weight=0.18`

### Effective Backend Settings
- source_candidate: `cand_0297`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.18, boundary_loss_weight=0.12, instance_loss_weight=0.07, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `189`, audit_blocked `129`, avg_gap `0.036506501580025004`
- loss: `science_loss` (targeted); attempts `174`, audit_blocked `115`, avg_gap `0.03630180636227898`
- eval: `science_eval` (available); attempts `181`, audit_blocked `121`, avg_gap `0.036213839240153665`
- config: `science_config` (available); attempts `174`, audit_blocked `115`, avg_gap `0.03630180636227898`
- train: `science_train` (available); attempts `167`, audit_blocked `108`, avg_gap `0.03610119972711198`

### Recent Module Evidence
- `science_backend`: attempts `189`, audit_blocked `129`, avg_gap `0.036506501580025004`
- `science_model`: attempts `189`, audit_blocked `129`, avg_gap `0.036506501580025004`
- `science_eval`: attempts `181`, audit_blocked `121`, avg_gap `0.036213839240153665`
- `science_config`: attempts `174`, audit_blocked `115`, avg_gap `0.03630180636227898`

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
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
