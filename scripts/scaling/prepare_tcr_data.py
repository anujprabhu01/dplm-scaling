#!/usr/bin/env python
"""Prepare TCR data for DPLM pretraining.

Samples sequences from the TCR repertoire pickle file and saves as a
HuggingFace dataset compatible with UniRefHFDataModule.

Usage:
    python scripts/scaling/prepare_tcr_data.py

Output:
    data-bin/tcr_2m/ - HuggingFace dataset with train/valid/test splits
"""

import pickle
from pathlib import Path

import pandas as pd
from datasets import Dataset, DatasetDict

# Configuration
SOURCE_PATH = '/mnt/disk11/user/xiaoyih1/data/tcr_data_all/data/tcr_repertoires_healthy_samples/tcr_repertoire_seqs.pkl'
OUTPUT_DIR = Path('data-bin/tcr_2m')
NUM_SAMPLES = 2_000_000
SEED = 9999

# Split ratios
TRAIN_RATIO = 0.98
VALID_RATIO = 0.01
TEST_RATIO = 0.01


def main():
    print(f"Loading source data: {SOURCE_PATH}")
    with open(SOURCE_PATH, 'rb') as f:
        df = pickle.load(f)

    print(f"Total sequences available: {len(df):,}")
    print(f"Sampling {NUM_SAMPLES:,} sequences with seed={SEED}")

    # Sample sequences
    sampled_df = df.sample(n=NUM_SAMPLES, random_state=SEED)
    sequences = sampled_df['tcr'].tolist()

    print(f"Sampled {len(sequences):,} sequences")
    print(f"Sequence length range: {min(len(s) for s in sequences)} - {max(len(s) for s in sequences)}")

    # Shuffle and split
    import random
    random.seed(SEED)
    random.shuffle(sequences)

    n_train = int(len(sequences) * TRAIN_RATIO)
    n_valid = int(len(sequences) * VALID_RATIO)

    train_seqs = sequences[:n_train]
    valid_seqs = sequences[n_train:n_train + n_valid]
    test_seqs = sequences[n_train + n_valid:]

    print(f"\nSplit sizes:")
    print(f"  Train: {len(train_seqs):,} ({len(train_seqs)/len(sequences)*100:.1f}%)")
    print(f"  Valid: {len(valid_seqs):,} ({len(valid_seqs)/len(sequences)*100:.1f}%)")
    print(f"  Test:  {len(test_seqs):,} ({len(test_seqs)/len(sequences)*100:.1f}%)")

    # Create HuggingFace datasets
    def create_dataset(seqs):
        return Dataset.from_dict({
            'seq': seqs,
            'length': [len(s) for s in seqs]
        })

    dataset_dict = DatasetDict({
        'train': create_dataset(train_seqs),
        'valid': create_dataset(valid_seqs),
        'test': create_dataset(test_seqs),
    })

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nSaving to: {OUTPUT_DIR}")
    dataset_dict.save_to_disk(str(OUTPUT_DIR))

    # Verify
    print("\nVerifying saved dataset...")
    from datasets import load_from_disk
    loaded = load_from_disk(str(OUTPUT_DIR))
    print(f"Loaded dataset: {loaded}")
    print(f"Train sample: {loaded['train'][0]}")

    print("\nDone!")


if __name__ == "__main__":
    main()
