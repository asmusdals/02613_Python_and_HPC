import argparse
import tempfile
import time
import zipfile
from pathlib import Path

import pandas as pd


def file_size_mb(path):
    return Path(path).stat().st_size / 1024**2


def timed(function, *args, **kwargs):
    start = time.perf_counter()
    result = function(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


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


def default_parquet_path(csv_path):
    return Path(csv_path).with_suffix(".parquet").name


def load_csv(path):
    return pd.read_csv(path, low_memory=False)


def save_parquet(df, path):
    df.to_parquet(path, index=False)


def save_csv(df, path):
    df.to_csv(path, index=False)


def read_parquet(path):
    return pd.read_parquet(path)


def csv_to_parquet(csv_path, parquet_path=None):
    if parquet_path is None:
        parquet_path = default_parquet_path(csv_path)

    df = load_csv(csv_path)
    save_parquet(df, parquet_path)
    return Path(parquet_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert DMI CSV data to Parquet and compare size/read/write times."
    )
    parser.add_argument("input_path", help="Path to a CSV file, or a .csv.zip file.")
    parser.add_argument(
        "--parquet-out",
        default=None,
        help="Output Parquet file. Defaults to <csv-name>.parquet in current folder.",
    )
    parser.add_argument(
        "--csv-out",
        default="exam_31_copy.csv",
        help="Temporary CSV output used for write benchmark.",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = get_csv_path(args.input_path, tmpdir)
        parquet_path = args.parquet_out or default_parquet_path(csv_path)

        print("=== Exercise 3.1: CSV to Parquet ===")
        print(f"CSV path:      {csv_path}")
        print(f"Parquet path:  {parquet_path}")

        df, csv_read_time = timed(load_csv, csv_path)
        _, parquet_write_time = timed(save_parquet, df, parquet_path)

        csv_size = file_size_mb(csv_path)
        parquet_size = file_size_mb(parquet_path)
        size_ratio = csv_size / parquet_size
        size_reduction = 100 * (1 - parquet_size / csv_size)

        print(f"CSV size:      {csv_size:.2f} MB")
        print(f"Parquet size:  {parquet_size:.2f} MB")
        print(f"Size ratio:    CSV is {size_ratio:.2f}x larger than Parquet")
        print(f"Reduction:     {size_reduction:.1f}% smaller than CSV")
        print()

        print("=== Exercise 3.2: Read/write timing ===")
        _, csv_write_time = timed(save_csv, df, args.csv_out)
        _, parquet_read_time = timed(read_parquet, parquet_path)
        _, csv_copy_read_time = timed(load_csv, args.csv_out)

        print(f"Read original CSV:       {csv_read_time:.3f} s")
        print(f"Write CSV copy:          {csv_write_time:.3f} s")
        print(f"Read CSV copy:           {csv_copy_read_time:.3f} s")
        print(f"Write Parquet:           {parquet_write_time:.3f} s")
        print(f"Read Parquet:            {parquet_read_time:.3f} s")
        print()

        print(
            "Read speedup:            "
            f"{csv_copy_read_time / parquet_read_time:.2f}x "
            "for Parquet compared with CSV"
        )
        print(
            "Write speedup:           "
            f"{csv_write_time / parquet_write_time:.2f}x "
            "for Parquet compared with CSV"
        )


if __name__ == "__main__":
    main()


# === Exercise 3.1: CSV to Parquet ===
# CSV path:      /tmp/tmptlbgci95/2023_01.csv
# Parquet path:  2023_01.parquet
# CSV size:      694.72 MB
# Parquet size:  102.66 MB
# Size ratio:    CSV is 6.77x larger than Parquet
# Reduction:     85.2% smaller than CSV

# === Exercise 3.2: Read/write timing ===
# Read original CSV:       13.948 s
# Write CSV copy:          35.958 s
# Read CSV copy:           15.856 s
# Write Parquet:           4.170 s
# Read Parquet:            4.273 s

# Read speedup:            3.71x for Parquet compared with CSV
# Write speedup:           8.62x for Parquet compared with CSV