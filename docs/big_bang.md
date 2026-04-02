# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T07:18:36+00:00`
- cycles_completed: `52`
- genesis seed: `cand_0001`
- last candidate: `cand_0350`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `normal_cycle`
- novelty cycles triggered: `6`

## Latest Step
- candidate: `cand_0350`
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
- `cand_0350`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.342676815071689`
- `cand_0349`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3378285449757641`
- `cand_0348`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.28712588257609695`
- `cand_0347`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.38893545131781926`
- `cand_0346`: outcome `dead_end`; diagnosis `complete`; benchmark `0.31127907756708684`

## Science Leaders
- best benchmark: `cand_0327` -> `0.5031005280065836`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.333569, audit averaged 0.315808, and the mean transfer gap was 0.017761.`
- recent benchmark avg: `0.3335691543016912`
- recent audit avg: `0.3158081307093427`
- recent transfer gap avg: `0.017761023592348525`
- `cand_0350`: benchmark `0.342676815071689`, audit `0.36287779989776237`, gap `-0.020200984826073354`
- `cand_0349`: benchmark `0.3378285449757641`, audit `0.30740775786450825`, gap `0.030420787111255843`
- `cand_0348`: benchmark `0.28712588257609695`, audit `0.2621984108350814`, gap `0.02492747174101556`
- `cand_0347`: benchmark `0.38893545131781926`, audit `0.35684454087911605`, gap `0.03209091043870321`
- `cand_0346`: benchmark `0.31127907756708684`, audit `0.2897121440702455`, gap `0.021566933496841356`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 3 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_eval` until new evidence appears.`

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
- summary: `Recent backend evolution is concentrated in science_backend (242 candidate(s), avg transfer gap 0.038035).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 689.1 MB on average, leaving most VRAM unused. 51 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `51`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0350`
- loss: `boundary_loss_weight=0.12, instance_margin=0.38`

### Effective Backend Settings
- source_candidate: `cand_0350`
- model: `hidden_dim=96, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.05`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.12, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `242`, audit_blocked `148`, avg_gap `0.03803511544148907`
- loss: `science_loss` (targeted); attempts `227`, audit_blocked `134`, avg_gap `0.03798827611233068`
- eval: `science_eval` (available); attempts `234`, audit_blocked `140`, avg_gap `0.03787378014738339`
- config: `science_config` (available); attempts `227`, audit_blocked `134`, avg_gap `0.03798827611233068`
- train: `science_train` (available); attempts `220`, audit_blocked `127`, avg_gap `0.037901122708179226`

### Recent Module Evidence
- `science_backend`: attempts `242`, audit_blocked `148`, avg_gap `0.03803511544148907`
- `science_model`: attempts `242`, audit_blocked `148`, avg_gap `0.03803511544148907`
- `science_eval`: attempts `234`, audit_blocked `140`, avg_gap `0.03787378014738339`
- `science_config`: attempts `227`, audit_blocked `134`, avg_gap `0.03798827611233068`

## External Review
- status: `cooldown`
- trigger_reason: `repeated_audit_blocked`
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
- summary: `Recent branching still has room, but `science_loss` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
