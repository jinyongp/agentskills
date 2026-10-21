# Preserve zero counts in tabletext CSV exports

Please investigate a reported loss of the distinction between numeric zero and a missing value in `tabletext.export_csv`, and ensure CSV exports preserve that distinction under the documented contract. This proposal concerns tabletext 1.4.0 on Python 3.11+. It requests maintainer assessment; it does not establish a confirmed defect, a root cause, or an implementation choice.

## Why this matters

A warehouse reconciliation report exports rows through `export_csv`. In this report, a measured item count of zero means the count is complete. A missing count means nobody has counted that location. The receiving team uses that distinction to decide which locations need another visit. According to the author notes, blank CSV cells currently cause the team to revisit completed zero-count locations.

These meanings belong to the consuming workflow. The package's public contract separately supports the required representation: `None` becomes an empty cell, while other values use Python's `str(value)`. An empty string remains empty. On that basis, numeric zero is expected to export as `0`, independently of the warehouse's business rules.

## Reported evidence and expected result

An operator reported the following incident excerpt:

> Input: [[0, None, 2]]. CSV read-back: [['', '', '2']].

The incident dashboard is private and unavailable to the recipient. Only this supplied excerpt was available for preparing the proposal; the dashboard and its remaining contents were not inspected. The author has not independently rerun the report, and no reproduction was executed while preparing this proposal.

For the same input, the expected CSV read-back under the supplied public contract is:

```python
[['0', '', '2']]
```

The reported result appears inconsistent with that contract. Whether it reproduces on the stated baseline, or depends on the caller's setup, remains unverified. The notes do not provide the operator's exact invocation, runtime version beyond Python 3.11+, configuration, or intermediate data.

The supplied package README offers this local check from the package directory. It is included as a pending verification step, not as an executed result:

```bash
python3 -c 'import csv, io, tabletext; print(list(csv.reader(io.StringIO(tabletext.export_csv([[0, None, 2]])))))'
```

## Required outcome and preservation conditions

After reading the CSV export, the recipient must be able to distinguish a completed zero count from an unmeasured count. The following examples express the requested outcome; they are acceptance expectations, not test results:

| Input row | Expected CSV read-back row | Reason |
| --- | --- | --- |
| `[0, None, 2]` | `['0', '', '2']` | Preserve zero and the accepted missing-value representation. |
| `[0, None, '']` | `['0', '', '']` | Keep empty strings empty as well as keeping `None` blank. |

The blank representation of `None` was deliberately accepted because another consumer uses it to mean unmeasured. Changing that meaning would break an existing requirement. Empty strings must also remain empty. Preserve normal CSV quoting, row order, and the documented string conversion of other values; text containing commas or quotes should remain a single value after CSV read-back.

Headers remain ordinary input rows. The warehouse report's headers are English by agreement. Header localization is explicitly excluded from this proposal, consistent with the package contract placing header translation outside the package.

## Approach, alternatives, and open questions

The required outcome is preservation of the documented value distinctions. The maintainer should first reproduce the supplied example against tabletext 1.4.0, then determine whether the relevant behavior originates in the exporter, caller data preparation, or another part of the reported path. No implementation was inspected for this proposal.

The author's suspicion about automatic delimiter detection is an unverified causal hypothesis. The public documentation describes use of the standard-library CSV writer with a comma delimiter for CSV and a tab delimiter for TSV; it provides no evidence that automatic detection causes the report. The hypothesis should not determine a patch before investigation.

Replacing every empty exported cell with `0` is unsuitable: it would turn both missing counts and intentional empty strings into zero, violating the preservation conditions. A possible temporary caller workaround is to convert known numeric zero counts to the string `'0'` before export while retaining `None` and empty strings. Its effectiveness has not been checked, and it would add caller-side handling for behavior already promised by the package contract. Continuing to interpret every blank as requiring a visit preserves the current missing-value meaning but leaves the reported unnecessary visits unresolved.

Other exporters, including `export_tsv`, have not been investigated. That is an evidence gap, not an agreed exclusion or a claim that they are affected. Whether related value-conversion behavior needs broader verification should be determined after reproducing and locating the CSV issue. There is no established incident rate, timing measurement, regression range, last known working version, or evidence of lost shipments. No impact estimate or performance benefit is claimed.

## Evidence sources and next verification

This packet is self-contained for the reported scenario and requirements. Its only case sources were:

- Author context and the permitted incident excerpt: `/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal/cases/author-notes.md`.
- Supplied public contract and local check: `/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/README.md`, headed “tabletext 1.4.0”.

These local paths identify the supplied artifacts; recipient access to them is not assumed, so the consequential contract, example, and constraints are included above. No immutable source revision was supplied. The package implementation, actual runtime behavior, wider dashboard, and other exporters remain unchecked. The next useful evidence is the local example's result with an exact Python version and package baseline, followed by verification of the preservation conditions if a change is warranted. If the example does not reproduce, recover the operator's exact invocation and relevant sanitized input transformations before concluding that the report is resolved.
