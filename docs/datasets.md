# Datasets

`harness-lab` should treat data provenance and dataset build reproducibility as part of the research harness.

The right default is:

- do not commit raw training data to git
- do not silently depend on a sibling repo path
- do record where the data came from
- do make attachment or fetching part of this repo's workflow
- prefer direct ABC bootstrap over any sibling-repo shortcut
- do build prepared local datasets inside this repo

## Current Approach

The repo now keeps a dataset registry at:

```text
artifacts/memory/datasets.json
```

and can attach existing local datasets under:

```text
artifacts/datasets/
```

The preferred bootstrap path is now:

- stage or download the three ABC source archives into `harness-lab`
- record a manifest and checksums
- register that dataset source in `artifacts/memory/datasets.json`
- build a prepared local dataset artifact from that source bundle

The important UX is:

- everyone uses the same bootstrap command
- if the archives are already present locally, bootstrap reuses them
- if they are not present, bootstrap can fetch or stage them

For us locally, that means we can seed the canonical archive location once from already-downloaded files and skip the wait without changing the public workflow.

## Why This Matters

For mesh-to-parametric learning, the dataset is part of the experiment definition:

- raw mesh source
- preprocessing variant
- split policy
- cache provenance

If that context is missing, the lab cannot reason well about its own results.

The loop and execution planner now consult this registry directly:

- proposals can carry a selected `dataset_id`
- execution plans surface dataset context
- runners can refuse to proceed if an expected dataset is not ready
- proposal drafting now only auto-selects locally registered `abc` datasets
- proposal drafting only auto-selects datasets with `kind=prepared`

## Initial CLI

Register any dataset:

```bash
PYTHONPATH=src python3 scripts/register_dataset.py abc_boundary512 \
  --kind prepared \
  --source local \
  --local-path /path/to/dataset
```

Bootstrap an ABC-backed dataset source directly into this repo:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 \
  --stl-url https://example.com/abc_stl.7z \
  --step-url https://example.com/abc_step.7z \
  --feat-url https://example.com/abc_feat.7z
```

You can also stage already-downloaded ABC archives into the canonical local location:

```bash
PYTHONPATH=src python3 scripts/seed_local_abc_archives.py abc_raw_v1 \
  --stl-archive /path/to/abc_stl.7z \
  --step-archive /path/to/abc_step.7z \
  --feat-archive /path/to/abc_feat.7z
```

Then reuse those local canonical archives with the normal bootstrap command:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 --reuse-existing
```

You can also bootstrap directly from already-downloaded archives in one shot:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 \
  --stl-archive /path/to/abc_stl.7z \
  --step-archive /path/to/abc_step.7z \
  --feat-archive /path/to/abc_feat.7z
```

Build a prepared dataset artifact from a bootstrapped source bundle:

```bash
PYTHONPATH=src python3 scripts/build_abc_dataset.py \
  abc_raw_v1 abc_boundary512 \
  --limit 512 \
  --val-count 64 \
  --num-points 2048
```
