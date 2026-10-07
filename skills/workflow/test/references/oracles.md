# Independent expectations

Read when code and tests reuse generated assumptions or a result lacks a justified oracle.

- Ground expected behavior in the user's requirements, supported contracts or an
  independently checked example. A generated implementation, its summary and its
  current output share assumptions; agreement among them does not establish correctness.
- Read code to find interfaces and reachable failures, while separately deriving
  what should happen. Resolve consequential missing semantics rather than inventing
  expected values. Tests may follow implementation if their expectations stay grounded.
  Recover agreed omissions from decisions and handoffs. A test must not turn an
  optional capability into a required one, or force expansion of a scoped prototype.
- A separate session, agent or model can repeat the same mistake. Distinct authors
  do not by themselves establish independence; identify the expectation's evidence.
- For a material detection gap, use the reported faulty state or a targeted wrong
  implementation to confirm the check rejects the named failure, and a valid case
  to confirm it preserves legitimate behavior. Reuse existing evidence when sufficient;
  exhaustive mutation testing and extra permanent tests are not required.
- Investigate agreement between broken code and passing tests. Preserve the intended
  contract rather than weakening assertions to match the implementation.

Evidence: [On the risk of coding before testing (2026)](https://arxiv.org/abs/2607.05139)
studies fault propagation across generated code and tests. Its benchmark results
motivate checking oracle independence, not a mandatory test-first workflow.
