# ABC Build

`harness-lab` now has a repo-native path from ABC source archives to a prepared local dataset artifact.

The intended shape is:

1. bootstrap an `abc_source` bundle into `artifacts/datasets/<source_dataset_id>/`
2. build a prepared dataset under `artifacts/datasets/<prepared_dataset_id>/`
3. register the prepared dataset in `artifacts/memory/datasets.json`
4. let proposal drafting and execution use that prepared dataset automatically

## Why This Matters

The lab should not stop at "source exists."

It needs a reproducible, local build step that turns:

- STL archive
- STEP archive
- features archive

into a prepared artifact with:

- matched subset manifest
- preprocessed per-object `.npz` files
- packed train/val shards
- metadata and build provenance

## Build Flow

Bootstrap the ABC source bundle:

```bash
PYTHONPATH=src python3 scripts/bootstrap_abc_dataset.py abc_raw_v1 \
  --stl-archive /path/to/abc_stl.7z \
  --step-archive /path/to/abc_step.7z \
  --feat-archive /path/to/abc_feat.7z
```

Build a prepared local dataset:

```bash
PYTHONPATH=src python3 scripts/build_abc_dataset.py \
  abc_raw_v1 abc_boundary512 \
  --limit 512 \
  --val-count 64 \
  --num-points 2048
```

Or use the higher-level entrypoint that reuses an existing prepared dataset if it is already present:

```bash
PYTHONPATH=src python3 scripts/ensure_abc_ready.py \
  abc_raw_v1 abc_boundary512
```

That writes a prepared dataset root like:

```text
artifacts/datasets/abc_boundary512/
```

with:

- `raw_subset/`
- `preprocessed/`
- `shards/`
- `build_manifest.json`

The lab auto-selects prepared `abc` datasets for execution. It does not auto-select raw source bundles.

`ensure_abc_ready.py` is the command the future autonomous loop should call. It gives the lab one stable step for:

- checking whether a prepared dataset already exists
- reusing it when possible
- rebuilding it when necessary
