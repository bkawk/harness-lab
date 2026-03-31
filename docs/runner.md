# Runner

`harness-lab` now has an explicit runner boundary.

That matters because the loop should not care whether a candidate is evaluated by:

- a lightweight simulator
- a local benchmark harness
- a remote training job

The loop can just ask for a backend.

## Initial Backends

- `simulated`
- `command`

The simulated backend is still useful for dry runs, but the interface now also supports a repo-native command backend.
By default, the command backend is:

```bash
python3 scripts/repo_command_backend.py
```

That backend now prefers a real internal science path:

- load prepared ABC shards from `HARNESS_LAB_DATASET_PATH`
- train a compact point model for a realistic bounded wall-clock budget
- score a benchmark slice and an audit slice
- write first-class training metrics under `traces/`

By default, the supervisor exports `HARNESS_LAB_SCIENCE_TIME_BUDGET_SECONDS=600`, so real science runs use a `10` minute wall-clock budget unless you override it.

If a machine does not have the science stack available, it can still fall back cleanly instead of leaving the lab without any backend at all.

So a fresh clone already has a backend to work with, without relying on any sibling repo. `HARNESS_LAB_BACKEND_COMMAND` can override that default, and the lab writes `artifacts/memory/backend_profile.json` so policy can automatically prefer the real backend path.

Even with the simulated backend, the runner now writes first-class trace artifacts:

- `traces/run.json`
- `traces/runner_stdout.log`
- `traces/runner_stderr.log`

For command backends, the runner also writes:

- `traces/live_command.json`

That file is refreshed while the backend is still running, so the lab can observe liveness and finish as soon as the command actually exits instead of treating the whole run as one blind wait.

That means the candidate workspace already preserves command-level execution evidence rather than only a structured outcome summary.

## Command Backend Contract

Out of the box, just run:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Set a custom command backend only if you want to override the repo-native default:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/example_command_backend.py"
```

Refresh backend readiness explicitly with:

```bash
PYTHONPATH=src python3 scripts/refresh_backend_profile.py
```

Then run:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

The command backend receives these environment variables:

- `HARNESS_LAB_REPO_DIR`
- `HARNESS_LAB_CANDIDATES_DIR`
- `HARNESS_LAB_CANDIDATE_ID`
- `HARNESS_LAB_CANDIDATE_DIR`
- `HARNESS_LAB_PLAN_PATH`
- `HARNESS_LAB_OUTCOME_PATH`
- `HARNESS_LAB_RESULT_PATH`
- `HARNESS_LAB_TRACE_DIR`
- `HARNESS_LAB_DATASET_ID`
- `HARNESS_LAB_DATASET_PATH`
- `HARNESS_LAB_HARDWARE_ENVIRONMENT`
- `HARNESS_LAB_HOSTNAME`

The runner itself can be tuned with:

- `HARNESS_LAB_RUNNER_POLL_SECONDS`

The backend command must write JSON to `HARNESS_LAB_RESULT_PATH` with:

- `outcome_label`
- `benchmark_summary`
- `audit_summary`

And it may also include:

- `benchmark_score`
- `audit_score`
- `observed_failure_modes`
- `evidence`

That result is then ingested into `outcome/result.json`, while raw stdout/stderr and the backend result file are preserved under `traces/`.

## Initial CLI

Run a candidate with the simulated backend:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend simulated
```

Run a candidate with the built-in repo-native command backend:

```bash
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Run a candidate with a custom external command backend:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/example_command_backend.py"
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

Bridge the same contract to a remote Ubuntu host with:

```bash
export HARNESS_LAB_BACKEND_COMMAND="python3 scripts/remote_command_backend.py"
export HARNESS_LAB_REMOTE_HOST="bkawk.local"
export HARNESS_LAB_REMOTE_WORKSPACE_ROOT="/tmp/harness-lab"
export HARNESS_LAB_REMOTE_BACKEND_COMMAND="python3 /data/projects/harness-lab/scripts/repo_command_backend.py"
export HARNESS_LAB_REMOTE_DATASET_PATH="/data/projects/harness-lab/artifacts/datasets/abc_boundary512"
PYTHONPATH=src python3 scripts/run_candidate.py cand_0002 --backend command
```

That remote adapter:

- copies `proposal.json`, diagnosis, and execution plan to a remote candidate workspace
- runs the remote command under those paths
- pulls back:
  - `backend_result.json`
  - `remote_stdout.log`
  - `remote_stderr.log`
  - `remote_backend.json`

So the local candidate workspace still ends up with a complete trace bundle even though the actual work happened on Ubuntu.

For testing or custom deployments, you can also override the transport binaries:

- `HARNESS_LAB_SSH_BIN`
- `HARNESS_LAB_SCP_BIN`
