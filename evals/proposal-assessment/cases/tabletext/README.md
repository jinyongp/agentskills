# tabletext 1.4.0

Fictional local evaluation package. Python 3.11+, standard library only.

Public contract:

- `export_csv(rows)` and `export_tsv(rows)` accept iterables of row values and return
  text, using the CSV standard-library writer with comma or tab delimiters.
- A `None` value becomes an empty cell. Other values use Python's `str(value)`.
- An empty string remains an empty cell. CSV quoting and row order are preserved.
- Header rows are ordinary input rows; header translation is outside this package.

The implementation is `tabletext.py`. No package installation or network is needed.
For a local check from this directory:

```bash
python3 -c 'import csv, io, tabletext; print(list(csv.reader(io.StringIO(tabletext.export_csv([[0, None, 2]])))))'
```
