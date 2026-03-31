# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-03-31T23:10:52+00:00`
- cycles_completed: `6`
- genesis seed: `cand_0001`
- last candidate: `cand_0159`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0159`
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
- `cand_0159`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.29029116689342593`
- `cand_0158`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3012152471872749`
- `cand_0157`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.31726446786090573`
- `cand_0156`: outcome `improved`; diagnosis `complete`; benchmark `0.28253004436822543`
- `cand_0155`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3358701997513282`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0155` -> audit `0.3332486601124782`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.305434, audit averaged 0.270028, and the mean transfer gap was 0.035406.`
- recent benchmark avg: `0.30543422521223207`
- recent audit avg: `0.27002822413986305`
- recent transfer gap avg: `0.035406001072369`
- `cand_0159`: benchmark `0.29029116689342593`, audit `0.2640949137166761`, gap `0.02619625317674984`
- `cand_0158`: benchmark `0.3012152471872749`, audit `0.21082715474001662`, gap `0.09038809244725826`
- `cand_0157`: benchmark `0.31726446786090573`, audit `0.24793809416843426`, gap `0.06932637369247147`
- `cand_0156`: benchmark `0.28253004436822543`, audit `0.29403229796171`, gap `-0.011502253593484557`
- `cand_0155`: benchmark `0.3358701997513282`, audit `0.3332486601124782`, gap `0.002621539638849979`

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
- summary: `Recent backend evolution is concentrated in science_backend (52 candidate(s), avg transfer gap 0.038890).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038890. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 595.9 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `52`, audit_blocked `46`, avg_gap `0.03888951039070013`
- loss: `science_loss` (available); attempts `37`, audit_blocked `32`, avg_gap `0.03896166172804723`
- eval: `science_eval` (available); attempts `44`, audit_blocked `38`, avg_gap `0.03821741246884015`
- config: `science_config` (available); attempts `37`, audit_blocked `32`, avg_gap `0.03896166172804723`
- train: `science_train` (available); attempts `30`, audit_blocked `25`, avg_gap `0.038581351805689106`

### Recent Module Evidence
- `science_backend`: attempts `52`, audit_blocked `46`, avg_gap `0.03888951039070013`
- `science_model`: attempts `52`, audit_blocked `46`, avg_gap `0.03888951039070013`
- `science_eval`: attempts `44`, audit_blocked `38`, avg_gap `0.03821741246884015`
- `science_config`: attempts `37`, audit_blocked `32`, avg_gap `0.03896166172804723`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 157 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- human advice: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 6 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `initial_harness` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `science_backend_error` if that failure mode keeps dominating.`
- [9] `ops`: `Harden backend startup and completion reporting so stalled candidates stop consuming full budget.`
- [7] `dataset`: `Consider improving the validation split or transfer-oriented data slices so the lab can distinguish local wins from robust gains sooner.`

## What We Did
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
