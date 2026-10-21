# Assessment: preserve completed zero counts in tabletext exports

**Disposition: adopt the corrective direction.** The reported CSV defect is reproduced, and the documented contract justifies a package correction. Refine the next-work scope to the shared value-conversion helper and regression checks for its two direct exporters. Do not replace blank cells with zero. This assessment makes no package changes and registers no tasks.

The current assessed proposal is `/tmp/agentskills-proposal-forward/author/revised-proposal.md` (SHA-256 `b70c9423588507851b91fbea38deccb1e5b9809319cecb9992cc9dea0344ec83`). It supersedes the earlier `/tmp/agentskills-proposal-forward/author/proposal.md`, which was read before the revision arrived. Conclusions and the plan below use the revised proposal. In particular, its uninvestigated TSV path is an evidence gap, not an agreed exclusion.

## Baseline, need, and independent evidence

The assessed target is the supplied fictional tabletext 1.4.0 package at `/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/`. Checks ran with Python 3.15.0, within the documented Python 3.11+ range. This verifies the supplied local baseline, not the original private incident environment or every supported Python version.

The consumer distinguishes a completed count of zero from an unmeasured count represented by `None`; collapsing both to blank prevents the receiving team from deciding which locations need another visit. The proposal reports unnecessary revisits, but their occurrence and frequency were not independently verified. Package responsibility follows independently from [README.md:7](/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/README.md:7): both export functions must render `None` as an empty cell and every other value with `str(value)`. Empty strings remain empty. Headers are ordinary rows, and localization is excluded.

The material claims separate as follows:

| Claim | Assessment |
| --- | --- |
| CSV loses zero for `[[0, None, 2]]` | Reproduced: raw text is `',,2\r\n'`, read-back is `[['', '', '2']]`; contract requires `[['0', '', '2']]`. |
| The report concerns tabletext 1.4.0 | Local `__version__` and README agree. Original runtime/configuration remain unavailable. |
| `None` and `''` must stay blank | Independently supported by the public contract and observed in both exporters. |
| Other non-`None` values must retain `str(value)` | Supported by the public contract; seven tested values violate it in each exporter. |
| Automatic delimiter detection causes the problem | Unsupported for this target. Source explicitly supplies comma/tab delimiters; conversion discards the values before writing. |
| Warehouse revisit impact | Author-reported context only; no private dashboard or original procedure was accessed. |

The confirmed cause is [tabletext.py:10](/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/tabletext.py:10), `return str(value or "")`. It substitutes an empty string for every falsy value. `_export` calls this helper for each cell before passing the row to the standard-library writer at [tabletext.py:17](/home/jinyongp/workspace/jinyongp/agentskills/evals/proposal-assessment/cases/tabletext/tabletext.py:17). CSV and TSV both call `_export` with explicit delimiters at lines 21–26. This establishes a conversion defect rather than a delimiter-selection defect.

## Related behavior and impact

The conversion matrix used `[0, None, '', 2, False, 0.0, [], (), {}, set(), True, -1, '0']`. Both exporters lose `0`, `False`, `0.0`, `[]`, `()`, `{}`, and `set()` to blank, instead of producing `'0'`, `'False'`, `'0.0'`, `'[]'`, `'()'`, `'{}'`, and `'set()'`. The other six values match the contract. The revised proposal's second acceptance example, `[[0, None, '']]`, was also checked directly: it produces `[['', '', '']]`, instead of `[['0', '', '']]`. The broader falsy-value cases follow from the public contract; they are not additional warehouse requirements.

**Necessary companion work:** honor the complete non-`None` rule in the shared helper, rather than special-casing numeric zero, and verify both direct exporters. TSV has the same demonstrated defect and the same documented obligation. This is bounded shared-path coverage, not a proposal to redesign exporters or investigate other packages.

