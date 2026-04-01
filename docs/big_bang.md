# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-01T22:00:40+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0300`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `1`

## Latest Step
- candidate: `cand_0300`
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
- `cand_0300`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29574560126772687`
- `cand_0299`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3128551711335869`
- `cand_0298`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0297`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3374706938391191`
- `cand_0296`: outcome `dead_end`; diagnosis `complete`; benchmark `0.37303324659835074`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.329776, audit averaged 0.310411, and the mean transfer gap was 0.019365.`
- recent benchmark avg: `0.3297761782096959`
- recent audit avg: `0.3104110878006557`
- recent transfer gap avg: `0.019365090409040206`
- `cand_0300`: benchmark `0.29574560126772687`, audit `0.23282680776107983`, gap `0.06291879350664703`
- `cand_0299`: benchmark `0.3128551711335869`, audit `0.3350051268934826`, gap `-0.0221499557598957`
- `cand_0297`: benchmark `0.3374706938391191`, audit `0.30456284436687675`, gap `0.032907849472242345`
- `cand_0296`: benchmark `0.37303324659835074`, audit `0.3692495721811836`, gap `0.003783674417167149`

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
- summary: `Recent backend evolution is concentrated in science_backend (192 candidate(s), avg transfer gap 0.036313).`
- recommended_action: `wait`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 1 scored candidate(s) have landed since structural commit `49fb173`.`
- secondary_context: `Recent real-backend runs are only using about 710.2 MB on average, leaving most VRAM unused. 1 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `1`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0300`
- train: `batch_size=3, eval_batch_size=3`

### Effective Backend Settings
- source_candidate: `cand_0300`
- model: `hidden_dim=128, global_dim=128, instance_dim=16, k_neighbors=6, instance_modulation_scale=0.1`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.05, instance_loss_weight=0.04, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=3, eval_batch_size=3, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `192`, audit_blocked `130`, avg_gap `0.03631342274521483`
- loss: `science_loss` (targeted); attempts `177`, audit_blocked `116`, avg_gap `0.036093735937587426`
- eval: `science_eval` (available); attempts `184`, audit_blocked `122`, avg_gap `0.03601472703428225`
- config: `science_config` (available); attempts `177`, audit_blocked `116`, avg_gap `0.036093735937587426`
- train: `science_train` (available); attempts `170`, audit_blocked `109`, avg_gap `0.035885901359252584`

### Recent Module Evidence
- `science_backend`: attempts `192`, audit_blocked `130`, avg_gap `0.03631342274521483`
- `science_model`: attempts `192`, audit_blocked `130`, avg_gap `0.03631342274521483`
- `science_eval`: attempts `184`, audit_blocked `122`, avg_gap `0.03601472703428225`
- `science_config`: attempts `177`, audit_blocked `116`, avg_gap `0.036093735937587426`

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
- summary: `Recent branching still has room, but `science_train` is the current active line.`
- current_mechanism_streak: `2`
- novelty_step_recommended: `False`
