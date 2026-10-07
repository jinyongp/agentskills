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
  Name the change they simplify or the resource they own: a cleanup wrapper pairs
  acquisition and release; a policy boundary avoids changing the same rule in several
  places. If removal preserves these needs with less coordination, use that alternative.
- Preserve the required path through success, reachable failures and recovery.
  Determine these requirements from the accepted scope, including deliberate
  omissions. A requested simulation or manual step is not an unfinished integration.
  Upload progress, submission state and retry behavior depend on the actual contract;
  implementing only a request call can leave that contract incomplete.
- Expose material limitations before choosing a shortcut that changes accepted
  behavior. Agreement on a prototype or reduced scope can permit that tradeoff.
- Reuse sufficient checks. Add coverage for a named gap, not a function/branch quota,
  and report what was actually exercised rather than equating small code with safety.

## Structural changes

When refactoring is part of the request, find the actual cost: duplicated policy
edits, unclear state/resource ownership, or tightly coupled callers that make the
current change difficult. Scope the fix to that friction; splitting files or adding
interfaces does not establish improvement by itself.

Before moving a responsibility, identify its callers, observable contract, lifecycle
and configuration. Keep those semantics while reducing coordinated edits or making
ownership clearer. Removing a wrapper must not lose cleanup, authorization, error
translation or compatibility. Keeping a useful wrapper needs no second implementation.

Use relevant before/after checks and inspect unchanged callers. Preserve accepted
architecture choices; a broader redesign needs a current requirement or a separate
decision. Do not generate glossary files, architecture tests or abstractions merely
because the refactor could support them.

## Completion evidence

Compare accepted outcomes with the final state and checks that actually ran.
Separate implemented behavior, verified behavior, and commit/publication state.
A planned check is pending; a required failed or unavailable check leaves completion
limited unless the user accepts that specific gap. Reuse evidence only when its
tested code, relevant configuration, and environment still apply. Inspect the final
diff for missing accepted behavior and accidental files. State any remaining decision
or action; completion alone grants no staging, commit, deployment, or task mutation.
