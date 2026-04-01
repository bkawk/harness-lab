# Big Bang

The GitHub repo is the lab dashboard.

## State
- status: `running`
- vital_spark_at: `2026-03-31T10:12:12+00:00`
- started_at: `2026-03-31T22:07:51+00:00`
- last_heartbeat: `2026-04-01T04:39:24+00:00`
- cycles_completed: `37`
- genesis seed: `cand_0001`
- last candidate: `cand_0190`
- last dataset: `abc_boundary512`
- last commit: `-`
- last publish message: `Publishing skipped.`
- last cycle mode: `novelty_cycle`
- novelty cycles triggered: `37`

## Latest Step
- candidate: `cand_0190`
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
- `cand_0190`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3106586247355788`
- `cand_0189`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.34293915302063094`
- `cand_0188`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.3792516104876982`
- `cand_0187`: outcome `audit_blocked`; diagnosis `complete`; benchmark `0.33833676754710607`
- `cand_0186`: outcome `improved`; diagnosis `complete`; benchmark `0.27670261293014486`

## Science Leaders
- best benchmark: `cand_0103` -> `0.448`
- best audit: `cand_0103` -> `0.418`
- tightest transfer: `cand_0146` -> gap `0.002621539638849979`
- best stable: `cand_0188` -> audit `0.36012895209447643`

## Science Trend
- summary: `Across the last 5 scored candidates, benchmark averaged 0.329578, audit averaged 0.292186, and the mean transfer gap was 0.037392.`
- recent benchmark avg: `0.32957775374423176`
- recent audit avg: `0.292185946612692`
- recent transfer gap avg: `0.03739180713153979`
- `cand_0190`: benchmark `0.3106586247355788`, audit `0.2448624311687765`, gap `0.0657961935668023`
- `cand_0189`: benchmark `0.34293915302063094`, audit `0.3139592458747021`, gap `0.02897990714592885`
- `cand_0188`: benchmark `0.3792516104876982`, audit `0.36012895209447643`, gap `0.019122658393221748`
- `cand_0187`: benchmark `0.33833676754710607`, audit `0.24348163373120418`, gap `0.09485513381590188`
- `cand_0186`: benchmark `0.27670261293014486`, audit `0.2984974701943007`, gap `-0.02179485726415581`

## Hindsight
- summary: `In the recent scored window, the lab saw 6 audit-blocked outcomes; it should emphasize transfer-stability checks.`
- adjustment: `Increase cooldown penalties for mechanisms with repeated dead_end outcomes.`
- adjustment: `Raise priority for proposals that directly target transfer stability after an audit_blocked result.`

## Policy
- summary: `After 189 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `Recent backend evolution is concentrated in science_backend (83 candidate(s), avg transfer gap 0.040748).`
- recommended_action: `wait`
- target_module: `science_model`
- problem: `Improve transfer-stability evaluation or smoke tests so promising candidates fail earlier before full audit.`
- why_this_module: `Recent backend edits are concentrated in `science_model` with average transfer gap 0.040748. Secondary signal: VRAM headroom is present, but it is not the main reason for this recommendation. Hold off on a mutation until the post-change sample is less thin. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- secondary_context: `Recent real-backend runs are only using about 593.5 MB on average, leaving most VRAM unused. 0 scored candidate(s) have landed since structural commit `320fcac`.`
- scored_candidates_since_change: `0`
- last_structural_commit: `320fcac`
### Modular Levers
- model: `science_model` (targeted); attempts `83`, audit_blocked `71`, avg_gap `0.040748323518761266`
- loss: `science_loss` (available); attempts `68`, audit_blocked `57`, avg_gap `0.041186423968956`
- eval: `science_eval` (available); attempts `75`, audit_blocked `63`, avg_gap `0.04057912053495972`
- config: `science_config` (available); attempts `68`, audit_blocked `57`, avg_gap `0.041186423968956`
- train: `science_train` (available); attempts `61`, audit_blocked `50`, avg_gap `0.04127788893072655`

### Recent Module Evidence
- `science_backend`: attempts `83`, audit_blocked `71`, avg_gap `0.040748323518761266`
- `science_model`: attempts `83`, audit_blocked `71`, avg_gap `0.040748323518761266`
- `science_eval`: attempts `75`, audit_blocked `63`, avg_gap `0.04057912053495972`
- `science_config`: attempts `68`, audit_blocked `57`, avg_gap `0.041186423968956`

## External Review
- status: `reviewed`
- trigger_reason: `repeated_audit_blocked`
- reviewer: `heuristic`
- summary: `After 189 candidates, the lab requested peer review because `repeated_audit_blocked` fired. Current policy mode is `stabilize`.`
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
- summary: `The humans recently addressed 1 lab request(s).`
- `seed_backend` addressed by `61b6720`: `Split the seed backend into more explicit evolvable modules so the lab can steer model, loss, eval, and config changes more precisely.`

## Diversity
- summary: `The lab has stayed on `initial_harness` for 6 recent candidates; inject a novelty step.`
- current_mechanism_streak: `6`
- novelty_step_recommended: `True`
