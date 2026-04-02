# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T02:51:21+00:00`
- cycles_completed: `28`
- genesis seed: `cand_0001`
- last candidate: `cand_0326`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `5`

## Latest Step
- candidate: `cand_0326`
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
- `cand_0326`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36317450514364247`
- `cand_0325`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3425602141987957`
- `cand_0324`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3737575430679745`
- `cand_0323`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2976612921570371`
- `cand_0322`: outcome `keeper`; diagnosis `complete`; benchmark `0.3133963693141253`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.338110, audit averaged 0.318978, and the mean transfer gap was 0.019132.`
- recent benchmark avg: `0.33810998477631504`
- recent audit avg: `0.3189779251312449`
- recent transfer gap avg: `0.019132059645070122`
- `cand_0326`: benchmark `0.36317450514364247`, audit `0.3208772538163956`, gap `0.042297251327246876`
- `cand_0325`: benchmark `0.3425602141987957`, audit `0.3299355360887518`, gap `0.012624678110043863`
- `cand_0324`: benchmark `0.3737575430679745`, audit `0.33931162210034604`, gap `0.03444592096762844`
- `cand_0323`: benchmark `0.2976612921570371`, audit `0.2776505563450572`, gap `0.02001073581197993`
- `cand_0322`: benchmark `0.3133963693141253`, audit `0.3271146573056738`, gap `-0.013718287991548506`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (218 candidate(s), avg transfer gap 0.037600).`
- recommended_action: `targeted_mutation`
- target_module: `science_eval`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are dominated by smoke-gate transfer checks, so the evaluation module is the best next bounded target. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 756.5 MB on average, leaving most VRAM unused. 27 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `27`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0326`
- model: `global_dim=256, hidden_dim=160`

### Effective Backend Settings
- source_candidate: `cand_0326`
- model: `hidden_dim=160, global_dim=256, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `218`, audit_blocked `138`, avg_gap `0.03759999542134786`
- loss: `science_loss` (available); attempts `203`, audit_blocked `124`, avg_gap `0.037512844225252154`
- eval: `science_eval` (targeted); attempts `210`, audit_blocked `130`, avg_gap `0.037398914142271006`
- config: `science_config` (available); attempts `203`, audit_blocked `124`, avg_gap `0.037512844225252154`
- train: `science_train` (available); attempts `196`, audit_blocked `117`, avg_gap `0.037394180908838`

### Recent Module Evidence
- `science_backend`: attempts `218`, audit_blocked `138`, avg_gap `0.03759999542134786`
- `science_model`: attempts `218`, audit_blocked `138`, avg_gap `0.03759999542134786`
- `science_eval`: attempts `210`, audit_blocked `130`, avg_gap `0.037398914142271006`
- `science_config`: attempts `203`, audit_blocked `124`, avg_gap `0.037512844225252154`

## External Review
- status: `idle`
- trigger_reason: `-`
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
