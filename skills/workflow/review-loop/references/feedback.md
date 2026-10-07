# Evaluate incoming review feedback

- Pin each comment to its file/revision and recover the expected behavior and
  accepted tradeoffs. A comment on an older revision may already be resolved.
- Treat reviewer and bot claims as candidates. Trace their trigger and effect,
  check defenses and callers, and reproduce when needed. Severity labels and
  reviewer confidence do not establish a defect.
- Classify each item as confirmed defect, already addressed, unsupported claim,
  clarification needed, or optional scope change. Give the evidence that changes
  the decision; do not implement a feature merely to satisfy an external suggestion.
- Preserve compatible independent work while clarifying a material ambiguity.
  Pause only changes that depend on the unresolved answer. A request to fix review
  findings does not erase prior product limits or imply new external permissions.
- For confirmed defects, apply authorized corrections and recheck affected areas.
  For unsupported claims, explain the concrete code/contract evidence. A stylistic
  suggestion may be acted on when requested, but does not become a correctness defect.
- Replies, resolving remote threads, and pushing commits follow the user's current
  scope. A proposed or posted reply is not proof that the code was corrected.
