import sys
import pandas as pd

# Hent input fra command line
file_path = sys.argv[1]
chunk_size = int(sys.argv[2])

total_precip = 0.0

# Læs filen i chunks
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    total_precip += chunk.loc[chunk["parameterId"] == "precip_past10min", "value"].sum()

# Print resultatet
print(total_precip)