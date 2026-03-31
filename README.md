# harness-lab

A living research harness for AI researchers trying to train systems that can turn triangle meshes into structured parametric representations.

The core bet is that we should optimize the full research harness, not just individual model tweaks.
Instead of compressing experiments down to a score and a prompt, `harness-lab` treats each candidate as a first-class workspace with traces, diagnosis, plans, outcomes, and memory.

This repo is meant to feel alive:
- every candidate is a workspace, not just a score
- every workspace can accumulate diagnosis, plans, outcomes, and memory
- every workspace now captures harness source provenance and raw runner traces
- the lab can draft follow-ups from prior evidence
- every candidate can begin with a bootstrap snapshot of the current scientific situation
- the lab can notice the machine it is running on and adapt its assumptions
- the lab can look back over its own evolutions and write explicit hindsight
- the lab can let hindsight change what it tries next
- the lab can decide when it needs bounded outside perspective and split that into `lab_advice` and `human_advice`
- the lab can derive an explicit policy state from hindsight and hardware
- the lab can enforce simple exploration budgets across mechanisms
- the lab can watch recent branch diversity and inject novelty steps when it gets repetitive
- `big-bang` can now recognize novelty cycles and surface them explicitly in the repo dashboard
- the precise `vital spark` timestamp is preserved the first time `big-bang` is lit
- the lab can reconcile what happened and publish tracked structural evolution
- the GitHub repo can act as the lab dashboard through tracked status pages and self-published evolution

If you care about Meta-Harness style systems, this is the important bet:
- let the lab look at the filesystem-native evidence of prior attempts
- let it explain what it thinks failed
- let it propose the next move from that evidence
- let it keep a durable memory of why it changed

## Direction

The main shift is toward:
- proposal generation from raw run traces
- harness evolution, not just strategy selection
- first-class candidate workspaces
- diagnosis from full logs, diffs, and audit evidence
- synthesis across many prior runs

The concrete long-term target is still mesh to parametric:
- mesh inputs
- learned structured intermediate reasoning
- parametric or CAD-like outputs

This repo is the research harness for getting there, not the finished model itself.

## Current Capabilities

Right now `harness-lab` can:
- create self-contained candidate workspaces
- build a queryable cross-run memory index
- capture structured diagnosis
- draft proposals from diagnosis and memory
- write a candidate bootstrap snapshot before drafting the next move
- rank parent candidates explicitly
- generate execution plans
- capture harness source snapshots and parent diffs per candidate
- record structured outcomes
- write backend command/output traces into the candidate workspace
- execute real external command backends through a stable result contract
- detect backend readiness and let policy switch from simulation to a real command backend automatically
- ship with a repo-native science backend so a fresh clone can train and score candidates without depending on other repos
- run that real science backend on a realistic default `600` second wall-clock budget instead of toy-length probes
- reconcile outcomes back into diagnosis
- write a hindsight artifact about what it should have done differently
- use hindsight to influence parent ranking and next-step proposals
- derive a policy state that changes cooldowns, backend preference, and publish cadence
- trigger bounded external review with hard gates and cooldowns
- enforce follow-up budgets so exhausted mechanisms stop dominating the search
- let budget force a broader branch when the current line has had enough chances
- let short-term diversity trigger novelty steps before the search feels stale
- detect and record the hardware it is running on
- carry hardware context into planning and execution
- use hardware context to influence parent ranking and proposal shape
- register and import datasets with provenance instead of depending on sibling repos
- bootstrap ABC-backed dataset sources directly into the repo
- build prepared local ABC datasets inside the repo
- consult the dataset registry before execution
- push tracked source/docs evolution to GitHub in a controlled way
- run a long-lived `big-bang` supervisor that seeds, evolves, and republishes the lab state
- surface live backend polling state in the repo dashboard while science is still running

## Initial docs

- `docs/project_plan.md`
- `docs/workspace_layout.md`
- `docs/memory_index.md`
- `docs/diagnosis_schema.md`
- `docs/proposal_schema.md`
- `docs/parent_synthesis.md`
- `docs/execution_plan.md`
- `docs/outcome_schema.md`
- `docs/reconciliation.md`
- `docs/publishing.md`
- `docs/loop.md`
- `docs/simulation.md`
- `docs/runner.md`
- `docs/hardware.md`
- `docs/datasets.md`
- `docs/abc_build.md`
- `docs/evidence.md`
- `docs/hindsight.md`
- `docs/policy.md`
- `docs/budget.md`
- `docs/diversity.md`
- `docs/backend_science_plan.md`
- `docs/external_review.md`
- `docs/bootstrap_snapshot.md`

## Quick Start

Create a candidate workspace with:

```bash
PYTHONPATH=src python3 scripts/create_candidate.py cand_0001
```

Build a cross-run candidate index with:

```bash
PYTHONPATH=src python3 scripts/build_memory_index.py
```

Build a hindsight artifact with:

```bash
PYTHONPATH=src python3 scripts/build_hindsight.py
```

Build the current lab policy with:

```bash
PYTHONPATH=src python3 scripts/build_policy.py
```

Build the current bounded external review artifact with:

```bash
PYTHONPATH=src python3 scripts/build_external_review.py
```

Build the current diversity artifact with:

```bash
PYTHONPATH=src python3 scripts/build_diversity.py
```

Update a candidate diagnosis with:

```bash
PYTHONPATH=src python3 scripts/update_diagnosis.py cand_0001 --status in_progress
```

