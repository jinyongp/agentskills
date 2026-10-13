# Domain modeling evaluation

## Decision cases — 2026-10-13

Parent instruction review in Codex; model version not exposed. These cases assess
written decisions, not independent agent execution or measured effectiveness.

| Request / fixture | Expected decision | Review result |
| --- | --- | --- |
| Clarify whether customer, account and user mean the same thing | Probe ownership/lifecycle scenarios; distinguish concepts only where behavior differs | Procedure 2–5 supplies the distinction and scenario check |
| Ordering and billing define cancellation differently | Preserve contextual meanings; inspect consumers before proposing shared terminology | Context boundaries retained |
| User says partial cancellation is allowed; code cancels the whole order | Surface sources and resolve policy; implementation alone is not authority | Conflict remains explicit |
| Analyze terminology without editing | Return inline findings; create no glossary or code changes | Scope limits writes |
| Document settled terms in an existing guide | Reuse that destination; avoid a second glossary | Existing documentation takes precedence |
| Name a local variable, or read an established definition | No modeling interview or mandatory records | Routing boundary explicit |
| Cosmetic choice with no costly tradeoff | No ADR | All three decision-record conditions required |
| Large monorepo; relevant definitions unavailable | Inspect selected contexts and report unresolved coverage | Partial search cannot establish absence |

## Input budget and evidence

No inspection helper: repository searches supply targeted evidence. No measured
tool-output cap, large-input recovery, live documentation edits, or independent
selection result is claimed. Format, body budget, links and standalone packaging
are checked separately. No wording-matching test is added.
