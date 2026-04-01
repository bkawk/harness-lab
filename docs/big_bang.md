# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T05:29:00+00:00`
- last_heartbeat: `2026-04-01T07:25:00+00:00`
- cycles_completed: `11`
- genesis seed: `cand_0001`
- last candidate: `cand_0206`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `11`

## Latest Step
- candidate: `cand_0206`
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
- `cand_0206`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28357429775165255`
- `cand_0205`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.39838436739098154`
- `cand_0204`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.4034031200430859`
- `cand_0203`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3482853346963483`
- `cand_0202`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30790769447857963`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.348311, audit averaged 0.311019, and the mean transfer gap was 0.037292.`
- recent benchmark avg: `0.3483109628721296`
- recent audit avg: `0.3110185393458251`
- recent transfer gap avg: `0.0372924235263045`
- `cand_0206`: benchmark `0.28357429775165255`, audit `0.2821491774108186`, gap `0.001425120340833974`
- `cand_0205`: benchmark `0.39838436739098154`, audit `0.3179206977508648`, gap `0.08046366964011675`
- `cand_0204`: benchmark `0.4034031200430859`, audit `0.33011392309989257`, gap `0.07328919694319336`
- `cand_0203`: benchmark `0.3482853346963483`, audit `0.3790332192959275`, gap `-0.030747884599579167`
- `cand_0202`: benchmark `0.30790769447857963`, audit `0.24587567917162206`, gap `0.062032015306957566`

## Hindsight
- summary: `In the recent scored window, the lab saw 8 audit-blocked outcomes; it should emphasize transfer-stability checks.`
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
- summary: `Recent backend evolution is concentrated in science_backend (99 candidate(s), avg transfer gap 0.038883).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038883. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- secondary_context: `Recent real-backend runs are only using about 595.2 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `aec3acb`
### Chosen Lever Values
- source_candidate: `cand_0206`
- no explicit lever values chosen yet

### Modular Levers
- model: `science_model` (targeted); attempts `99`, audit_blocked `84`, avg_gap `0.03888306193838521`
- loss: `science_loss` (available); attempts `84`, audit_blocked `70`, avg_gap `0.03891259777760263`
- eval: `science_eval` (available); attempts `91`, audit_blocked `76`, avg_gap `0.038569858397769885`
- config: `science_config` (available); attempts `84`, audit_blocked `70`, avg_gap `0.03891259777760263`
- train: `science_train` (available); attempts `77`, audit_blocked `63`, avg_gap `0.03876723044120836`

### Recent Module Evidence
- `science_backend`: attempts `99`, audit_blocked `84`, avg_gap `0.03888306193838521`
- `science_model`: attempts `99`, audit_blocked `84`, avg_gap `0.03888306193838521`
- `science_eval`: attempts `91`, audit_blocked `76`, avg_gap `0.038569858397769885`
- `science_config`: attempts `84`, audit_blocked `70`, avg_gap `0.03891259777760263`

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
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