The same truthiness operation also raises an avoidable exception for a printable object whose `__bool__` raises: both exports raise `RuntimeError` even though its `__str__` returns `'printable'`. Avoiding a truthiness test is part of restoring the stated conversion rule. This is a boundary of the same cause, not a separate feature or request for broad object-protocol testing.

Existing preservation checks passed for CSV and TSV: commas, tabs, quotes, LF, CR, CRLF, Unicode, supplied English headers, row order, generator rows, empty outer input, and a single empty row. `None` and empty strings stayed blank. These are baseline observations; no corrected implementation has been tested.

No related separate defect was established in the scoped module. Header translation, broader exporter redesign, and investigation beyond the two directly shared paths remain excluded. No performance improvement, incident rate, regression range, affected historical versions, or downstream usage inventory is established.

The corrective change would alter the serialized contents of previously blank falsy cells in both formats. A consumer relying on the current undocumented collapse could observe different output; no such dependency was demonstrated. Signatures, delimiters, quoting, supplied header text, and iteration order need no change. Previously exported blanks cannot reveal whether the original value was zero, `None`, or `''`; any recovery requires retained original data and re-export. There is no demonstrated need for a schema migration, service deployment, or new dependency.

## Options and decision

| Option | Outcome and cost |
| --- | --- |
| Keep behavior or document zero as blank | Preserves the defect and conflicts with the existing contract and justified consumer need. Decline. |
| Replace blank output cells with zero | Corrupts missing values and intentional empty strings; the original distinction is already lost. Decline. |
| Consumer converts known numeric zero counts to `'0'` first | Checked for the narrow sample: `[['0', None, '', 2]]` reads back as `[['0', '', '', '2']]`. Viable temporarily when original typed input is available; duplicates the package's promised conversion and leaves other falsy values untreated. More general non-`None` string conversion is possible by the same reasoning, but no consumer-wide adaptation was tested. |
| Correct shared conversion to `"" if value is None else str(value)` | Directly expresses the existing contract, fixes both direct paths, and removes the unnecessary truthiness call without changing writer behavior. Recommended mechanism, still unimplemented and unvalidated. |
| Special-case zero or add a CSV-only bypass | Leaves other documented non-`None` cases wrong or makes the two APIs inconsistent; more maintenance than correcting the shared cause. Decline. |

Validity and responsibility are established locally. The small shared-helper correction is feasible by source inspection and desirable to prevent silent information loss. Prioritize it as a bounded correctness fix; production severity and scheduling cannot be quantified from the supplied evidence. No additional incident evidence is needed to justify the local contract correction, though maintainers still own acceptance and release timing.

## Ordered next-work plan

1. **Capture contract-based regressions before editing.** In the project's existing test location, once available, add focused checks through the public CSV and TSV APIs for the revised proposal's two examples, `[[0, None, 2]]` and `[[0, None, '']]`. Include representative additional falsy values and a printable object that must not require truth testing. Expectations come from the README, not current output. Completion: checks demonstrate the documented conversion failures on this baseline.
2. **Correct only the shared conversion.** Distinguish `None` by identity and call `str(value)` for other values. Keep writer setup and delimiters unchanged. This depends on step 1; no redesign, localization, or post-export blank replacement is required. Completion: regression checks pass and both API paths use the correction.
3. **Verify preservation against the candidate.** Repeat read-back checks for blank `None`/`''`, normal non-falsy values, quoting of both delimiters, quotes and embedded line endings, supplied English headers, row order, iterable rows, and empty input/rows. Run existing relevant checks if a real package checkout provides them; assess its Python support matrix before claiming full compatibility. Completion: corrected conversion and preserved behavior pass together. Baseline-only passes in this assessment do not satisfy this step.
4. **Prepare a concise compatibility note before any authorized release.** State that falsy non-`None` values now retain their documented text in CSV and TSV. If an affected consumer still has original records, compare a representative corrected export with expected typed values and re-export affected data as needed. Observe completed zero counts and missing counts separately during consumer validation. Reverting the code restores the known loss, so use retained originals for recovery rather than blanket blank-to-zero edits. Release timing, historical scope, and original-data availability remain maintainer/consumer decisions.

