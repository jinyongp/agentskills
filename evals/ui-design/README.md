# UI design evaluation

## Information relationships — 2026-10-16

Revision: working-tree changes to `SKILL.md` and `references/craft.md`.
Evidence: parent instruction review in Codex; model version not exposed.
The core rule applies before layout selection; the conditionally loaded reference
ships with the skill and supplies general examples. This file is maintainer evidence,
not installed runtime guidance. Earlier checks below apply to their dated revisions.

| Scenario | Expected decision | Parent review |
| --- | --- | --- |
| A plan picker separates promotional prices from billing and eligibility conditions | Associate material conditions with the applicable price; preserve supplied amounts and terms | Core claim/qualification rule and plan example cover the decision |
| Order rows style status and available actions alike, with an unclear action target | Distinguish state from action and identify the affected order | Core role rule and order example cover the decision |
| Account settings lose label/value pairing when stacked | Retain each value's association in visual and logical reading order | Label/value rule and source-order guidance cover the decision |
| Search results scatter comparable properties into separate decorative cards | Preserve comparison of the same property across results | Comparison example supports consistent labels, order, or columns without prescribing one layout |
| A compact author/date row is already clear | Retain useful metadata formatting, including a suitable separator | Explicit exception prevents punctuation bans and redundant labels |
| A dense comparison table or peer choices already serve the task | Preserve density and equal emphasis where appropriate | No required card conversion or invented priority |
| A brief includes an illustrative complaint unrelated to the product's content | Apply the failure principle without importing that example's fields into the UI | Reference separates examples from product requirements |

The cases span independent common tasks rather than noun substitutions in the
reported failure. This review establishes written decision coverage, not observed
generation quality, reader comprehension, or comparative skill benefit.

Executed verification in Linux/WSL with Node.js 26.10.0:

- `uv run --locked check.py validate --check-index`: 66 skill formats and index freshness passed.
- The test phase of `uv run --locked check.py`: 176 existing tests ran, one skipped; no failures.
- `uv run --locked check.py smoke`: skills@1.7.0 discovery and bundled-resource fixture passed.
- `uv run --locked check.py package`: packed CLI project/global lifecycle checks passed.
- Creator validation passed for both changed skills; all five local Markdown links resolved.
- Actual bundled CLI installation into a temporary project for Codex and Claude copied
  all five ui-design files and all four ui-stress files byte-for-byte. Only the selected
  skills and generated index were installed; evaluation records were absent.

The initial full run stopped at smoke because the default npm cache was read-only;
smoke and package passed with a temporary writable cache. Creator validation initially
lacked PyYAML; a temporary `uv run --with pyyaml` environment resolved it without a
repository dependency change. Final body sizes: ui-design 3,978 characters;
ui-stress 3,528. No tests pinning prose or CSS were added.

## Accepted-scope review — 2026-10-07

Parent instruction review; model version not recorded. Paired case:
An agreed preview needs truthful controls and labels; review does not turn it into a
live integration.
The revised rules recover agreed limits before judging gaps. This is not independent
agent execution. Repository checks and actual selective installation passed for this
revision; earlier results below retain their original scope.


## Local-skill-informed reinforcement — 2026-10-07

Parent rule review; model version not recorded. Paired cases:
A promotional page exposes offer, evidence, and commitment conditions; a task screen
prioritizes controls and current state rather than promotional hierarchy.
Instructions are original guidance informed by local workflow comparison, not a
copied manual. New references are conditional and bundled where needed. This checks
decision boundaries, not independent agent performance. Earlier results below
retain their original scope and date.

Revision verification passed: 49 skill formats/catalogs, 76 existing tests, CLI
fixtures, creator validation, and actual skills@1.7.0 installation of this skill
alone. Bundled files matched byte-for-byte; local links, the body budget, and the
saved-record convention passed. No independent agent or reader study was run.


## Decision clarity review — 2026-10-07

Parent instruction review; model version not recorded.
Paired case: Decoration competing with a task action prompts regrouping or emphasis
changes; peer choices can retain equal weight.
The revised rule states the evidence and resulting decision while preserving the
contrasting valid case. This is rule review, not independent task execution or a
measured quality improvement. Earlier verification results below are historical.

## Cases

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Build a screen from real product tasks | Let actions and content determine sections | Content-driven composition retained |
| Preserve a branded gradient and familiar cards | Keep techniques serving identity and usability | No blanket pattern bans |
| Add testimonials without real customers | Expose missing evidence or omit claims | Fabricated credibility rejected |
| Demonstrate a backend that is not connected | Label preview behavior and report limits | Prototype boundary explicit |
| Audit a functional but visually plain screen | Distinguish optional aesthetic improvements from defects | Minimal styling alone is not a finding |
| Edit one screen in a large application | Inspect relevant screens and report scope | Partial inspection remains partial |
| Review only with no runtime access | Return recommendations and disclose verification gap | No source edit or completeness claim |
| Refine a chosen non-Apple visual identity | Apply spatial/craft principles within the chosen style | No compulsory Apple appearance |
| Add translucent chrome | Judge hierarchy, changing-background legibility, modality, and fallback | Blur is not contrast or modal behavior |
| Keep a custom font and valid fixed spacing | Judge actual scripts, sizes, and enlargement | No system-font replacement or literal recipe |
| Immediate press feedback is requested | Preserve cancellation and activation semantics | Acknowledgement separated from commitment |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decision rules through parent review, not independent agent
execution. Automatic selection, real-project effectiveness, and large-input
recovery remain unmeasured. No runtime helper or dependency is bundled; inspection
ceilings depend on project tools. No tests that pin instruction text were added.

Initial version: 3,422 body characters excluding frontmatter. Full verification passed: 27 skills,
67 existing tests, and CLI fixture checks. Creator validation passed. Actual
selective installation with `skills@1.7.0` copied all three files byte-for-byte
without another skill. Upstream MIT license comparison and local links passed.
No rendered product or independent design task was evaluated.

The component-craft extension adds a conditional reference, with upstream MIT
copyrights for both Miqdad Badjuber and Emil Kowalski preserved. Current body:
3,590 characters. Full locked checks passed: 41 skills, 76 tests, CLI fixtures.
Creator validation, exact four-file selective installation, local links, saved-record
fragment, and both upstream copyrights plus the full permission notice passed.
Extension cases were assessed through parent instruction review; runtime effects
remain unmeasured.
