# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T07:54:30+00:00`
- last_heartbeat: `2026-04-01T08:04:33+00:00`
- cycles_completed: `1`
- genesis seed: `cand_0001`
- last candidate: `cand_0211`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `0`

## Latest Step
- candidate: `cand_0211`
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
- `cand_0211`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.36243190781179485`
- `cand_0210`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0209`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3559216505182819`
- `cand_0208`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0207`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3627513425494484`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0206` -> gap `0.001425120340833974`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 3 scored candidates, benchmark averaged 0.360368, audit averaged 0.318142, and the mean transfer gap was 0.042226.`
- recent benchmark avg: `0.360368300293175`
- recent audit avg: `0.318141946163141`
- recent transfer gap avg: `0.042226354130034026`
- `cand_0211`: benchmark `0.36243190781179485`, audit `0.3089735794882592`, gap `0.05345832832353564`
- `cand_0209`: benchmark `0.3559216505182819`, audit `0.3380635537857295`, gap `0.017858096732552398`
- `cand_0207`: benchmark `0.3627513425494484`, audit `0.3073887052154344`, gap `0.05536263733401403`

## Hindsight
- summary: `In the recent scored window, the lab saw 8 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_model` until new evidence appears.`

## Policy
- summary: `After 210 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, budget_policy_changed, fusion_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `9`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (103 candidate(s), avg transfer gap 0.038986).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038986. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `575060b`.`
- secondary_context: `Recent real-backend runs are only using about 592.4 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `575060b`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `575060b`
### Chosen Lever Values
- source_candidate: `cand_0211`
- no explicit lever values chosen yet

### Modular Levers
- model: `science_model` (targeted); attempts `103`, audit_blocked `87`, avg_gap `0.03898646272781765`
- loss: `science_loss` (available); attempts `88`, audit_blocked `73`, avg_gap `0.03903237210359412`
- eval: `science_eval` (available); attempts `95`, audit_blocked `79`, avg_gap `0.03869311106290239`
- config: `science_config` (available); attempts `88`, audit_blocked `73`, avg_gap `0.03903237210359412`
- train: `science_train` (available); attempts `81`, audit_blocked `66`, avg_gap `0.03890377479734621`

### Recent Module Evidence
- `science_backend`: attempts `103`, audit_blocked `87`, avg_gap `0.03898646272781765`
- `science_model`: attempts `103`, audit_blocked `87`, avg_gap `0.03898646272781765`
- `science_eval`: attempts `95`, audit_blocked `79`, avg_gap `0.03869311106290239`
- `science_config`: attempts `88`, audit_blocked `73`, avg_gap `0.03903237210359412`

## External Review
- status: `reviewed`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 210 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
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
- summary: `The lab has stayed on `science_model` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
