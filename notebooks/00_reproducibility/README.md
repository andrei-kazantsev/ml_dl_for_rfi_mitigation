# PUNCH RFI Report Reproduction

This guide defines the server run order for the historical 2020 PUNCH RFI
report result. It uses existing stage notebooks. It does not replace the
legacy row-level split with the later group-split experiments.

## Source inputs

- Download `B0531+21_59000_48386.fil` from Edmond dataset
  `doi:10.17617/3.HQYC8O`.
- Verify MD5 `3cf053e6bc46911eada8d19bcb591bf5` before generation.
- Use the historical segment-label table and the existing RFI-block and
  channel-range annotations.

The segment-label table is required. The RFI annotations define positive
channels. The table defines the clean `None` segments. Do not create `None`
labels from all segments outside the RFI blocks.

Before the first notebook, set these paths to existing server files and an
existing output directory:

```bash
export RFIM_FILTERBANK_PATH=/path/to/B0531+21_59000_48386.fil
export RFIM_SEGMENT_LABELS_PATH=/path/to/segments_index_B0531+21_59000_48386.csv
export RFIM_OUTPUT_DIR=/path/to/existing/output_directory
```

## Run order and checks

1. `01_dataset_creation/creating_dataset_from_filterbank_by_indexes.ipynb`
   - Build 256-sample channel profiles with labels and identity columns.
   - Check the source checksum and the expected `(6823936, 256)` array shape.
2. `01_dataset_creation/subdataset_creation.ipynb`
   - Build the historical balanced subset.
   - Check 10,000 `NBRFI` and 10,000 `None` rows, with split sizes
     16,000/2,000/2,000.
3. `02_feature_exploration/stat_analysis.ipynb`
   - Inspect the 16 statistical features before fitting a tabular model.
4. `03_model_training/1_cnn_model.ipynb`
   - Train the historical 1D CNN with per-channel maximum normalization.
   - Check the recorded model shape, validation-selected checkpoint, and test
     metrics.
5. `03_model_training/classical_learning_stat.ipynb`
   - Train the six-model statistical ladder.
   - Check the validation-selected thresholds and the selected three-feature
     MLP artifact.
6. `04_full_file_tests/1d_cnn_global_test_rfi_cleaning_real_test.ipynb` and
   `04_full_file_tests/mlp_global_test_rfi_cleaning_real_test.ipynb`
   - Produce individual masks and historical global diagnostics.
   - Check that an individual validation spectrogram has no `sample_index` in
     train, validation, or test. Label row-excluded historical diagnostics
     separately from this complete-segment check.
7. `03_model_training/performance_comparison/`
   - Run CPU CNN, GPU CNN, selected MLP, model-only timing, and the final
     performance plot in the order documented in its local README.
   - Check p95 against the 26.2144-ms physical segment budget. The timing
     excludes I/O, feature creation, normalization, and host-to-device transfer.

## Boundaries

- The core release covers the 2020 training, same-observation diagnostics, and
  classifier-only timing result.
- PSRCHIVE S/N and the 2024 transfer test require other input observations.
  They are separate work and are not validated by this run order.
- The notebooks keep only headings and comments that state a purpose,
  invariant, or reason for a selected index. New notebook text uses ASD-STE100
  style.
