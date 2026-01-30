# Modifications from Original DPLM

This document tracks changes made to the original [bytedance/dplm](https://github.com/bytedance/dplm) repository for TCR scaling law experiments.

## Code Changes

| File | Description |
|------|-------------|
| `vendor/openfold/setup.py` | Added `OPENFOLD_CPU_ONLY` env var to skip CUDA kernel compilation |
| `src/byprot/models/utils.py` | Modified `get_net()` to support custom architecture configs (for scaling experiments with arbitrary model sizes) |
| `src/byprot/datamodules/dataset/uniref_hf.py` | Modified `load_dataset_from_hf()` to support local datasets saved with `save_to_disk()` |

## New Files Added

### Scripts
| File | Description |
|------|-------------|
| `scripts/scaling/inspect_tcr_data.py` | Inspect TCR repertoire pickle file |
| `scripts/scaling/prepare_tcr_data.py` | Sample and prepare TCR data as HuggingFace dataset |

### Configs
| File | Description |
|------|-------------|
| `configs/datamodule/tcr.yaml` | Datamodule config for TCR data |
| `configs/experiment/scaling/tcr_smoke_test.yaml` | Smoke test config with small custom model |
| `configs/experiment/scaling/tcr_0.1m.yaml` | 0.1M parameter model config |

## Data
- TCR sequences from: `/mnt/disk11/user/xiaoyih1/data/tcr_data_all/data/tcr_repertoires_healthy_samples/tcr_repertoire_seqs.pkl`
- Sampling: 2M sequences with seed=9999
- Output: `data-bin/tcr_2m/` (HuggingFace dataset format)
