import sys
import os
import pandas as pd

input_path = sys.argv[1]
output_dir = sys.argv[2]
chunk_size = 100000

os.makedirs(output_dir, exist_ok=True)

for i, chunk in enumerate(pd.read_csv(input_path, chunksize=chunk_size)):
    output_path = os.path.join(output_dir, f"part_{i:05d}.parquet")
    chunk.to_parquet(output_path, index=False)