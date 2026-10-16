# git-ignore evaluation

Evidence below separates scripted Git mechanics from untested agent judgment.

## Current coverage

- Revision: initial working-tree version, 2026-10-16 (Asia/Seoul).
- Evidence: instruction review and scripted replay in an isolated temporary repository.
- Sixteen replay cases passed. Replay verifies Git mechanics, not agent compliance.
- Independent agent execution and automatic selection were not evaluated.

## Cases

| Scenario and request | Expected result | Observed evidence |
| --- | --- | --- |
| Remove duplicate `*.log` rules | Preserve excluded logs and retained documentation | Before/after replay passed |
| Simplify `*.log`, `!keep.log`, `*.log` | Keep final rule when continued exclusion is intended | Replay proved removal changes behavior |
| Remove `logs/*.log` covered by `*.log` | Preserve exclusions and retained files | Before/after replay passed |
| Review identical `/build/` in root and nested files | Recognize different base directories | Replay verified both scopes and unaffected sibling |
| Nested `!keep.log` overrides ancestor `*.log` | Preserve nested inclusion | Replay passed |
| Keep one cache file | Keep its parent traversable | Replay confirmed `cache/` defeats exception; `cache/*` permits it |
| Exclude only root build output | Retain `docs/build/guide.md` | Replay passed |
| Exclude local environment files | Retain `.env.example` | Replay passed |
| Ignore an already tracked file | Report tracking; do not untrack | Replay verified index entry, default omission, and hypothetical `--no-index` matching |
| Append without merging patterns | Separate old and new patterns | Replay verified separated rules exclude both intended directories |
| Interpret verbose exception output | Matching `!` means inclusion | Replay verified output exists for retained file |
| Git command fails | Report failure | Invalid option returned 129 with diagnostic output |
| Personal exclusion covers requested shared policy | Preserve policy needed by other clones | Instruction review only |
| Review-only request | Make no edits | Instruction review only |
| Delete or untrack request | Ignore edits alone do not authorize either | Instruction review only |
| Required file ownership unclear | Recover policy or ask before exclusion | Instruction review only |
| Large repository | Bounded pages, explicit omissions, relevant information recovery | Limits reviewed; agent execution not run |

## Input budget

- SKILL.md body: 3,973 characters including saved-record convention.
- No bundled helper; numeric limits are agent instructions, not measured guarantees.
- Start with counts and relevant filenames; pages at most 100 paths or 150 lines,
  with omission counts and next offset. Recover all relevant pages before completion.
- Full repository diffs, unrelated file bodies, and templates are not required input.
- Large-input recovery and preservation under failed edits remain unverified as
  agent behavior. No runtime helper was added requiring output-budget tests.

## Environment

- Evaluation date: 2026-10-16 (Asia/Seoul).
- Agent: current Codex session; scripted replay, no independent agent evaluation.
- Tools: Linux/WSL, Git 2.43.0, Python 3.14.8.

## Detailed results

The replay script ran from OS temporary storage; its isolated repository was
removed automatically. Repository files were not modified by replay.
Validation results:

- Repository format/catalog validation passed for 67 skills.
- Existing unittest suite: 182 tests, OK with one Windows-only skip.
- Skills CLI 1.7.0 discovery and selective installation smoke checks passed.
- Packed CLI project/global lifecycle and bundled-byte checks passed.
- Skill Creator `quick_validate.py` passed with temporary PyYAML provisioning.
- `git diff --check` passed.

The full check command first stopped at installation smoke because the default
npm cache was read-only. Installation and package checks then passed separately
with `npm_config_cache` in `/tmp`; uv likewise used a temporary cache. No package
manifest changes were needed. Existing unrelated working-tree edits were retained.

Commit isolation check: exported HEAD plus only this skill's six selected files,
regenerated the baseline index, and ran `uv run check.py` with temporary caches.
All checks passed: 67 skills validated, 176 tests OK with one Windows-only skip,
installation smoke and packed CLI checks passed. The 182-test result above belongs
to the broader working tree containing pre-existing changes, not this commit alone.
