# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T02:00:22+00:00`
- cycles_completed: `22`
- genesis seed: `cand_0001`
- last candidate: `cand_0175`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `22`

## Latest Step
- candidate: `cand_0175`
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
- `cand_0175`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32597718606334886`
- `cand_0174`: outcome `improved`; diagnosis `complete`; benchmark `0.26639875963606036`
- `cand_0173`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3361496020750038`
- `cand_0172`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3679953081293829`
- `cand_0171`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3092432551702846`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0168` -> audit `0.3564474663677673`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.321153, audit averaged 0.285148, and the mean transfer gap was 0.036005.`
- recent benchmark avg: `0.3211528222148161`
- recent audit avg: `0.28514759657614486`
- recent transfer gap avg: `0.036005225638671236`
- `cand_0175`: benchmark `0.32597718606334886`, audit `0.2485482826525044`, gap `0.07742890341084446`
- `cand_0174`: benchmark `0.26639875963606036`, audit `0.30563936789187574`, gap `-0.03924060825581538`
- `cand_0173`: benchmark `0.3361496020750038`, audit `0.3252721143011864`, gap `0.010877487773817363`
- `cand_0172`: benchmark `0.3679953081293829`, audit `0.2782413117792644`, gap `0.08975399635011849`
- `cand_0171`: benchmark `0.3092432551702846`, audit `0.2680369062558934`, gap `0.04120634891439123`

## Hindsight
- summary: `In the recent scored window, the lab saw 6 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
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
- summary: `Recent backend evolution is concentrated in science_backend (68 candidate(s), avg transfer gap 0.040214).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.040214. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 593.4 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `68`, audit_blocked `59`, avg_gap `0.04021445592365205`
- loss: `science_loss` (available); attempts `53`, audit_blocked `45`, avg_gap `0.04063450358227461`
- eval: `science_eval` (available); attempts `60`, audit_blocked `51`, avg_gap `0.0399236639127452`
- config: `science_config` (available); attempts `53`, audit_blocked `45`, avg_gap `0.04063450358227461`
- train: `science_train` (available); attempts `46`, audit_blocked `38`, avg_gap `0.04066802742124956`

### Recent Module Evidence
- `science_backend`: attempts `68`, audit_blocked `59`, avg_gap `0.04021445592365205`
- `science_model`: attempts `68`, audit_blocked `59`, avg_gap `0.04021445592365205`
- `science_eval`: attempts `60`, audit_blocked `51`, avg_gap `0.0399236639127452`
- `science_config`: attempts `53`, audit_blocked `45`, avg_gap `0.04063450358227461`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `none`
- summary: `No external review yet.`
- lab advice: `No live external advice.`
- human advice: `No human-facing advice.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
