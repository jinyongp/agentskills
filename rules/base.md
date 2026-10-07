# Shared working principles

- Follow the current task and project instructions. Recover agreed scope and deliberate tradeoffs before changing or reviewing work.
- Keep active context on current choices and necessary rationale. Retain durable constraints with scope/reason and temporary constraints while applicable; keep superseded proposals in history only when needed.
- When a decision changes, check dependent plans and handoffs for stale assumptions. Update authorized records or identify the discrepancy; preserve unrelated history and unresolved choices.
- Choose the smallest implementation that completes the agreed behavior, including its relevant failure paths. Add abstractions when a current requirement justifies them.
- Inspect existing code and commands before proposing changes. Preserve unrelated edits.
- Start inspection with bounded summaries. Follow relevant detail and report omissions; truncated evidence is not complete evidence.
- Validate affected behavior with existing checks first. Add coverage for meaningful uncovered failures using independently justified expectations.
- Review every requested area. Recheck affected callers after fixes; preserve agreed limitations rather than expanding features during review.
- Report completed work, validation evidence, and remaining gaps separately. Reuse evidence only while its relevant code, configuration, and execution conditions still hold.
