# brief evaluation

## Cases

| Request | Expected behavior | Result |
| --- | --- | --- |
| 20 applicants, 5 screened, 2 interviews booked, no offer; summarize hiring. | Preserve counts and distinguish booked interviews from completed interviews. | Parent instruction review only |
| A checklist has an unchecked deployment item but no deployment evidence. | Mark deployment unknown rather than asserting not started. | Parent instruction review only |
| All authorized work is complete; give a brief. | Report completion with evidence; invent no next choice or blocker. | Parent instruction review only |
| Explain why a release failed in detail. | Provide causal reasoning and conditions; adapt the board format when needed. | Parent instruction review only |
| Write the standup message itself. | Return only the requested message. | Parent instruction review only |
| Create a packet for another agent to resume implementation. | A status brief alone is not a substitute for necessary continuation context. | Parent instruction review only |
| Write a formal narrative update with language guidance also loaded. | Return one update in the requested voice; choose prose without compulsory emoji or a checklist. | Parent instruction review only |

## Validation and limits

Evaluation date: 2026-10-06 (Asia/Seoul), current Codex session; model version
not recorded. Cases above review the instructions, not independently generated
model responses. Automatic selection, long-session compliance, comprehension,
and token savings remain unmeasured. Upstream benchmark results do not establish
the behavior of this renamed and condensed adaptation.

Body length: 2526 characters, measured after frontmatter removal.
The 4,000-character body limit is an input policy, not a fixed response-size cap.
Long answers retain essential information; scripted paging is not applicable to
this instruction-only skill. No runtime helper, shared skill, or new dependency
is required. No tests that match instruction wording were added.

Full repository verification passed: 23 skills validated, 67 existing tests passed,
and CLI fixture smoke checks passed. Creator format validation and actual selective
installation passed. SKILL.md, NOTICE.md, and the complete upstream AGPL license
matched the installed copies byte for byte; the license also matched upstream.

Context review revision (2026-10-06): 2,798 body characters. Full verification of
44 skills and 76 existing tests passed. Creator validation and selective installation
passed; all three files matched, local links resolved, and the AGPL license stayed unchanged.
