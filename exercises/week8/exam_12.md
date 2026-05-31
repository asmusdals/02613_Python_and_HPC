# Exam 1.2

The measurements were run as a batch job with 1 core and a fixed CPU model:

```bash
#BSUB -n 1
#BSUB -R "select[model==XeonGold6126]"
```

The batch script uses:

```bash
/usr/bin/time -f "mem=%M KB runtime=%e s" python -u exam_11.py "$FILE" "$CHUNK_SIZE" 2>&1
```

Measured results:

| Chunk size | Result | Memory | Runtime |
| ---: | ---: | ---: | ---: |
| 1,000 | 12548.630000000054 | 130,980 KB | 28.78 s |
| 10,000 | 12548.629999999994 | 134,544 KB | 15.92 s |
| 100,000 | 12548.629999999997 | 192,296 KB | 15.06 s |
| 1,000,000 | 12548.630000000001 | 572,252 KB | 15.32 s |

All chunk sizes give the same precipitation total, apart from tiny floating point rounding differences. The smallest chunk size uses the least memory, but it is much slower because Pandas has to process many more chunks. Increasing the chunk size improves runtime until around 100,000 rows, where the runtime is best in this run. Going from 100,000 to 1,000,000 rows does not improve runtime, but it increases memory use substantially.

Compared to the non-chunked Pandas version from week 7, which used about 2045 MB for the full dataframe and took about 14.2 s just to read the file, chunking uses much less memory. The best chunked version takes 15.06 s, so it is only slightly slower than loading the full dataframe, but it is much more memory efficient and can run in a memory-constrained setting.
