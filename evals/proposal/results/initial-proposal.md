# Preserve completed zero counts in tabletext CSV exports

Please investigate the reported loss of numeric zero in `tabletext.export_csv`
and, if reproduced, restore the documented value conversion while preserving
blank missing values. This proposal targets the reported baseline of tabletext
1.4.0 on Python 3.11+. It requests maintainer assessment; no package change or
issue submission has been made.

## Need and basis for the expectation

A warehouse reconciliation report exports location counts through `export_csv`.
A measured count of zero means the location has been counted and the count is
complete. A missing count means nobody has counted that location. The receiving
team uses the exported values to decide which locations need another visit. The
author reports that completed zero-count locations currently receive unnecessary
revisits because their CSV cells are blank.

That operational distinction belongs to this consumer. The expectation that zero
exports as `0` also follows from the supplied public package contract: `None`
becomes an empty cell, and every other value uses Python's `str(value)`. Empty
strings remain empty. `export_csv` uses the standard-library CSV writer with a
comma delimiter; quoting and row order are preserved. Headers are ordinary input
rows, and translation is outside the package.

## Evidence and its limits

The author supplied this operator-reported excerpt from a private incident
dashboard:

> Input: [[0, None, 2]]. CSV read-back: [['', '', '2']].

Under the documented contract, the expected CSV read-back is:

```python
[['0', '', '2']]
```

The excerpt transfers the relevant reported input and result; the dashboard is
unavailable to the recipient, and no other dashboard contents were inspected.
Neither the author nor this proposal's preparer independently reran the report.
The raw serialized CSV, exact runtime details beyond Python 3.11+, and original
operator procedure were not supplied. The public README provides the local check
below, but it has not been executed during proposal preparation. No implementation
was inspected.

The author suspects automatic delimiter detection. That is an untested hypothesis,
not an established cause; the documented export API specifies its delimiter. No
incident rate, lost shipments, timing measurements, last known working version,
or regression range is established. Other exporters have not been investigated.

## Requested outcome and boundaries

After CSV export and read-back, recipients must be able to distinguish a completed
zero count from an unmeasured count. Maintainer verification should establish:

- `[[0, None, 2]]` reads back as `[['0', '', '2']]`.
- `None` remains blank: another consumer deliberately uses it for an unmeasured
  value. Empty strings also remain empty.
- Other non-`None` values retain their documented `str(value)` representation;
  for example, `[[0, None, '', 2, False]]` should read back as
  `[['0', '', '', '2', 'False']]`. This is an acceptance example, not a test result.
- Normal CSV quoting for delimiters, quotes, and embedded newlines, along with row
  order, continues to work. Header rows retain their supplied English text.

Header localization is excluded by agreement. No change to the meaning of missing
values, broader exporter redesign, or investigation of other exporters is requested.

## Options and next verification

The suggested replacement of every empty exported cell with `0` cannot meet these
conditions: it would turn both missing values and intentional empty strings into
completed counts. The recommended approach is to reproduce the report, then make
the smallest correction needed to honor the existing conversion contract. A
specific implementation mechanism remains open until investigation establishes
the cause. If the report cannot be reproduced, recover the original runtime and
procedure details before deciding whether a package correction is warranted.

The supplied README offers this check from the directory containing `tabletext.py`,
using Python 3.11+ without installation or network access:

```bash
python3 -c 'import csv, io, tabletext; print(list(csv.reader(io.StringIO(tabletext.export_csv([[0, None, 2]])))))'
```

This command is a pending maintainer verification step, not evidence of an
executed reproduction. If reproduced, verify the preservation conditions above
against any proposed correction. Maintainer acceptance, cause, affected versions,
and any shared implementation impact remain unresolved.

## Source provenance

Only these two case inputs informed this proposal. Their local paths may require
sharing with a recipient; the consequential contract and incident excerpt are
included above so assessment does not depend on access to private material.

- Author context and reported incident:
  [author-notes.md](/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal/cases/author-notes.md).
- Supplied public contract and local check for tabletext 1.4.0:
  [README.md](/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/README.md).
