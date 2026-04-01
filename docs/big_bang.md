# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T03:46:17+00:00`
- cycles_completed: `32`
- genesis seed: `cand_0001`
- last candidate: `cand_0185`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `32`

## Latest Step
- candidate: `cand_0185`
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
- `cand_0185`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2999730179732504`
- `cand_0184`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.344276638518601`
- `cand_0183`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3091300175665085`
- `cand_0182`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.39604896238835885`
- `cand_0181`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3121166161901515`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0177` -> audit `0.3589113262474345`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.332309, audit averaged 0.298515, and the mean transfer gap was 0.033794.`
- recent benchmark avg: `0.3323090505273741`
- recent audit avg: `0.2985152705207114`
- recent transfer gap avg: `0.03379378000666264`
- `cand_0185`: benchmark `0.2999730179732504`, audit `0.2508811584173397`, gap `0.049091859555910666`
- `cand_0184`: benchmark `0.344276638518601`, audit `0.3767879026228933`, gap `-0.03251126410429228`
- `cand_0183`: benchmark `0.3091300175665085`, audit `0.29660556201829824`, gap `0.012524455548210245`
- `cand_0182`: benchmark `0.39604896238835885`, audit `0.3274105571275263`, gap `0.06863840526083254`
- `cand_0181`: benchmark `0.3121166161901515`, audit `0.2408911724174995`, gap `0.07122544377265203`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `8`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (78 candidate(s), avg transfer gap 0.040975).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.040975. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 589.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `78`, audit_blocked `67`, avg_gap `0.0409751151665465`
- loss: `science_loss` (available); attempts `63`, audit_blocked `53`, avg_gap `0.041502642038740684`
- eval: `science_eval` (available); attempts `70`, audit_blocked `59`, avg_gap `0.04082058367158244`
- config: `science_config` (available); attempts `63`, audit_blocked `53`, avg_gap `0.041502642038740684`
- train: `science_train` (available); attempts `56`, audit_blocked `46`, avg_gap `0.04164450042121587`

### Recent Module Evidence
- `science_backend`: attempts `78`, audit_blocked `67`, avg_gap `0.0409751151665465`
- `science_model`: attempts `78`, audit_blocked `67`, avg_gap `0.0409751151665465`
- `science_eval`: attempts `70`, audit_blocked `59`, avg_gap `0.04082058367158244`
- `science_config`: attempts `63`, audit_blocked `53`, avg_gap `0.041502642038740684`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 3 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
