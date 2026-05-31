# Exercise 2.3

After loading the January 2023 DMI data with PyArrow, the PyArrow table size was:

```text
507.57 MB
```

After converting the PyArrow table to a pandas DataFrame, the DataFrame size was:

```text
919.13 MB
```

So the pandas DataFrame after conversion was larger than the original PyArrow table.

The sizes are different because PyArrow and pandas store data differently in memory. PyArrow uses a compact columnar memory format. This is especially efficient for typed columns such as numbers, timestamps, and strings.

When the table is converted to pandas, the data has to be represented using pandas and NumPy data structures. Some columns, especially string-like columns, can take more memory in pandas because pandas may store them as Python objects or less compact internal structures. Pandas also has extra overhead for indexes and column metadata.

Therefore, even though the two objects contain the same rows and columns, their memory layout is different. In this case, PyArrow stored the data more compactly than pandas.
