# Machine Learning for RFI Mitigation

This repository explores narrowband radio-frequency interference (RFI)
mitigation with a small 1D convolutional neural network (CNN) and classical
machine learning models. The CNN uses the time series of each frequency
channel. The classical models use statistical features calculated from the
same data.

The notebooks reproduce the training and evaluation workflow for an
observation of the Crab pulsar (B0531+21). The global test uses labelled
segments from the same observation that were not used for training.

## Notebooks

Run the notebooks in this order:

1. `01_create_training_subset.ipynb` — create the training data and split.
2. `02_cnn_training.ipynb` — train the CNN.
3. `03_statistical_models_training.ipynb` — train and compare the statistical models, then select one to save.
4. `04_model_inspection.ipynb` — inspect model predictions on spectrograms.
5. `05_global_test.ipynb` — evaluate the models on labelled segments not used for training.
6. `06_model_performance.ipynb` — measure CNN and statistical-model inference time.
7. `07_visualization.ipynb` — plot the training, evaluation, and performance results.

In notebook 03, set `selected_model_name` after inspecting the models. The
later notebooks use the saved model.

## Data and paths

Download `B0531+21_59000_48386.fil` from the [published dataset](https://doi.org/10.17617/3.HQYC8O).
The segment labels are included in this repository as
`segments_index_B0531+21_59000_48386.csv`.

Set the filterbank path in `config.py`. You can also change the paths to the
labels and output directory there. The first notebook creates the output
directory and saves the generated training data there. The other notebooks
use the same directory for models and results.

Some notebooks can overwrite existing results. Use a separate output directory
when you want to keep a previous run.

## Requirements

The reference environment uses Python 3.10.12.

| Package | Reference version | Use |
| --- | --- | --- |
| JupyterLab | 3.6.7 | Run the notebooks. |
| NumPy | 1.24.4 | Work with channel arrays and numerical calculations. |
| pandas | 2.0.3 | Work with labels, features, and result tables. |
| SciPy | 1.10.1 | Calculate the sigmoid function for model scores. |
| scikit-learn | 1.3.2 | Split data, train statistical models, and calculate metrics. |
| PyTorch | 2.2.2+cu121 | Train and run the CNN on CPU or GPU. |
| Matplotlib | 3.7.2 | Plot spectrograms, training curves, and results. |
| joblib | 1.6.0 | Save and load the selected statistical model. |
| tqdm | 4.66.1 | Show progress during processing and training. |
| your | 0.6.7 | Read filterbank data. |

The CNN can train on CPU or GPU. Notebook 06 requires a CUDA-enabled GPU for
the CPU/GPU performance comparison. Its timings cover model inference and the
threshold decision, not data loading or feature calculation.

## Contact

For questions, errors, or inaccuracies, contact
[akazantsev@mpifr-bonn.mpg.de](mailto:akazantsev@mpifr-bonn.mpg.de).
