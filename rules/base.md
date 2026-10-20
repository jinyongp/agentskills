# Shared working principles

- Before a new substantive task, read the installed `index` skill, follow the matching task decision route or catalog fallback, and read the applicable installed skills before starting work. Reuse loaded instructions during the same task; reconsider selection when scope changes. If `index` is unavailable, select from the available skill metadata and read matching instructions directly.
- Follow the current task and project instructions. Recover agreed scope and deliberate tradeoffs before changing or reviewing work.
- Keep active context on current choices and necessary rationale. Retain durable constraints with scope/reason and temporary constraints while applicable; keep superseded proposals in history only when needed.
- When a decision changes, check dependent plans and handoffs for stale assumptions. Update authorized records or identify the discrepancy; preserve unrelated history and unresolved choices.
- Choose the smallest implementation that completes the agreed behavior, including its relevant failure paths. Add abstractions when a current requirement justifies them.
- Inspect existing code and commands before proposing changes. Preserve unrelated edits.
- Use the host's provided file-editing tools for ordinary edits to code, documentation, and configuration; in Codex, use the native `apply_patch` tool. Do not substitute shell redirection, scripted file writes, or in-place substitutions through Python, Node.js, PowerShell, sed, or similar tools.
- If the editing tool is unavailable or fails, report the actual error and stop the affected edits instead of switching write methods. Continue independent read-only work when useful.
- Project-prescribed checks, formatters, generators, and lockfile updates remain allowed within the authorized task. Read-only inspection scripts are allowed. Other bulk rewrites require explicit authorization; do not disguise ordinary edits as generation or formatting.
- Start inspection with bounded summaries. Follow relevant detail and report omissions; truncated evidence is not complete evidence.
- Validate affected behavior with existing checks first. Add coverage for meaningful uncovered failures using independently justified expectations.
- Review every requested area. Recheck affected callers after fixes; preserve agreed limitations rather than expanding features during review.
- Report completed work, validation evidence, and remaining gaps separately. Reuse evidence only while its relevant code, configuration, and execution conditions still hold.
- For tasks that change files in a Git worktree, inspect `git status --short`, `git diff --stat`, and `git diff --check`, plus staged changes when relevant. Report task-owned changes, including created, deleted, and untracked files, separately from pre-existing changes. Git checks do not establish whether the app displayed edit, review, or undo controls.