Draft a new proposal from diagnosis memory with:

```bash
PYTHONPATH=src python3 scripts/draft_proposal.py cand_0002
```

Write a candidate bootstrap snapshot from current lab state with:

```bash
PYTHONPATH=src python3 scripts/build_bootstrap_snapshot.py cand_0002 --dataset-id abc_boundary512
```

Rank parent candidates explicitly with:

```bash
PYTHONPATH=src python3 scripts/synthesize_parents.py --write-index
```

Create an execution plan for a drafted candidate with:

```bash
PYTHONPATH=src python3 scripts/plan_execution.py cand_0002
```

Record the outcome of an executed candidate with:

```bash
PYTHONPATH=src python3 scripts/update_outcome.py cand_0002 --status complete
```

Reconcile diagnosis from that outcome with:

```bash
PYTHONPATH=src python3 scripts/reconcile_diagnosis.py cand_0002
```

Publish tracked lab evolution to GitHub with:

```bash
PYTHONPATH=src python3 scripts/publish_lab.py --message "Describe the structural change"
```

Advance one candidate through the local loop with:

```bash
PYTHONPATH=src python3 scripts/advance_loop.py cand_0002
```

Run that same loop while explicitly anchoring source capture to the repo root:

```bash
PYTHONPATH=src python3 scripts/advance_loop.py cand_0002 --repo-dir .
```

Run one full lab step with data readiness, next-candidate creation, loop advancement, and optional publishing:

```bash
PYTHONPATH=src python3 scripts/run_lab.py \
  --source-dataset-id abc_raw_v1 \
  --prepared-dataset-id abc_boundary512
```

Run the long-lived supervisor:

```bash
PYTHONPATH=src python3 scripts/big_bang.py \
  --source-dataset-id abc_raw_v1 \
  --prepared-dataset-id abc_boundary512 \
  --cycles 0
```

Or manage the same long-running lab process with the repo-local control wrapper:

```bash
scripts/big_bang_ctl.sh start
scripts/big_bang_ctl.sh status
scripts/big_bang_ctl.sh stop
```

Reset the lab back to a clean genesis-ready runtime state while preserving datasets:

```bash
PYTHONPATH=src python3 scripts/reset_lab.py
```

Advance one candidate through the loop with a deterministic simulated outcome:

```bash
PYTHONPATH=src python3 scripts/advance_loop.py cand_0002 \
  --finalize-outcome \
  --simulate-outcome
```

Run a candidate through an explicit backend interface with:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend simulated
```

Use the built-in repo-native science backend with:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Override it with a custom command backend only when you want to:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/example_command_backend.py"
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Or bridge candidate execution to Ubuntu over SSH while still pulling the result and raw logs back into the local workspace:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/remote_command_backend.py"
export HARNESS_LAB_REMOTE_HOST="bkawk.local"
export HARNESS_LAB_REMOTE_WORKSPACE_ROOT="/tmp/harness-lab"
export HARNESS_LAB_REMOTE_BACKEND_COMMAND="python3 /data/projects/harness-lab/scripts/example_command_backend.py"
export HARNESS_LAB_REMOTE_DATASET_PATH="/data/projects/harness-lab/artifacts/datasets/abc_boundary512"
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Refresh the backend profile the lab uses for `auto` runner selection with:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/example_command_backend.py"
PYTHONPATH=src python3 scripts/refresh_backend_profile.py
```

Refresh the hardware profile the lab will consider with:

```bash
PYTHONPATH=src python3 scripts/refresh_hardware.py
```

Bootstrap an ABC-backed source bundle into `harness-lab`:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 \
  --stl-archive /path/to/abc_stl.7z \
  --step-archive /path/to/abc_step.7z \
  --feat-archive /path/to/abc_feat.7z
```

If the canonical archives are already present under `artifacts/datasets/abc_raw_v1/archives/`, the same command can just reuse them:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 --reuse-existing
```

Build a prepared local dataset artifact from that source bundle:

```bash
PYTHONPATH=src python3 scripts/build_abc_dataset.py \
  abc_raw_v1 abc_boundary512 \
  --limit 512 \
  --val-count 64 \
  --num-points 2048
```

Or just ensure the prepared dataset is ready, reusing it if it already exists:

```bash
PYTHONPATH=src python3 scripts/ensure_abc_ready.py \
  abc_raw_v1 abc_boundary512
```

## Why Researchers May Care

Most “AI research agent” repos compress away the actual evidence.
`harness-lab` is trying the opposite approach:
- keep the candidate workspace first-class
- keep raw trace-adjacent structure visible
- keep source snapshots and parent diffs directly in each workspace
- keep diagnosis and outcome separate from proposal intent
- keep cross-run synthesis inspectable
- keep publication controlled rather than magical

The goal is not just autonomy at execution time.
The goal is a system that can slowly become a better research partner for mesh-to-parametric learning because its memory and judgments stay legible.

The starting point for that evolution is the genesis seed candidate.
From there, the lab should be able to keep stepping forward, leaving behind:

- candidate workspaces
- tracked status pages
- self-published structural commits

so the GitHub repo itself becomes the easiest place to watch its progress.

## Lineage

This project was informed by an earlier lab generation in `mesh-para`, but it is intentionally not a copy of that codebase.
It is a cleaner attempt to build the next research harness around first-class workspaces, diagnosis, synthesis, and controlled self-evolution.

## Remote

- `origin`: `git@github.com:bkawk/harness-lab.git`
