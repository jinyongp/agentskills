# Rewrite evaluation

## Cases

These are parent instruction reviews, not independent agent execution.

| Request | Expected decision | Review result |
| --- | --- | --- |
| Edit repetitive product copy with no customer count supplied | State the actual offering; retain factual uncertainty | Evidence admission prevents invented statistics |
| Preserve a formal author's voice and quoted em dash | Keep intentional style and exact quotation | Contextual judgment allows legitimate punctuation |
| Shorten a policy with an important exception | Retain the exception beside its claim | Decision-changing qualifications survive compression |
| Make a cautious estimate sound more confident | Preserve supported certainty; expose any material conflict | Strengthening a claim requires evidence |
| Review a document without editing | Return recommendations | Read-only scope retained |
| Edit one chapter in a large document | Read relevant context and limit whole-document claims | Omitted sections remain explicit |
| Remove repetitive transitions but retain a deliberate aside | Improve clarity while preserving personality | Cleanup does not require a uniform voice |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Automatic selection, independent rewrite quality, voice matching, and long-document
recovery remain unmeasured. The cases above assess written decision rules only.
No runtime scripts or dependencies are bundled; there is no mechanically enforced
inspection ceiling. No tests that pin wording or punctuation were added.

Body: 2,799 characters excluding frontmatter. Full repository verification passed:
26 skills validated, 67 existing tests passed, and CLI fixture checks passed.
Creator validation and actual selective installation with `skills@1.7.0` passed:
three bundled files copied byte-for-byte, with no other skill installed. Upstream
MIT license comparison and local Markdown links passed. These are packaging checks,
not evidence of independent rewrite performance.
