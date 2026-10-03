# Skill evaluations

Evaluate whether instructions produce the intended results separately from format validation.
When adding a skill, record inputs and expected results in `evals/<skill-name>/`.
Keep each skill's cases and results in its own folder.

| Skill | Evaluation record |
| --- | --- |
| git-commit | [Request scope, commit grouping, excluded changes](git-commit/README.md) |
| git-branch | [Branch operations and index/worktree preservation](git-branch/README.md) |
| git-sync | [Remote synchronization, divergence, tags, local work](git-sync/README.md) |
| git-conflict | [Merge, rebase, and cherry-pick conflict procedures](git-conflict/README.md) |
| git-pr | [PR scope, body preparation, and validation limits](git-pr/README.md) |
| handoff | [Missing context, targeted lookups, and work preservation](handoff/README.md) |

Cover at least these cases:

- Typical request: the skill applies and produces the requested result.
- Adjacent request: an out-of-scope request does not invoke the skill.
- Missing input or tool failure: request necessary information or explain the failure.
- Input budget: measure default and follow-up output sizes. Verify limits and omission
  reporting with large inputs, and recover required information page by page.

Record the request, expected result, agent and version, and actual result.
For skills with scripts, also verify normal and failure inputs.

## Authoring policy verification

On 2026-10-03, the Git skills were revised to start with summaries and use input budgets.
Repository limits are 300 characters for descriptions and 4,000 for SKILL.md bodies,
separate from the official format limits.
All 40 tests in `uv run check.py test` passed, covering accepted boundary values,
rejected overflows, preservation on generation failure, bounded inspection output,
and information recovery. These results do not measure automatic skill selection
or independent agent judgment.

The five Git skill bodies decreased from 23,042 characters at initial commit `6669a64`
to 12,429 characters, about 46%. This comparison excludes frontmatter and conditional references.
The final `uv run --locked check.py`, individual installation and execution of the inspection
helper, local documentation links, and per-skill MIT notices all passed verification.
