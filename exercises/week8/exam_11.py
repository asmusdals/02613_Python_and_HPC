import sys

import pandas as pd


def total_precipitation(path, chunk_size):
    total = 0.0

    for chunk in pd.read_csv(path, chunksize=chunk_size):
        precip = chunk["parameterId"] == "precip_past10min"
        total += chunk.loc[precip, "value"].sum()

    return total


def main():
    if len(sys.argv) != 3:
        print("Usage: python exam_11.py <csv-path> <chunk-size>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    chunk_size = int(sys.argv[2])

    print(total_precipitation(path, chunk_size))


if __name__ == "__main__":
    main()
