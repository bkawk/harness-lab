# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-02T20:24:39+00:00`
- last_heartbeat: `2026-04-18T06:40:48+00:00`
- cycles_completed: `1988`
- genesis seed: `cand_0001`
- last candidate: `cand_2412`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `328`

## Latest Step
- candidate: `cand_2412`
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
- active_candidate: `cand_2412`
- backend_status: `finished`
- backend_pid: `3108607`
- backend_started_at: `2026-04-18T06:30:43+00:00`
- backend_last_poll_at: `2026-04-18T06:40:46+00:00`
- backend_poll_interval_seconds: `1.0`

## Recent Candidates
- `cand_2412`: outcome `keeper`; diagnosis `complete`; benchmark `0.32324337499392874`
- `cand_2411`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28895296233712375`
- `cand_2410`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3454544395318337`
- `cand_2409`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2833084769612253`
- `cand_2408`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3224087267061642`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_2357` -> gap `-0.00011202849963909411`
- best stable: `cand_1857` -> audit `0.3982083419591221`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.312674, audit averaged 0.278447, and the mean transfer gap was 0.034227.`
- recent benchmark avg: `0.3126735961060551`
- recent audit avg: `0.278447023431623`
- recent transfer gap avg: `0.034226572674432146`
- `cand_2412`: benchmark `0.32324337499392874`, audit `0.3054842768054807`, gap `0.017759098188448064`
- `cand_2411`: benchmark `0.28895296233712375`, audit `0.23250180645200785`, gap `0.0564511558851159`
- `cand_2410`: benchmark `0.3454544395318337`, audit `0.2777659433946094`, gap `0.06768849613722427`
- `cand_2409`: benchmark `0.2833084769612253`, audit `0.24895686609600923`, gap `0.03435161086521607`
- `cand_2408`: benchmark `0.3224087267061642`, audit `0.3275262244100078`, gap `-0.005117497703843565`

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
- summary: `Mechanisms science_loss, science_train, science_model exhausted their follow-up budget; broaden the search.`
- exploration_mode: `force_broad_exploration`
- tracked_mechanisms: `13`

## Backend
- summary: `The repo-native science backend is available through the command runner with a realistic wall-clock training budget.`
- preferred_backend: `command`
- available_backends: `command, simulated`
- command_backend_configured: `True`

## Backend Science
- summary: `Recent backend evolution is concentrated in science_backend (2303 candidate(s), avg transfer gap 0.032144).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures point to transfer behavior that likely depends on model capacity and representation quality. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on broad mutation until the post-change sample is less thin. Small conservative lever nudges are still allowed. The last structural change could not be identified, so recent-signal gating is conservative.`
- secondary_context: `Recent real-backend runs are only using about 613.9 MB on average, leaving most VRAM unused. The last structural change could not be identified, so recent-signal gating is conservative.`
- scored_candidates_since_change: `0`
- last_structural_commit: `-`
### Chosen Lever Values
- source_candidate: `cand_2412`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_2412`
- model: `hidden_dim=160, global_dim=192, instance_dim=24, k_neighbors=8, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.08, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.0002, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (targeted); attempts `2303`, audit_blocked `969`, avg_gap `0.03214410729858532`
- loss: `science_loss` (available); attempts `2288`, audit_blocked `955`, avg_gap `0.032103371028514543`
- eval: `science_eval` (available); attempts `2295`, audit_blocked `961`, avg_gap `0.032108397430382435`
- config: `science_config` (available); attempts `2288`, audit_blocked `955`, avg_gap `0.032103371028514543`
- train: `science_train` (available); attempts `2281`, audit_blocked `948`, avg_gap `0.03207748191132201`

### Recent Module Evidence
- `science_backend`: attempts `2303`, audit_blocked `969`, avg_gap `0.03214410729858532`
- `science_model`: attempts `2303`, audit_blocked `969`, avg_gap `0.03214410729858532`
- `science_eval`: attempts `2295`, audit_blocked `961`, avg_gap `0.032108397430382435`
- `science_config`: attempts `2288`, audit_blocked `955`, avg_gap `0.032103371028514543`

### Code Context
- summary: `Backend code context maps the five modular science seams to their key functions, bounded lever surfaces, fixed implementation surfaces, and likely failure-mode touchpoints.`
- target_file: `src/harness_lab/science_model.py`
- target_purpose: `Defines the point-cloud model, local-neighborhood aggregation, and representation capacity surface.`
- key_functions: `CompactPointModel.__init__, CompactPointModel.forward, knn_indices, gather_neighbors`
- levered_surfaces: `hidden_dim, global_dim, instance_dim, k_neighbors, instance_modulation_scale`
- fixed_surfaces: `Point encoder and classifier topology; Fusion layout combining point, local, and global features; Instance pathway structure and normalization`

### Failure-To-Code Hints
- `boundary_smoke:gap_too_wide` -> `science_eval, science_loss, science_model`: `Boundary smoke regressions often reflect a mix of strict smoke-gap thresholds, weak boundary pressure in the loss, or insufficient boundary-sensitive representation capacity.`
- `hard_transfer_regression` -> `science_loss, science_model, science_config`: `Hard-transfer failures usually point to brittle transfer-sensitive structure, insufficient representation robustness, or seed defaults that underweight difficult cases.`
- `transfer_smoke:gap_too_wide` -> `science_eval, science_model`: `A wide benchmark-to-smoke gap is often governed by smoke gate strictness and by whether the model capacity generalizes beyond the local benchmark slice.`

### Code Change Brief
- decision_state: `wait`
- decision_reason: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`
- target_file: `src/harness_lab/science_model.py`
- target_functions: `CompactPointModel.__init__, CompactPointModel.forward, knn_indices, gather_neighbors`
- proposed_change: `Increase or rebalance representation capacity in a narrow way, such as local-context width or neighborhood strength, without touching smoke thresholds or runner behavior.`
- wait_option: `Recent evidence may still be too thin or too noisy for broad mutation, but conservative lever nudges are still allowed while more scored candidates accumulate.`

### Code Change Gate
- summary: `Machine-enforced scope and verification gate for the current code-change brief.`
- recommended_action: `wait`
- target_file: `src/harness_lab/science_model.py`
- max_changed_files: `2`
- allowed_write_files: `src/harness_lab/science_model.py, tests/test_science_model.py`
- focused_tests: `tests/test_science_model.py`
- verification_status: `No verification run recorded yet.`

### Autonomous Mutation
- summary: `Autonomous code mutation remains blocked for this seam.`
- eligible: `False`
- state: `blocked`
- reason: `Decision state is `wait`, so autonomous code mutation stays blocked. Recommended action is `wait`, not `targeted_mutation`.`
- execution_mode: `candidate_workspace_only`
- auto_publish: `False`
- silent_rollback: `False`

## External Review
- status: `idle`
- trigger_reason: `-`
- reviewer: `heuristic`
- summary: `After 2410 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `audit_score_below_keeper_band` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [12] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [10] `module_surface`: `Consider exposing `science_loss` as a more explicit evolvable backend module if it keeps dominating search.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `audit_score_below_keeper_band` if that failure mode keeps dominating.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`

## What We Did
- summary: `No recent human responses recorded yet.`
- response_file: `docs/lab_responses.json`
- no recent human responses recorded yet

## Diversity
- summary: `The lab has stayed on `science_loss` for 3 recent candidates; inject a novelty step.`
- current_mechanism_streak: `3`
- novelty_step_recommended: `True`
