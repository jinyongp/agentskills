Task 1 — Proposal

Please investigate a reported loss of leading zeros in LedgerCSV 2.1.

An inventory team reports the following round-trip result after exporting cells and parsing the CSV back:

```text
Input:    [["A, B", "0027"]]
Reported: [["A, B", "27"]]
Expected: [["A, B", "0027"]]
```

The supplied public contract states that each cell is exported without changing its text and that quoted cells may contain commas. The team uses leading zeros to distinguish stock identifiers; removing them can cause distinct stock items to be joined.

Please investigate whether this report can be reproduced and where the text changes. A teammate suspects number inference, but that remains a hypothesis: no implementation was inspected and no local reproduction was run. The raw CSV, exact export invocation, and parsing configuration are not available in the supplied evidence, so the responsible stage has not been established.

The example above is the permitted excerpt from a private incident record that cannot be shared. It supplies the reported input and results, rather than an independently verified reproduction.

The required outcome is to preserve identifier text, including leading zeros, while retaining ordinary CSV quoting for comma-containing cells. Changing delimiters would not address that requirement. Successful verification would reproduce the example through the relevant export and parse paths and return both `"A, B"` and `"0027"` unchanged. This proposal requests investigation; it does not prescribe an implementation.

Task 2 — Code review

- **[P2] Restore valid equality at `allocator.py:8`.** For positive `n == available`, such as `reserve(3, 3)`, the changed `n >= available` condition raises `ValueError`. The public contract permits equality, and the original implementation returned `0`. Restore the strict `n > available` comparison.

Coverage: static review of the supplied original and changed conditions against the supplied contract. No repository inspection or runtime checks were performed. Callers and tests were not supplied; persistent reservations are outside the accepted scope.

Task 3 — Git sync

My immediate next action would be a local, read-only inspection of the configured push destination, refspec, and outgoing commit for `fix/date`. The fetch and push URLs differ, so the fetch endpoint does not establish where a push would go.

I would report the credential-fetch failure and pause uploading, without repeatedly retrying it or presenting cached remote state as current. The one local-only commit does not establish the current state of the uninspected push destination. Preserve the unrelated untracked note. No push or other mutation has been performed.

Task 4 — Korean notice

담당자는 승인이 완료된 신청에 한해 영업일 기준 이틀 이내에 처리할 수 있습니다. 다만 장비 수급이 지연되면 처리 시점이 변경될 수 있습니다.

Task 5 — Drawer animation

Keep the existing CSS transitions and dialog primitives. Retarget the drawer’s transform when its desired open state changes so a reversal starts from its current visual position. Reuse existing timing tokens and transition only the intended properties.

Keep application state independent of animation completion. If the primitive retains the drawer during exit, ensure a stale completion cannot remove a drawer that has reopened. Handle cancelled transitions and zero-duration reduced-motion paths without relying solely on `transitionend`. Preserve the primitive’s focus, keyboard dismissal, and modal behavior; use an instant or reduced-travel alternative under `prefers-reduced-motion`.

Verify rapid close/reopen sequences, cancellation, unmounting, focus and Escape behavior, and preference changes during playback. These are implementation recommendations based only on the supplied facts; no source inspection, browser observation, edits, or performance verification was performed.

Baseline revision and resources read

Exact HEAD: `db383f973b51a731d94f8d66a8ae50a79dfab624`.

All resources were read using `git show HEAD:<path>`:

- `skills/workflow/proposal/SKILL.md`
- `skills/workflow/proposal/references/proposal-contract.md`
- `skills/workflow/proposal/references/reader-review.md`
- `skills/workflow/code-review/SKILL.md`
- `skills/workflow/code-review/references/focused-checks.md`
- `skills/git/git-sync/SKILL.md`
- `skills/writing/korean-writing/SKILL.md`
- `skills/writing/korean-writing/references/diagnosis.md`
- `skills/frontend/animate/SKILL.md`
- `skills/frontend/animate/references/interactions.md`
- `skills/frontend/animate/references/mechanics.md`
- `skills/frontend/animate/references/css.md`
