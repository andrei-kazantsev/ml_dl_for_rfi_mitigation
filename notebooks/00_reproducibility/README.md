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

Before the first notebook, set `filterbank_file_path`, `segment_labels_path`,
and `output_dir` to existing server locations. Set `run_dir` in the second
notebook to the same directory as `output_dir`.

## Run order and checks

1. `01_dataset_creation/creating_dataset_from_filterbank_by_indexes.ipynb`
   - Build 256-sample frequency-channel time series with labels and identity columns.
   - Check the source checksum and metadata/time-series row alignment.
2. `01_dataset_creation/subdataset_creation.ipynb`
   - Build the historical balanced subset.
   - Preserve `sample_index`, the 16 features, and labels in subset metadata.
   - Use `sample_index` to map each subset row to the full channel-time-series array.
   - Check 10,000 `NBRFI` and 10,000 `None` rows, source-row alignment, and
     split sizes 16,000/2,000/2,000.
3. `02_feature_exploration/stat_analysis.ipynb`
   - Inspect the 16 statistical features before fitting a tabular model.
4. `03_model_training/1_cnn_model.ipynb`
   - Train the historical 1D CNN with per-channel maximum normalization.
   - Require CUDA and read each input from the full array by `sample_index`.
   - Check the recorded model shape, validation-selected checkpoint, and test
     metrics. Stop after the test metric; the following cells are retained
     legacy diagnostics.
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
- The subset stage writes only subset metadata and split indices. It does not
  duplicate channel time series or binary target labels.
- PSRCHIVE S/N and the 2024 transfer test require other input observations.
  They are separate work and are not validated by this run order.
- The notebooks keep only headings and comments that state a purpose,
  invariant, or reason for a selected index. New notebook text uses ASD-STE100
  style.
