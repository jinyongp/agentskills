# UI stress evaluation

## Relationship preservation — 2026-10-16

Revision: working-tree changes to `SKILL.md` and `references/cases.md`.
Evidence: parent instruction review in Codex; model version not exposed.
These are inspection cases, not executed browser fixtures. Earlier verification
below retains its original scope and date.

| Scenario | Expected decision | Parent review |
| --- | --- | --- |
| A search result omits an optional property | Remaining values retain their identities; no misleading reassociation | Missing-field case makes the semantic failure explicit |
| Translated setting labels wrap at a supported narrow width | Each label still identifies its value and control | Locale/width variation checks relationships beyond clipping |
| An order's action text changes with its state | Action remains tied to the correct order and differs from current state | Item/state/action association included in the inspection |
| A plan condition wraps away from its displayed price | Check whether the condition's applicability remains clear | Price/condition case covers the relationship |
| A compact metadata row or peer options survive content changes | Leave the valid structure intact | Healthy counterpart guards against separator and density rules |

No browser run, independent agent execution, or measured improvement is claimed.
Format/index checks (66 skills), 176 existing tests (one skipped), skills@1.7.0
installation fixtures, packed CLI checks, creator validation, and local links passed.
Actual Codex and Claude project installations retained all four ui-stress files
byte-for-byte and excluded evaluation records. Body: 3,528 characters.
See the [paired UI design record](../ui-design/README.md) for commands, environment,
resolved cache/dependency setup failures, and distribution-check details.

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Break a member list with long labels | Feed plausible fixture data through existing boundary | No markup edits to manufacture failures |
| Empty/one/page-size-plus-one list | Exercise meaningful collection states independently | Data and flow boundaries included |
| No schema limit found | State unknown acceptance limit | No unsupported unbounded-input claim |
| Screenshot shows truncated decorative text | Judge actual user access and contract | Truncation not automatically a defect |
| RTL supported by the product | Exercise mixed direction and action access | Localization scoped to requirements |
| Review only | Return evidence and suggestions | No compulsory fix or production mutation |
| Find a purely visual issue | Reuse preview evidence unless durable coverage pays off | No automatic regression-test accumulation |
| Missing browser | Separate source hypotheses from rendered failures | Evidence limits explicit |
| Huge application | Select surfaces/fields and disclose omissions | No full-code or data dump |
| Load-test an API | Outside UI resilience scope | Trigger distinguished |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Parent review checks written decisions, not independent execution. Actual UI failures,
fixture isolation, automatic invocation, and runtime fixes remain unmeasured.
No generic helper is bundled because schemas and preview boundaries differ by project;
reuse their bounded tooling. Output sizes and large-input recovery were not measured.
No permanent tests mirror wording or duplicate existing format checks.

Body: 3,474 characters. Full locked checks passed: 39 skills, 76 tests, CLI fixtures.
Creator validation, exact four-file selective installation, local links, saved-record
fragment, and upstream MIT comparison passed.
