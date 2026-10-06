# Operation semantics

Read only the section matching the selected operation. Follow project and protocol
requirements; these questions do not require every API to implement every feature.

## Errors and authorization

Distinguish invalid input, missing/inaccessible resources, conflict, limits, unavailable
dependencies, and internal failure according to the consumer contract. State meaningful
retry/recovery behavior without exposing secrets or internal implementation details.
Resolve identity, ownership, tenant boundaries, and resource-level permission where
the operation needs them; authentication alone does not establish authorization.

For HTTP, use method and status semantics from
[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html). RPC, SDK exceptions, and
message delivery have their own error boundaries; do not transfer HTTP conventions
without checking the selected protocol and client behavior.

## Retries, duplicates, and concurrency

Define what happens when an operation succeeds but its acknowledgement is lost.
Transport failure does not prove no side effect occurred. Idempotence concerns the
intended effect of repetition, not identical status codes or response bodies.
For a deduplication key, define scope, payload mismatch, concurrent attempts, result
lookup, retention/expiry, and what the actual implementation guarantees.
Avoid promising exactly-once effects solely from a retry mechanism or request ID.

Where updates compete, specify version/conflict or merge behavior and retry safety.
Keep cancellation, timeout, and committed outcome distinct. Batch operations need
atomicity or per-item completion/error semantics when partial success is possible.

## Pagination, streams, and jobs

Define ordering, traversal state, limit meaning, and stability under relevant data
changes. Cursor and offset schemes have different tradeoffs; choose from actual
consumer requirements rather than imposing one globally. State how omitted results
can be recovered and whether a snapshot or live view is promised.

For streams/messages, define applicable delivery, ordering, reconnection, and duplicate
handling. For asynchronous jobs, define acknowledgement, identity, status, terminal
states, cancellation, result retrieval, and expiry only where needed. A successfully
accepted request is not proof that its work completed. Match guarantees to verified
provider behavior and supported client recovery.
