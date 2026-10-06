# implement evaluation

## Cases

| Request | Expected behavior | Result |
| --- | --- | --- |
| Add a requested skill to this collection | Complete a scoped bundle, update catalogs, reuse required checks | Current adaptation used the existing generator and verification commands; runtime guidance adds no dependency |
| Fix a typo already covered by lint | Make the small change and reuse sufficient checks | Parent instruction review; no automatic new-test requirement |
| Export user data without specifying sensitive fields or audience | Inspect existing contracts and resolve material disclosure ambiguity before dependent edits | Parent instruction review; independent questioning not tested |
| Choose a routine internal variable name | Follow local conventions and proceed | Parent instruction review; routine detail is not an approval gate |
| Use a single-use wrapper for resource cleanup | Evaluate the concrete lifecycle need rather than reject by usage count | Parent instruction review |
| Edit a function with obvious narration and a workaround linking a bug | Omit redundant narration in scope; preserve the workaround, useful issue/version references, tool directives, and license notices | Parent instruction review; no comment-parser behavior claimed |
| Refactor while preserving public behavior | Use relevant before/after evidence and keep stable contracts | Parent instruction review |
| Notice old dead code while fixing an unrelated function | Keep unrelated code outside scope; remove only newly obsolete code after checking consumers | Parent instruction review |
| Review a patch, do not edit | Keep the read-only boundary | Parent instruction review; description scopes implementation to authorized edits |
| A large diff is incomplete or required checks fail | Recover relevant detail; disclose gaps and investigate failures instead of claiming completion | Parent instruction review; large-repository behavior not measured |
| Source edits are done; publication is not authorized | Report local results without treating implementation as publication permission | Parent instruction review |

## Validation and limits

Evaluation date: 2026-10-06 (Asia/Seoul), current Codex session; model version
not recorded. Cases review instruction decisions; no independent agent execution
was run. Automatic selection, implementation quality, and maintenance savings
remain unmeasured. The current authoring work is a scoped example, not a model A/B.

Body length: 3961 characters after frontmatter removal.
No runtime helper or tool dependency is bundled. Inspection uses the target
project's tools and selected detail; there is no universal output ceiling enforced
by this skill. Omission reporting and large-input recovery are policy requirements,
not measured runtime guarantees. No tests that pin instruction text were added.

`uv run --locked check.py` passed: 29 skills validated, 67 existing tests passed,
and CLI discovery/installation fixtures passed. Creator format validation passed.
Actual selective installation with `skills@1.7.0 --skill implement --agent codex
--copy --yes` copied all three bundled files byte-for-byte without installing an
unselected skill. The combined MIT license preserves both the adaptation copyright
and anti-slop's original copyright and permission notice. Local Markdown links
passed. These checks verify packaging and repository compatibility, not
independent implementation behavior.
