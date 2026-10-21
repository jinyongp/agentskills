"""Fictional export package used as raw input for skill evaluation."""

import csv
import io

__version__ = "1.4.0"


def cell_text(value):
    return str(value or "")


def _export(rows, delimiter):
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=delimiter)
    for row in rows:
        writer.writerow([cell_text(value) for value in row])
    return output.getvalue()


def export_csv(rows):
    return _export(rows, ",")


def export_tsv(rows):
    return _export(rows, "\t")
