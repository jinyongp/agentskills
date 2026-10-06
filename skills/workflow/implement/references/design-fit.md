# Simple and complete implementation

Read only for the current design or completeness decision.

- Reuse fits when its behavior, error semantics, lifecycle, supported platforms and
  integration match the task. A short standard-library call can still miss freshness
  or tenant isolation; a dependency can be appropriate when it covers those needs.
- Keep code easy to understand and modify. A readable function may be simpler to
  maintain than a compressed expression. A named boundary or cleanup wrapper can
  earn its cost without multiple implementations or callers.
- Give added configuration, layers, packages and extension points a current purpose
  or concrete maintenance benefit. Scope refactoring to what enables this task.
- Preserve the required path through success, reachable failures and recovery.
  Upload progress, submission state and retry behavior depend on the actual contract;
  implementing only a request call can leave that contract incomplete.
- Expose material limitations before choosing a shortcut that changes accepted
  behavior. Agreement on a prototype or reduced scope can permit that tradeoff.
- Reuse sufficient checks. Add coverage for a named gap, not a function/branch quota,
  and report what was actually exercised rather than equating small code with safety.
