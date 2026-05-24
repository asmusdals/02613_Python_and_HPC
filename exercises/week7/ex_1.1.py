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
    df["created"] = pd.to_datetime(df["created"], format="ISO8601")
    df["observed"] = pd.to_datetime(df["observed"], format="ISO8601")

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
        print("Usage: python3 ex_1.1.py /path/to/2023_01.csv.zip")
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

    print("\n=== Exercise 1.4 ===")
    df_reduced = reduce_dmi_df(df2)
    print(f"Memory usage after reduction (bytes): {df_memsize(df_reduced)}")
    print(f"Memory usage after reduction (MB):    {df_memsize(df_reduced) / 1024**2:.2f}")

    print("\nColumn summary after reduction:")
    summarize_columns(df_reduced)    

if __name__ == "__main__":
    main()


# OUTPUT
# n-62-27-23(s224473) $ python3 ex_1.1.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip
# === Exercise 1.1 ===
# Unzip first + read_csv: 17.088 s
# Read zip directly:      14.542 s
# Fastest method: read zip directly with pandas

# === Exercise 1.2 ===
# DataFrame shape: (8142495, 7)
# Memory usage (bytes): 2144438374
# Memory usage (MB):    2045.10

# Column summary:
#           name    dtype   unique  size (MB)
# 0      coordsx  float64      224         62
# 1      coordsy  float64      219         62
# 2      created   object  8142495        652
# 3     observed   object    44640        597
# 4  parameterId   object       47        546
# 5    stationId    int64      247         62
# 6        value  float64    11532         62
# Total size: 2045.0958003997803 MB

# === Exercise 1.4 ===
# Memory usage after reduction (bytes): 268706914
# Memory usage after reduction (MB):    256.26

# Column summary after reduction:
#           name                dtype   unique  size (MB)
# 0      coordsx              float32      224         31
# 1      coordsy              float32      219         31
# 2      created  datetime64[ns, UTC]  8142495         62
# 3     observed  datetime64[ns, UTC]    44640         62
# 4  parameterId             category       47          7
# 5    stationId                int32      247         31
# 6        value              float32    11532         31
# Total size: 256.258882522583 MB
# (02613) ~/Documents/02613/week7