# Modifications from Original DPLM

This document tracks changes made to the original [bytedance/dplm](https://github.com/bytedance/dplm) repository for TCR scaling law experiments.

## Code Changes

| File | Description |
|------|-------------|
| `vendor/openfold/setup.py` | Added `OPENFOLD_CPU_ONLY` env var to skip CUDA kernel compilation |

## New Files Added

### Scripts
| File | Description |
|------|-------------|
| `scripts/scaling/inspect_tcr_data.py` | Inspect TCR repertoire pickle file |

### Configs
| File | Description |
|------|-------------|
| (none yet) | |

## Data
- TCR sequences from: `/mnt/disk11/user/xiaoyih1/data/tcr_data_all/data/tcr_repertoires_healthy_samples/tcr_repertoire_seqs.pkl`
- Sampling: 2M sequences with seed=9999