No candidate patch, full package test suite, release, performance measurement, or private incident replay was performed. Implementation remains future work.

## Checked scope, inputs, and command evidence

Content inputs read:

- Installed skill: `/tmp/agentskills-proposal-forward/recipient/.agents/skills/proposal-assessment/SKILL.md` and its `references/proposal-contract.md`.
- Current received proposal: `/tmp/agentskills-proposal-forward/author/revised-proposal.md`. The earlier `/tmp/agentskills-proposal-forward/author/proposal.md` was also read and is superseded.
- Target inputs: the exact `README.md` and `tabletext.py` paths linked above, read in full.
- Required navigation/instructions: `/home/jinyongp/.codex/skills/index/SKILL.md`, `/home/jinyongp/.agents/skills/index/references/routes/review.md`, `/home/jinyongp/workspace/jinyongp/agentskills/skills/tooling/index/SKILL.md`, that repository index's `references/routes/review.md`, and applicable repository `AGENTS.md`, together with the supplied task instructions. The explicitly requested installed skill was used; no skill review was performed.

Author notes, evaluation READMEs above the target, other cases, prior results, and parent conversation were not read. No browsing, installation, repository writes, package edits, or external writes occurred. This assessment is the sole authored output.

Commands and results:

- `cat` read the identified instructions and inputs; `nl -ba tabletext.py` confirmed source locations (26 lines). `nl -ba README.md tabletext.py` was also used; its combined numbering is not used for source citations.
- `ls -ld /tmp/agentskills-proposal-forward/recipient /tmp/agentskills-proposal-forward/recipient/assessment.md` confirmed the destination directory exists and the assessment did not exist; exit 2 was only the absent output file.
- From the target directory, `bash -ic` ran `PYTHONDONTWRITEBYTECODE=1 python3 -c 'import csv, io, tabletext; text = tabletext.export_csv([[0, None, 2]]); print(repr(text)); print(list(csv.reader(io.StringIO(text))))'`. Exit 0; outputs `',,2\r\n'` and `[['', '', '2']]`.
- From the same directory, `bash -ic` ran a standard-library Python heredoc with `PYTHONDONTWRITEBYTECODE=1`. It printed Python/module versions; compared read-back values to `'' if value is None else str(value)` for the 13-value matrix in both formats; asserted all seven observed mismatches per format; verified the preservation cases described above; and captured the printable object's truth-test exception for both exporters. Exit 0: all observation-harness assertions passed. This means the baseline observations were confirmed; the documented conversion acceptance checks fail on the baseline.
- After receiving the revision, another `bash -ic` / `PYTHONDONTWRITEBYTECODE=1 python3` heredoc checked `[[0, None, '']]` and `[['0', None, '', 2]]` through CSV export/read-back. Exit 0: the revised acceptance case still loses zero, and the narrow known-zero string workaround produces `[['0', '', '', '2']]`. `sha256sum /tmp/agentskills-proposal-forward/author/revised-proposal.md` recorded the current proposal revision above.
- Interactive shell initialization printed no-job-control notices and an `fnm` multishell symlink permission error. Python still executed successfully; neither message affected the read-only checks, and no environment repair was attempted.
- `sha256sum README.md tabletext.py` identified the inspected baseline: README `79bec58c2eb0cc06daf62e3fc0161e3f96285a8311690f8ddeb3d2a7705af458`; module `ab063d87db37a7fa3966549758c6b2526e83da59c9cdc93a0afc4cc0bc71db5d`. The same hashes were confirmed after saving the initial assessment; target files remained unchanged.

The commands imported only the supplied local module and Python standard library. Bytecode generation was disabled. No test or implementation files were added to the package; broader repository checks that regenerate files were outside this read-only assessment.
