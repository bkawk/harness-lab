# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-04-01T21:39:36+00:00`
- last_heartbeat: `2026-04-02T00:15:53+00:00`
- cycles_completed: `14`
- genesis seed: `cand_0001`
- last candidate: `cand_0312`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `3`

## Latest Step
- candidate: `cand_0312`
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
- `cand_0312`: outcome `dead_end`; diagnosis `complete`; benchmark `0.3353497352026351`
- `cand_0311`: outcome `dead_end`; diagnosis `complete`; benchmark `0.34902284133616246`
- `cand_0310`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.2849482988243342`
- `cand_0309`: outcome `dead_end`; diagnosis `complete`; benchmark `0.46003062144822787`
- `cand_0308`: outcome `dead_end`; diagnosis `complete`; benchmark `0.39786773820750965`

## Science Leaders
- best benchmark: `cand_0281` -> `0.4640540113671977`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0238` -> gap `0.0011169645632786995`
- best stable: `cand_0296` -> audit `0.3692495721811836`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.365444, audit averaged 0.314103, and the mean transfer gap was 0.051341.`
- recent benchmark avg: `0.36544384700377386`
- recent audit avg: `0.314102971828586`
- recent transfer gap avg: `0.05134087517518791`
- `cand_0312`: benchmark `0.3353497352026351`, audit `0.36621014235286986`, gap `-0.030860407150234748`
- `cand_0311`: benchmark `0.34902284133616246`, audit `0.3213434778296967`, gap `0.02767936350646577`
- `cand_0310`: benchmark `0.2849482988243342`, audit `0.2198169044385574`, gap `0.06513139438577681`
- `cand_0309`: benchmark `0.46003062144822787`, audit `0.362591512181426`, gap `0.09743910926680188`
- `cand_0308`: benchmark `0.39786773820750965`, audit `0.30055282234037983`, gap `0.09731491586712981`

## Hindsight
- summary: `In the recent scored window, the lab repeated dead-end candidates 5 times; similar proposal shapes should cool down sooner.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`
- adjustment: `Reduce parent/proposal priority for `science_loss` until new evidence appears.`

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
- summary: `Recent backend evolution is concentrated in science_backend (204 candidate(s), avg transfer gap 0.037171).`
- recommended_action: `targeted_mutation`
- target_module: `science_loss`
- problem: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- why_this_module: `Recent failures are boundary-transfer specific, so the loss surface is the best next bounded module to adjust. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation.`
- secondary_context: `Recent real-backend runs are only using about 727.5 MB on average, leaving most VRAM unused. 13 scored candidate(s) have landed since structural commit `49fb173`.`
- scored_candidates_since_change: `13`
- last_structural_commit: `49fb173`
### Chosen Lever Values
- source_candidate: `cand_0312`
- model: `hidden_dim=160, instance_modulation_scale=0.15`

### Effective Backend Settings
- source_candidate: `cand_0312`
- model: `hidden_dim=160, global_dim=256, instance_dim=12, k_neighbors=10, instance_modulation_scale=0.15`
- loss: `param_loss_weight=0.2, boundary_loss_weight=0.15, instance_loss_weight=0.06, instance_margin=0.38`
- eval: `transfer_smoke_min_score=0.24, transfer_smoke_max_gap=0.03, transfer_smoke_min_boundary_f1=0.12`
- config: `lr=0.00025, weight_decay=0.0002, time_budget_seconds=600, eval_reserve_seconds=120`
- train: `batch_size=2, eval_batch_size=2, grad_clip=1.0, log_interval=20`

### Modular Levers
- model: `science_model` (available); attempts `204`, audit_blocked `134`, avg_gap `0.037171018078652515`
- loss: `science_loss` (targeted); attempts `189`, audit_blocked `120`, avg_gap `0.037040074158053334`
- eval: `science_eval` (available); attempts `196`, audit_blocked `126`, avg_gap `0.03693340488934971`
- config: `science_config` (available); attempts `189`, audit_blocked `120`, avg_gap `0.037040074158053334`
- train: `science_train` (available); attempts `182`, audit_blocked `113`, avg_gap `0.03688995086125823`

### Recent Module Evidence
- `science_backend`: attempts `204`, audit_blocked `134`, avg_gap `0.037171018078652515`
- `science_model`: attempts `204`, audit_blocked `134`, avg_gap `0.037171018078652515`
- `science_eval`: attempts `196`, audit_blocked `126`, avg_gap `0.03693340488934971`
- `science_config`: attempts `189`, audit_blocked `120`, avg_gap `0.037040074158053334`

## External Review
- status: `cooldown`
- trigger_reason: `exhaustion_signal`
- reviewer: `heuristic`
- summary: `After 310 candidates, the lab requested peer review because `exhaustion_signal` fired. Current policy mode is `stabilize`.`
- lab advice: `Bias the next branch toward under-explored backend fingerprints or mechanisms instead of repeating the current local basin.`
- human advice: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- human advice: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What The Lab Wants
- summary: `The lab has 4 ranked requests for human help.`
- [10] `non_self_evolving`: `Consider strengthening the non-self-evolving seed around `boundary_smoke:gap_too_wide` if that failure mode keeps dominating.`
- [6] `evaluation`: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- [5] `vram_headroom`: `Consider increasing batch size or model capacity so the science backend uses more of the available VRAM.`
- [4] `module_surface`: `Consider exposing `science_train` as a more explicit evolvable backend module if it keeps dominating search.`

## What We Did
- summary: `The humans recently addressed 2 lab request(s).`
- response_file: `docs/lab_responses.json`
- `module_surface` addressed by `32debd4`: `Made backend targeting failure-aware so the lab can steer bounded changes toward the right module instead of revisiting a generic basin.`
- `evaluation` addressed by `23dc0ec`: `Refined transfer failure attribution so the lab can tell local-only gains, hard-transfer regressions, and boundary failures apart.`

## Diversity
- summary: `Recent branching still has room, but `science_model` is the current active line.`
- current_mechanism_streak: `1`
- novelty_step_recommended: `False`
