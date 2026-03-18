import sys
import time
import tempfile
import subprocess
from pathlib import Path

import pandas as pd


def df_memsize(df):
    return int(df.memory_usage(deep=True).sum())


def summarize_columns(df):
    print(pd.DataFrame([
        (
            c,
            df[c].dtype,
            len(df[c].unique()),
            df[c].memory_usage(deep=True) // (1024**2)
        ) for c in df.columns
    ], columns=['name', 'dtype', 'unique', 'size (MB)']))
    print('Total size:', df.memory_usage(deep=True).sum() / 1024**2, 'MB')


def load_unzip_then_read(zip_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        t0 = time.perf_counter()

        subprocess.run(
            ["unzip", "-o", "-q", zip_path, "-d", tmpdir],
            check=True
        )

        csv_files = list(Path(tmpdir).glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError("No CSV file found after unzip.")

        df = pd.read_csv(csv_files[0], low_memory=False)

        t1 = time.perf_counter()
        return df, t1 - t0


def load_zip_direct(zip_path):
    t0 = time.perf_counter()
    df = pd.read_csv(zip_path, compression="zip", low_memory=False)
    t1 = time.perf_counter()
    return df, t1 - t0


def reduce_dmi_df(df):
    df = df.copy()

    # Tider: object -> datetime
    df["created"] = pd.to_datetime(df["created"])
    df["observed"] = pd.to_datetime(df["observed"])

    # Få unikke værdier -> category
    df["parameterId"] = df["parameterId"].astype("category")

    # Taltyper gøres mindre
    df["coordsx"] = df["coordsx"].astype("float32")
    df["coordsy"] = df["coordsy"].astype("float32")
    df["value"] = df["value"].astype("float32")
    df["stationId"] = pd.to_numeric(df["stationId"], downcast="integer")

    return df


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 week7_ex12.py /path/to/2023_01.csv.zip")
        sys.exit(1)

    zip_path = sys.argv[1]

    print("=== Exercise 1.1 ===")
    df1, t_unzip = load_unzip_then_read(zip_path)
    print(f"Unzip first + read_csv: {t_unzip:.3f} s")

    df2, t_zip = load_zip_direct(zip_path)
    print(f"Read zip directly:      {t_zip:.3f} s")

    if t_unzip < t_zip:
        print("Fastest method: unzip first, then read CSV")
    else:
        print("Fastest method: read zip directly with pandas")

    print("\n=== Exercise 1.2 ===")
    print(f"DataFrame shape: {df2.shape}")
    print(f"Memory usage (bytes): {df_memsize(df2)}")
    print(f"Memory usage (MB):    {df_memsize(df2) / 1024**2:.2f}")

    print("\nColumn summary:")
    summarize_columns(df2)


    df3, t_zip = load_zip_direct(zip_path)
    print(f"Read zip directly:      {t_zip:.3f} s")

    print("\n=== Exercise 1.4 ===")
    df_reduced = reduce_dmi_df(df3)
    print(f"Memory usage after reduction (MB): {df_memsize(df_reduced) / 1024**2:.2f}")
    print("\nColumn summary after reduction:")
    summarize_columns(df_reduced)
    

if __name__ == "__main__":
    main()
