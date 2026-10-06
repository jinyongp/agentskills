# Accessibility evaluation

## Cases

| Request | Expected decision | Parent review |
| --- | --- | --- |
| A control has an aria-label but is not keyboard operable | Exercise required behavior and identify the exclusion | Literal presence is insufficient |
| Review a roving-tabindex widget | Evaluate its focus and interaction pattern | Negative tabindex is not banned |
| Check 18px regular text at a 3.5:1 ratio | Treat as normal text, not 18pt large text | W3C units checked against primary source |
| A computed ratio is 4.499:1 | Fail an applicable 4.5:1 threshold despite displayed rounding | Unrounded classification explicit |
| Decorative borders or inactive labels have low contrast | Check criterion applicability and exceptions | No blanket contrast finding |
| A 24px target satisfies AA requirements; recommend 44px | Separate normative requirement from usability recommendation | No fabricated universal 44px AA rule |
| A photo-backed label passes one flat color pair | Check relevant composited background variations | Narrow calculation does not prove full contrast |
| An automated scan passes with no screen-reader testing | Disclose coverage and untested interaction | No full-conformance claim |
| Review only one component in a large site | Inspect relevant detail and limit findings to reviewed scope | Uninspected pages remain unverified |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decision rules through parent review, not independent agent
execution. Automatic selection, real-project effectiveness, and large-input
recovery remain unmeasured. No runtime helper or dependency is bundled; inspection
ceilings depend on project tools. No tests that pin instruction text were added.

Body: 3,679 characters excluding frontmatter. Full verification passed: 29 skills,
67 existing tests, and CLI fixture checks. Creator validation passed. Actual
selective installation with `skills@1.7.0` copied all four files byte-for-byte,
including the conditional criteria reference, without another skill. Upstream
MIT license comparison and local links passed.

Standards notes were checked against linked W3C explanations on 2026-10-06.
No independent browser or assistive-technology execution was performed.
