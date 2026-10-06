# Sum quantities

From this directory, use Python 3.11+ to sum a JSON array of nonnegative integers.
The command reads standard input and writes one JSON object to standard output.

```bash
printf '%s\n' '[2, 3, 0]' | python3 cli.py
```

Expected result:

```json
{"total": 5}
```

An empty array returns `{"total": 0}`. Negative numbers, booleans, non-integers,
non-array inputs, and invalid JSON fail with exit code 2 and an error on stderr.
Correct the input before retrying. No files or remote resources are changed.

These examples were executed on Linux with the Python versions recorded in
the evaluation report. Other shells and platforms were not exercised.
