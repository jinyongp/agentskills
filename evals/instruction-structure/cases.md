# Representative task inputs

Both agents received the five requests below. The baseline agent was instructed to
read the named skills and needed bundled references using `git show HEAD:<path>`
at `db383f973b51a731d94f8d66a8ae50a79dfab624`. The candidate agent read the working
tree. Both were told to return the requested outputs and resource list, without
skill critique, edits, project execution, installs, or service calls.
Neither received evaluator expectations or the other output.

## 1. Proposal

Use `skills/workflow/proposal/SKILL.md`. Prepare an English proposal for the
maintainer of the fictional LedgerCSV 2.1 library, inline. Raw notes: inventory team
calls its import job 'silver-lantern'; deployment was moved to another office last
month. Recipient receives only your proposal. Library's supplied public contract:
each cell is exported without changing its text; quoted cells may contain commas.
Reported input `[["A, B", "0027"]]`, output parsed back as `[["A, B", "27"]]`;
expected `[["A, B", "0027"]]`. Team distinguishes identifiers with leading zeros;
losing them joins distinct stock items. A teammate suspects number inference, but
no implementation was inspected and no local reproduction was run. The private
incident page cannot be shared; the preceding input and results are the permitted
excerpt. The requirement is preserve identifiers while retaining normal CSV
quoting, not change delimiters. Ask maintainer to investigate the report; do not
assert a proven cause. No implementation/submission authorized.

## 2. Code review

Use `skills/workflow/code-review/SKILL.md`. Review only this supplied Python change,
with no repository/tool execution required. Public contract: `reserve(n, available)`
rejects nonpositive `n` and `n` greater than `available`; equality is valid.
Original: `if n <= 0 or n > available: raise ValueError(); return available - n`.
Changed: `if n <= 0 or n >= available: raise ValueError(); return available - n`.
Change at `allocator.py` line 8. Accepted scope excludes persistent reservations.
Return actionable findings with evidence, coverage limits. Do not edit.

The semicolon-separated text describes the supplied guard and following return;
this is a static change-review case, not a runnable Python fixture.

## 3. Git sync

Use `skills/git/git-sync/SKILL.md`. User requests 'push my current branch'. Supplied
facts from trusted inspection: branch `fix/date`; one local-only commit; remote
`origin` fetch and push URLs differ; push destination is not yet inspected; working
tree has an unrelated untracked note. Network credential fetch now failed once.
Explain your immediate next action using only these facts. Do not execute mutations
or network calls.

## 4. Korean notice

Use `skills/writing/korean-writing/SKILL.md`. Edit this Korean notice for clarity,
preserving meaning and register. Return notice only:

> 승인이 완료된 신청에 한하여 담당자가 영업일 기준 이틀 이내에 처리할 수 있습니다. 다만 장비 수급이 지연되는 경우에는 처리 시점이 변경될 수 있습니다.

## 5. Drawer animation

Use `skills/frontend/animate/SKILL.md`. User requests implementation guidance for
reversing a drawer animation mid-flight. Existing app uses CSS transitions,
keyboard-accessible dialog primitives, and `prefers-reduced-motion`. Drawer can
close and reopen rapidly. No runtime/browser is available and edits are not
authorized. Return a concise implementation recommendation and verification limits
grounded only in these facts.
