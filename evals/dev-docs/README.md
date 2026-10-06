# Developer documentation evaluation

See [parent task execution](../task-execution/README.md) for an authored CLI guide
whose documented commands and success/failure behavior were actually executed.
That scoped result supplements the instruction review below.

## Decision cases

Parent instruction review on 2026-10-06 in the current Codex session; model version
not recorded. These cases assess the written decision rules, not independent agent
execution or automatic skill selection.

| Request or condition | Expected decision | Review result |
| --- | --- | --- |
| Small library needs a first-use README | Provide orientation and a working path; link deeper detail only where useful | Structure follows the task, not a mandatory four-part tree |
| Experienced user needs one troubleshooting command | Give relevant prerequisites and recovery | No unrelated beginner tutorial |
| Source mentions an undocumented private method | Verify public support before recommending it | Implementation is not an automatic public contract |
| Spec and runtime disagree | Identify version and conflict; document only supported claims | No invented agreement or silent product edit |
| Review only | Return supported findings | Files remain outside editing scope |
| Korean output with language guidance loaded | Use requested language and return one document | No English-only dependency |
| Example calls a paid remote write | Use authorized isolated execution or disclose unverified output | Writing permission is not live execution permission |
| Generated API pages are stale | Edit their source and inspect scoped regeneration | No hand-editing an unexplained generated artifact |
| Published page needs relocation | Inspect actual links and redirect support | Preserve navigation; report unverifiable redirects |
| Monorepo has thousands of docs and symbols | Select task-relevant headings and sections; report omissions and retrieve required detail | No whole-site dump or partial completeness claim |
| Build or authentication unavailable | Run available checks and retain exact gaps | A link/build pass is not command verification |
| Existing useful snippet checks cover the change | Reuse them | No wording-pinning tests or per-edit test quota |

## Input budget and evidence limits

No runtime helper is bundled: native documentation tools and selected source reads
are more appropriate than a universal parser. Default input is relevant paths,
headings, and public entrypoints; command output and generated references are fetched
only for selected examples. Large-input recovery and output sizes are not mechanically
measured by this skill. A new reducer, if needed in a target project, needs explicit
limits and large-input/failure verification.

References are conditional; both use original guidance with primary-source links.
No third-party manual is copied. Independent writing quality, actual product example
execution, publication, and multi-language reader evaluation remain unmeasured.

Packaging verification passed: 45 skills, 76 existing tests, and CLI fixtures.
Creator validation and actual selective installation with skills@1.7.0 passed;
all four bundled files matched byte-for-byte. MIT notice and local links passed.
Entrypoint body: 3,651 characters, excluding frontmatter.

## Main-path instruction review

Parent instruction review on 2026-10-07; model version not recorded. The following
paired cases inspect the revised rules for conflicting or overbroad decisions.
They are not independent writing executions, reader studies, or quality scores.
The packaging figures above describe the earlier verification run.

| Condition | Decision supported by the revised instructions | Parent review |
| --- | --- | --- |
| API-call example interrupted by object prototype construction | Keep the call and its result together; link independent mechanics | Main-path relevance test gives a concrete relocation decision |
| Prototype semantics change how the reader checks a response field | Keep the applicable field-access caveat beside that operation | Essential use conditions remain available |
| Page opens with internals before explaining how to generate an SDK | Open with the generation task and outcome; move rationale to its own section | Opening criterion exposes the missing takeaway |
| API reference opens with parameters and version applicability | Preserve lookup structure | No forced tutorial or first-success sequence |
| Basic generation shares a continuous sequence with CI and remote-reference variants | Keep basic setup through result together; label or link independent workflows | Separation follows reader tasks rather than page-length limits |
| Paid or destructive command has a warning before execution | Retain the warning before the affected step | First-success ordering preserves relevant safeguards |
| Example is intended to demonstrate several APIs working together | State the composition purpose and keep required integration | Example-purpose rule does not force one API per snippet |
| All commands compile but the example's purpose is buried | Report the specific obstructing passage, task, effect, and relocation | Correctness checks cannot substitute for readability review |

The entrypoint now routes prose and example reviews to the bundled structure
reference. Actual improvements in autonomous writing and reader comprehension
remain unmeasured; no permanent wording or layout assertions were added.

Revision verification: repository format/catalog validation passed for 49 skills;
skill-creator validation, routed reference paths, the canonical saved-record fragment,
and diff whitespace checks passed. Entrypoint body: 3,896 characters. Tests and CLI
installation were not rerun for these instruction-only changes.
