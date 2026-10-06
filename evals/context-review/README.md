# Repository-wide context and decision review

Reviewed on 2026-10-06 in the current Codex session; model version not recorded.
Inventory snapshot: commit `ef1603e` with 44 skills. Later additions have their own
evaluation records; this historical review does not cover those additions.
Scope: all 44 installed-skill entrypoints, all 19 bundled references, all seven
runtime helpers, and relevant evaluation and authoring guidance. This is a parent
instruction and source review, supplemented by packaging and existing runtime checks.
It does not measure independent agent selection or task execution for every skill.

## Criteria

- Preserve task intent, requested language, genre, voice, qualifications, and authorization.
- Keep standalone installation complete; apply accompanying guidance within one task.
- Use context and evidence for decisions. Distinguish contracts from heuristics and examples.
- Load only relevant evidence; preserve exact paths and recoverable omissions.
- Reuse useful tests and static checks. Add lasting coverage only for meaningful gaps.
- Distinguish inspection, observed behavior, scripted checks, and independent judgments.

## Corrections

| Area | Supported concern | Result |
| --- | --- | --- |
| brief | A checklist and emoji notation were imposed on updates | Form follows the destination; status remains factual and explicit |
| clear, terse | A single opening sentence or paragraph count could control delivery | Essential qualifications determine readable opening prose; combination yields one result |
| handoff | An English-only packet could override the task's working language | Requested or established language governs; identifiers and quotations stay exact |
| verify | Every bug appeared to require an additional edge case | Reuse adequate coverage; add a case for a distinct meaningful gap |
| code-review | Test changes lacked explicit review criteria for brittle or redundant protection | Check expectations, gaps, real boundaries, and concrete maintenance or policy effects |
| git-commit | The trigger omitted committing; imperative grammar was unconditional | Explicit commit trigger and repository-governed message style |
| Git inspection helpers | Worktree/diff inspection ran configured filesystem-monitor hooks | Disable fsmonitor per inspection query; preserve repository configuration and actual commit hooks |

The fsmonitor issue was reproduced in the existing read-only and external-driver
fixtures: both failed because marker files were created before the correction.
The corrected helpers pass those same fixtures. Existing tests were extended;
no separate test suite or instruction-wording assertions were added.

## Per-skill review

Retained means no further instruction correction was supported in this review;
it does not certify every possible runtime or agent behavior. Changed rows name
the correction above. Platform constants and inspection limits remain where they
express standards or concrete output contracts rather than quality quotas.

