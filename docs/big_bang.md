# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T12:42:44+00:00`
- last_heartbeat: `2026-04-01T13:03:23+00:00`
- cycles_completed: `2`
- genesis seed: `cand_0001`
- last candidate: `cand_0243`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `2`

## Latest Step
- candidate: `cand_0243`
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
- `cand_0243`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.39747503873769563`
- `cand_0242`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.32215991546118283`
- `cand_0241`: outcome `-`; diagnosis `empty`; benchmark `None`
- `cand_0240`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3548846633190189`
- `cand_0239`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3088403526545396`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 4 scored candidates, benchmark averaged 0.345840, audit averaged 0.279497, and the mean transfer gap was 0.066343.`
- recent benchmark avg: `0.34583999254310926`
- recent audit avg: `0.2794974195444184`
- recent transfer gap avg: `0.06634257299869083`
- `cand_0243`: benchmark `0.39747503873769563`, audit `0.2977320794083679`, gap `0.09974295932932775`
- `cand_0242`: benchmark `0.32215991546118283`, audit `0.27121843600091877`, gap `0.05094147946026406`
- `cand_0240`: benchmark `0.3548846633190189`, audit `0.31551906150741504`, gap `0.03936560181160387`
- `cand_0239`: benchmark `0.3088403526545396`, audit `0.23352010126097195`, gap `0.07532025139356763`

## Hindsight
- summary: `In the recent scored window, the lab saw 7 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 242 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- selection_mode: `stabilize`
- cooldown_multiplier: `2.0`
- preferred_runner_backend: `command`
- publish_every_cycles: `1`
- novelty_cycle_priority: `high`

## Budget
- summary: `Mechanisms initial_harness, science_model, budget_policy_changed exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `9`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (135 candidate(s), avg transfer gap 0.038006).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.038006. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. 1 scored candidate(s) have landed since structural commit `678f462`.`
- secondary_context: `Recent real-backend runs are only using about 592.9 MB on average, leaving most VRAM unused. 1 scored candidate(s) have landed since structural commit `678f462`.`
- scored_candidates_since_change: `1`
- last_structural_commit: `678f462`
### Chosen Lever Values
- source_candidate: `cand_0243`
- no explicit lever values chosen yet

### Effective Backend Settings
- source_candidate: `cand_0243`
- model: `hidden_dim=96, global_dim=192, instance_dim=12, k_neighbors=8, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.02, instance_margin=0.35`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `135`, audit_blocked `110`, avg_gap `0.03800575300548311`
- loss: `science_loss` (available); attempts `120`, audit_blocked `96`, avg_gap `0.0379147488043525`
- eval: `science_eval` (available); attempts `127`, audit_blocked `102`, avg_gap `0.03771050104064715`
- config: `science_config` (available); attempts `120`, audit_blocked `96`, avg_gap `0.0379147488043525`
- train: `science_train` (available); attempts `113`, audit_blocked `89`, avg_gap `0.03774223156543552`

### Recent Module Evidence
- `science_backend`: attempts `135`, audit_blocked `110`, avg_gap `0.03800575300548311`
- `science_model`: attempts `135`, audit_blocked `110`, avg_gap `0.03800575300548311`
- `science_eval`: attempts `127`, audit_blocked `102`, avg_gap `0.03771050104064715`
- `science_config`: attempts `120`, audit_blocked `96`, avg_gap `0.0379147488043525`

## External Review
- status: `reviewed`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 242 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `transfer_smoke_failed` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_model` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `transfer_smoke_failed` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `science_model` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
