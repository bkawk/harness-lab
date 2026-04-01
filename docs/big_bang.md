# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T05:29:00+00:00`
- last_heartbeat: `2026-04-01T06:53:13+00:00`
- cycles_completed: `8`
- genesis seed: `cand_0001`
- last candidate: `cand_0203`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `8`

## Latest Step
- candidate: `cand_0203`
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
- `cand_0203`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3482853346963483`
- `cand_0202`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.30790769447857963`
- `cand_0201`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3001193599820565`
- `cand_0200`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34117131400763645`
- `cand_0199`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31934057811013555`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.323365, audit averaged 0.295824, and the mean transfer gap was 0.027541.`
- recent benchmark avg: `0.32336485625495126`
- recent audit avg: `0.2958241922402131`
- recent transfer gap avg: `0.027540664014738182`
- `cand_0203`: benchmark `0.3482853346963483`, audit `0.3790332192959275`, gap `-0.030747884599579167`
- `cand_0202`: benchmark `0.30790769447857963`, audit `0.24587567917162206`, gap `0.062032015306957566`
- `cand_0201`: benchmark `0.3001193599820565`, audit `0.24026370614574744`, gap `0.059855653836309086`
- `cand_0200`: benchmark `0.34117131400763645`, audit `0.30269102975176154`, gap `0.03848028425587491`
- `cand_0199`: benchmark `0.31934057811013555`, audit `0.31125732683600704`, gap `0.008083251274128511`

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
- summary: `Recent backend evolution is concentrated in science_backend (96 candidate(s), avg transfer gap 0.038460).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038460. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- secondary_context: `Recent real-backend runs are only using about 595.2 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `aec3acb`
### Chosen Lever Values
- source_candidate: `cand_0203`
- no explicit lever values chosen yet

### Modular Levers
- model: `science_model` (targeted); attempts `96`, audit_blocked `81`, avg_gap `0.038459668519605125`
- loss: `science_loss` (available); attempts `81`, audit_blocked `67`, avg_gap `0.03841337448420865`
- eval: `science_eval` (available); attempts `88`, audit_blocked `73`, avg_gap `0.03809433536486827`
- config: `science_config` (available); attempts `81`, audit_blocked `67`, avg_gap `0.03841337448420865`
- train: `science_train` (available); attempts `74`, audit_blocked `60`, avg_gap `0.038211854789772376`

### Recent Module Evidence
- `science_backend`: attempts `96`, audit_blocked `81`, avg_gap `0.038459668519605125`
- `science_model`: attempts `96`, audit_blocked `81`, avg_gap `0.038459668519605125`
- `science_eval`: attempts `88`, audit_blocked `73`, avg_gap `0.03809433536486827`
- `science_config`: attempts `81`, audit_blocked `67`, avg_gap `0.03841337448420865`

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