| Skill | Decision boundary reviewed | Disposition |
| --- | --- | --- |
| accessibility | Selected standard, applicability, exceptions, actual keyboard and contrast evidence | Retained |
| animate | Project tools, contextual timing, interruption, reduced motion, usable alternatives | Retained |
| animate-native | Installed runtime, gesture ownership, keyboard, device evidence, optional haptics | Retained |
| animation-audit | Heuristic inventory, scan and output paging, skips, evidence-backed plans | Retained |
| animation-debug | Reproduced symptom, discriminating probes, diagnosis versus authorized fixes | Retained |
| animation-opportunities | Demonstrated benefit, instant alternatives, empty recommendation set | Retained |
| animation-performance | Matched measured runs, frame pacing, noise, limited device/build claims | Retained |
| animation-review | Selected motion, contextual findings, source versus runtime evidence | Retained |
| animation-vocabulary | Observable effects, ambiguity, aliases, naming without implementation | Retained |
| mobile-web | Actual browser symptoms, input alternatives, scoped viewport and keyboard handling | Retained |
| prototype | Requested alternatives, comparable states, selection and authorized integration | Retained |
| responsive | Content-driven breakpoints, preserved information, intentional scrolling | Retained |
| ui-design | Product identity, honest content, functional controls, contextual aesthetics | Retained |
| ui-library | Concrete capability gap, current primary evidence, project tool precedence | Retained |
| ui-stress | Plausible supported extremes, observed failures, disposable fixtures, sufficient coverage | Retained |
| git-branch | Verified refs and start point, existing work, worktree occupancy, scoped deletion | Retained |
| git-commit | Requested action, excluded staging, message conventions, bounded read-only inspection | Changed |
| git-conflict | Both intended behaviors, rebase stage meanings, unrelated staging, continuation scope | Retained |
| git-pr | Draft versus publication, exact published head, templates, readback and retry limits | Retained |
| git-sync | Direction and exact destination, fresh versus cached refs, integration and force scope | Retained |
| git-worktree | Exact registry paths, local and ignored data, locks, ownership and lifecycle | Retained |
| benchmark | Required result equivalence, matched workloads, sampling, noise and measurement scope | Retained |
| code-review | Introduced defects, independent expectations, test maintenance costs, read-only helpers | Changed |
| debug | Reproduction, hypotheses, smallest authorized correction, meaningful regression coverage | Retained |
| handoff | Unrecoverable intent, targeted lookups, historical evidence, working language | Changed |
| implement | Material ambiguity, simple boundaries, scoped changes, proportionate checks | Retained |
| plan | Current decisions, dependencies, observable completion, pending evidence | Retained |
| survey | Inert manifests, bounded selected-directory inspection, commands as data | Retained |
| test | Independently justified contracts, reuse, stable boundaries and maintenance cost | Retained |
| test-contract | Real consumer/provider expectations, allowed variability, verified conformance | Retained |
| test-e2e | Actual user entrypoint, isolated state, meaningful completion and substitution limits | Retained |
| test-integration | Real tested boundary, consuming outcome, owned resources, distinct wiring evidence | Retained |
| test-maintenance | Concrete cost, retained failure protection, authorized and bounded pruning | Retained |
| test-property | Justified domain and invariant, shrinking, replay, exploration limits | Retained |
| test-unit | Stable behavior, independent expected values, lightweight real collaborators | Retained |
| verify | Useful checks, reuse, no automatic edge-case addition, execution evidence | Changed |
| brief | Factual status, suitable form, requested genre and composed output | Changed |
| clear | Attention-aware completeness, natural paragraphing, composed output | Changed |
| english-writing | Register, modal scope, contextual punctuation, meaningful passive voice | Retained |
| korean-writing | Korean information flow, speech level, contextual predicates and connectors | Retained |
| rewrite | Source fidelity, negation and obligation, review-only scope, language composition | Retained |
| summarize | Source attribution, uncertainty, actual action items and incomplete-source disclosure | Retained |
| terse | Essential qualifications, complete authorized work, deliverable voice and composed output | Changed |
| write | Evidence-based drafting, reader task, genre, language routing and publication scope | Retained |

## Validation and limits

Mechanical packaging checks cover individual selective installation, exact resource
copies, entrypoint limits, conditional local-reference resolution, the saved-record
fragment, evaluation presence, and unchanged license files. Full repository checks
exercise existing validation, runtime fixtures, and CLI discovery/installation.
Measured results:

- `uv run --locked check.py` passed: 44 skills, 76 existing tests, and CLI fixtures.
- Creator format validation passed for all 44 skills.
- All 44 actual selective installations with skills@1.7.0 copied every bundled file
  byte-for-byte into isolated temporary projects; each installed only the named skill.
- All skill-local references resolved inside their installed skill roots; repository
  documentation links resolved. Remote-link availability was not part of this check.
- Body lengths ranged from 2,411 to 3,961 characters, within the 4,000-character policy.
  Every skill retained the canonical saved-record fragment and an evaluation record.
- Root and category catalogs and this review table matched all 44 unique skill names.
- Every bundled license matched its pre-review committed bytes.
- The two extended hook fixtures failed before the helper correction and passed after it;
  existing large-input, paging, failure, timeout, and preservation checks also passed.

No live PR, deployment, production data, native device, assistive-technology session,
or benchmark campaign was exercised. External API compatibility and remote-link
availability were not rechecked across every documented platform. Existing references
direct the executing agent to installed-version and primary-source evidence when needed.
Standalone installation proves bundled-file completeness, not autonomous selection,
cross-skill cooperation, native-reader quality, or every task's runtime correctness.
