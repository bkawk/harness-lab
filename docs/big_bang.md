# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T05:29:00+00:00`
- last_heartbeat: `2026-04-01T06:32:02+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0201`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0201`
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
- `cand_0201`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3001193599820565`
- `cand_0200`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34117131400763645`
- `cand_0199`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31934057811013555`
- `cand_0198`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34325512536238556`
- `cand_0197`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3111798670149263`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.323013, audit averaged 0.290535, and the mean transfer gap was 0.032479.`
- recent benchmark avg: `0.3230132488954281`
- recent audit avg: `0.29053453137217267`
- recent transfer gap avg: `0.03247871752325543`
- `cand_0201`: benchmark `0.3001193599820565`, audit `0.24026370614574744`, gap `0.059855653836309086`
- `cand_0200`: benchmark `0.34117131400763645`, audit `0.30269102975176154`, gap `0.03848028425587491`
- `cand_0199`: benchmark `0.31934057811013555`, audit `0.31125732683600704`, gap `0.008083251274128511`
- `cand_0198`: benchmark `0.34325512536238556`, audit `0.32914814808038473`, gap `0.014106977282000832`
- `cand_0197`: benchmark `0.3111798670149263`, audit `0.2693124460469625`, gap `0.04186742096796381`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 2 times; similar proposal shapes should cool down sooner.`
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
- summary: `Recent backend evolution is concentrated in science_backend (94 candidate(s), avg transfer gap 0.038972).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038972. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- secondary_context: `Recent real-backend runs are only using about 592.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `aec3acb`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `aec3acb`
### Chosen Lever Values
- source_candidate: `cand_0201`
- no explicit lever values chosen yet

### Modular Levers
- model: `science_model` (targeted); attempts `94`, audit_blocked `79`, avg_gap `0.03897242364692908`
- loss: `science_loss` (available); attempts `79`, audit_blocked `65`, avg_gap `0.03902060939435584`
- eval: `science_eval` (available); attempts `86`, audit_blocked `71`, avg_gap `0.03864871240218133`
- config: `science_config` (available); attempts `79`, audit_blocked `65`, avg_gap `0.03902060939435584`
- train: `science_train` (available); attempts `72`, audit_blocked `58`, avg_gap `0.03887567212612776`

### Recent Module Evidence
- `science_backend`: attempts `94`, audit_blocked `79`, avg_gap `0.03897242364692908`
- `science_model`: attempts `94`, audit_blocked `79`, avg_gap `0.03897242364692908`
- `science_eval`: attempts `86`, audit_blocked `71`, avg_gap `0.03864871240218133`
- `science_config`: attempts `79`, audit_blocked `65`, avg_gap `0.03902060939435584`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 199 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- human advice: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 5 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
