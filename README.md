## btable-py

A Python interface for the [BTable serialization format](https://github.com/framed-data/clj-btable/),
providing fast, compact binary serialization for large, sparse, labeled 2D numeric datasets ('binary tables').

A BTable is basically a binary representation of a sparse matrix on disk, and the format is inspired
by the [Compressed Row Storage](http://netlib.org/linalg/html_templates/node91.html) (CRS) format,
saving space by only storing the indices/values of nonzero cells. It is designed in a strictly
row-oriented format for efficient iteration, and is _not_ a library for matrix computation or
linear algebra.

Note that BTables are *not* a drop-in replacement for all datasets stored as e.g. CSV:
the increases in efficiency is proportional to the sparsity of the dataset.
For a pathological fully-nonzero dataset, the space occupied can be much larger than a CSV!

### Examples
```py
import btable

# Writing a table
labels = ["login", "view_item", "purchase"]
rows = [[5.0,3.0,1.0], [2.0,0.0,0.0], [0.0,0.0,0.0]]
btable.write("/path/to/my_table.btable", labels, rows)

# Reading a table
bt = btable.BTable("/path/to/my_table.btable")

print(bt.labels)

for row in bt.rows():
  # Process individual row...
  print(row[0:])
```
