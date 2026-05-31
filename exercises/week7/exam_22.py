import sys
import tempfile
import time
import zipfile
from pathlib import Path

import pandas as pd
import pyarrow.csv as csv


def pyarrow_load(path):
    """Load a CSV file with PyArrow, convert it, and return a pandas DataFrame."""
    table = csv.read_csv(path)
    return table.to_pandas()


def pandas_load(path):
    """Load a CSV file directly with pandas and return a pandas DataFrame."""
    return pd.read_csv(path, low_memory=False)


def timed_load(load_function, path):
    start = time.perf_counter()
    data = load_function(path)
    elapsed = time.perf_counter() - start
    return data, elapsed


def timed_pyarrow_load_and_convert(path):
    start_read = time.perf_counter()
    table = csv.read_csv(path)
    read_time = time.perf_counter() - start_read

    start_convert = time.perf_counter()
    df = table.to_pandas()
    convert_time = time.perf_counter() - start_convert

    total_time = read_time + convert_time
    return df, read_time, convert_time, total_time


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
        print("Usage: python exam_22.py /path/to/2023_01.csv or 2023_01.csv.zip")
        sys.exit(1)

    input_path = sys.argv[1]

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = get_csv_path(input_path, tmpdir)

        print("=== Exercise 2.2: PyArrow to pandas ===")
        print(f"CSV path: {csv_path}")

        pandas_df, pandas_time = timed_load(pandas_load, csv_path)
        arrow_df, arrow_read_time, convert_time, arrow_total_time = (
            timed_pyarrow_load_and_convert(csv_path)
        )

        speedup = pandas_time / arrow_total_time

        print(f"Pandas read time:             {pandas_time:.3f} s")
        print(f"PyArrow read time:            {arrow_read_time:.3f} s")
        print(f"PyArrow to pandas time:       {convert_time:.3f} s")
        print(f"PyArrow + conversion time:    {arrow_total_time:.3f} s")
        print(f"Speedup vs pure pandas:       {speedup:.2f}x")

        if arrow_total_time < pandas_time:
            print("Conclusion: PyArrow + conversion is faster than pure pandas.")
        else:
            print("Conclusion: PyArrow + conversion is slower than pure pandas.")

        print()
        print(f"Pandas shape:                 {pandas_df.shape}")
        print(f"PyArrow-converted shape:      {arrow_df.shape}")
        print(
            "PyArrow-converted memory:     "
            f"{arrow_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        )


if __name__ == "__main__":
    main()


# === Exercise 2.2: PyArrow to pandas ===
# CSV path: /tmp/tmpwvhxq1gf/2023_01.csv
# Pandas read time:             11.461 s
# PyArrow read time:            3.037 s
# PyArrow to pandas time:       0.371 s
# PyArrow + conversion time:    3.408 s
# Speedup vs pure pandas:       3.36x
# Conclusion: PyArrow + conversion is faster than pure pandas.

# Pandas shape:                 (8142495, 7)
# PyArrow-converted shape:      (8142495, 7)
# PyArrow-converted memory:     919.13 MB

