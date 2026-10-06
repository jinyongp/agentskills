# terse evaluation

## Cases

| Request | Expected behavior | Result |
| --- | --- | --- |
| Explain an operation with three independent conditions in terse mode. | Keep all three conditions while shortening each; state the answer first. | Parent instruction review only |
| Give a complete specification, tersely. | Complete the requested specification; do not cap it at a short conversational answer. | Parent instruction review only |
| Write a polite rejection email. | Return only the email; preserve its requested politeness rather than importing blunt chat tone. | Parent instruction review only |
| Finish an authorized change and report status. | Perform the change and checks; short wording does not replace the work. | Parent instruction review only |
| A destructive operation needs a go-ahead and has a material warning. | Keep the warning, flag the pending decision first, and place the blocking question last. | Parent instruction review only |
| Review code without requesting a communication style. | The description does not automatically turn normal review into terse mode. | Parent instruction review only |
| A pending decision has several essential conditions, with language guidance loaded. | Preserve them in readable opening prose and produce one result; a single-sentence rule does not govern completeness. | Parent instruction review only |

## Validation and limits

Evaluation date: 2026-10-06 (Asia/Seoul), current Codex session; model version
not recorded. Cases above review the instructions, not independently generated
model responses. Automatic selection, long-session compliance, comprehension,
and token savings remain unmeasured. Upstream benchmark results do not establish
the behavior of this renamed and condensed adaptation.

Body length: 2794 characters, measured after frontmatter removal.
The 4,000-character body limit is an input policy, not a fixed response-size cap.
Long answers retain essential information; scripted paging is not applicable to
this instruction-only skill. No runtime helper, shared skill, or new dependency
is required. No tests that match instruction wording were added.

Full repository verification passed: 22 skills validated, 67 existing tests passed,
and CLI fixture smoke checks passed. Creator format validation and actual selective
installation passed. SKILL.md, NOTICE.md, and the complete upstream AGPL license
matched the installed copies byte for byte; the license also matched upstream.

Context review revision (2026-10-06): full verification of 44 skills and 76 existing
tests passed. Creator validation and selective installation passed; all three files
matched, local links resolved, and the AGPL license stayed unchanged.
