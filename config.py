from pathlib import Path

repository_dir = Path(__file__).resolve().parent

filterbank_file_path = Path('/path/to/B0531+21_59000_48386.fil')
segment_labels_path = repository_dir / 'segments_index_B0531+21_59000_48386.csv'
run_dir = repository_dir / 'runs' / 'punch_rfi_reproduction'
