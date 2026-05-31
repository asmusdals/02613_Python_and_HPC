import sys
import tempfile
import time
import zipfile
from pathlib import Path

import pandas as pd
import pyarrow.csv as csv


def pyarrow_load(path):
    """Load a CSV file with PyArrow and return a PyArrow table."""
    return csv.read_csv(path)


def pandas_load(path):
    """Load a CSV file with pandas and return a pandas DataFrame."""
    return pd.read_csv(path, low_memory=False)


def timed_load(load_function, path):
    start = time.perf_counter()
    data = load_function(path)
    elapsed = time.perf_counter() - start
    return data, elapsed


def extract_csv_from_zip(zip_path, output_dir):
    with zipfile.ZipFile(zip_path) as zf:
        csv_names = [name for name in zf.namelist() if name.endswith(".csv")]
        if not csv_names:
            raise FileNotFoundError("No CSV file found inside zip file.")

        zf.extract(csv_names[0], output_dir)
        return Path(output_dir) / csv_names[0]


def get_csv_path(path, tmpdir):
    path = Path(path)
    if path.suffix == ".zip":
        return extract_csv_from_zip(path, tmpdir)
    return path


def main():
    if len(sys.argv) != 2:
        print("Usage: python exam_21.py /path/to/2023_01.csv or 2023_01.csv.zip")
        sys.exit(1)

    input_path = sys.argv[1]

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = get_csv_path(input_path, tmpdir)

        print("=== Exercise 2.1: Reading DMI data with PyArrow ===")
        print(f"CSV path: {csv_path}")

        pandas_df, pandas_time = timed_load(pandas_load, csv_path)
        arrow_table, pyarrow_time = timed_load(pyarrow_load, csv_path)

        speedup = pandas_time / pyarrow_time

        print(f"Pandas read time:  {pandas_time:.3f} s")
        print(f"PyArrow read time: {pyarrow_time:.3f} s")
        print(f"Speedup:           {speedup:.2f}x")
        print()

        print(f"Pandas shape:      {pandas_df.shape}")
        print(f"PyArrow rows:      {arrow_table.num_rows}")
        print(f"PyArrow columns:   {arrow_table.num_columns}")
        print(f"Pandas memory:     {pandas_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"PyArrow size:      {arrow_table.nbytes / 1024**2:.2f} MB")
        print()

        print("PyArrow schema:")
        print(arrow_table.schema)


if __name__ == "__main__":
    main()



# === Exercise 2.1: Reading DMI data with PyArrow ===
# CSV path: /tmp/tmptweejf8n/2023_01.csv
# Pandas read time:  14.204 s
# PyArrow read time: 3.466 s
# Speedup:           4.10x

# Pandas shape:      (8142495, 7)
# PyArrow rows:      8142495
# PyArrow columns:   7
# Pandas memory:     2045.10 MB
# PyArrow size:      507.57 MB

# PyArrow schema:
# coordsx: double
# coordsy: double
# created: timestamp[ns, tz=UTC]
# observed: timestamp[s, tz=UTC]
# parameterId: string
# stationId: int64
# value: double
