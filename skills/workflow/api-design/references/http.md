# HTTP API rules

Read for HTTP design or review; follow only sections relevant to the operation.
Use resource-oriented HTTP as the default for new contracts. Naming, envelopes,
pagination style, and version placement are design choices: follow established
conventions and explain consequential exceptions. Method and status meanings are
protocol constraints. Do not silently change a supported legacy contract to improve
style; identify violations and their consumer impact before proposing migration.

## Resources and routes

- Name resources with domain nouns; default collections to plural paths such as
  `/invoices/{invoiceId}`. Keep casing and separators consistent. Avoid database
  table names or CRUD verbs such as `/getInvoice` in new resource routes.
- Nest for actual ownership or scoped identity, not every database relationship.
  Choose a canonical resource URI; keep identity stable when mutable labels change.
- Put resource identity in paths, selection/filter/sort/page controls in queries,
  and structured write data in bodies. Do not depend on GET request bodies. Keep
  credentials and sensitive values out of URLs, which may reach logs and history.
- Model a domain transition as a resource when it has useful identity or lifecycle
  (for example, `POST /invoices/{id}/cancellations`). Otherwise a documented POST
  action can fit; do not force every action into an arbitrary field update.
  Specify allowed source states, effects, duplicate calls, and invalid transitions.
- Requests must carry the context needed to interpret them; avoid hidden workflow
  state that makes identical requests depend on an undocumented prior call.

## Methods and write semantics

| Method | Contract to check |
| --- | --- |
| GET / HEAD | Read without requested domain mutations; logging is incidental. HEAD returns no content. Never use GET for confirmation, deletion, or payment effects. |
| POST | Create in a collection or process an explicit action. Define generated identity, effects, and whether retries require deduplication. |
| PUT | Create or replace state at the target URI; define writable representation and omitted-field behavior. Do not label a merge-only partial update PUT. |
| PATCH | Apply a defined patch format; specify omitted/null values, array edits, validation, and atomic application. PATCH is not inherently idempotent. |
| DELETE | Remove the target association; define soft deletion, downstream effects, and repeated/missing-resource outcomes. Repetition must not repeat the intended effect. |

PUT and DELETE idempotence concerns intended effects, not identical responses.
For PATCH, declare the media type and semantics; do not assume every JSON object is
a standardized patch. Reject a failed patch without partially applying it.
Where lost updates matter, define version checks, for example ETag with If-Match,
or an existing revision contract. State how clients recover after conflicts.

## Responses and errors

- Choose status from the actual outcome: 200 for success with content, 201 for
  creation, 202 for accepted unfinished work, 204 for success without content.
  Default creation responses to a canonical Location and useful representation;
  document alternatives. A 204 response has no content. A 202 response must explain
  how completion is observed when the caller needs that outcome.
- Return an empty collection as a successful list response with an empty result,
  not a missing-resource error. Distinguish a missing parent or individual resource.
- Separate malformed requests (400), absent/invalid credentials (401, with an
  appropriate WWW-Authenticate challenge), denied permission (403), and missing
  resources (404). A deliberate 404 concealment policy must be consistent.
- Distinguish current-state conflict (409), failed request precondition (412),
  unsupported request media type (415), unacceptable response media type (406),
  and syntactically valid but unprocessable content (422). Choose and document
  400 versus 422 validation policy consistently; not every business failure is 409.
  Methods implemented by the server but disallowed for the target use 405 with
  Allow; unrecognized or unimplemented methods use 501. Rate limits use 429;
  temporary service unavailability can use 503. Specify retry advice only when supported.
- Do not hide a failed operation inside 200. For deliberate batch protocols,
  distinguish envelope success from per-item failures and document partial effects.
- Keep one documented error shape with a stable machine-readable discriminator,
  actionable detail, and field locations for validation failures. Clients must not
  parse human prose for control flow. Preserve an existing suitable shape; consider
  RFC 9457 Problem Details for a new one. Avoid stack traces and secret values.

## Representations and validation

- Declare request/response media types and actual negotiation behavior. Keep field
  naming and collection envelopes consistent; do not mandate an envelope everywhere.
- Specify required, writable, read-only, nullable, defaulted, and clearable fields.
  Define types, ranges, string/collection bounds, enum handling, and cross-field
  rules from domain requirements. Reject or explicitly ignore unknown fields;
  never accidentally bind arbitrary input to privileged model properties.
- Fix representations for identifiers, timestamps/time zones, durations, money,
  and large numbers using consumer precision needs. Define coercion deliberately;
  avoid different interpretation of the same value across operations.
- Validate before effects; state transactional or partial behavior across multiple
  writes. Check ownership and tenant access on resources, nested parents, related
  identifiers, and restricted writable fields rather than only at route entry.

## Lists, retries, and caching

- For list operations, define supported filters, operators, sort directions, and
  handling of invalid parameters. Use deterministic ordering with a tie-breaker.
  When pagination is needed, specify default/maximum limits, invalid-limit behavior,
  next-page detection, terminal pages, and cursor expiry or invalidity where applicable.
  Choose cursor or offset from traversal needs; do not invent page sizes or exact total counts.
- For paginated lists, state consistency under inserts/deletes and how selection
  binds to continuation state. Empty results and exhausted pages need predictable
  shapes. Treat cursors
  as opaque to clients; a cursor never substitutes for authorization.
- For retryable writes, establish whether operation idempotence provides sufficient
  recovery. When using deduplication keys, define scope, payload mismatch, concurrent
  duplicates, retention, and lost-response recovery using the operation guidance.
  Retry-After can guide timing; it does not make a non-idempotent write safe.
- Choose explicit cache policy where freshness or confidentiality matters. Separate
  private reuse, shared caching, and no-store; no-cache permits storage with
  revalidation. Include relevant Vary dimensions for negotiated representations.
  Do not allow shared caches to mix user/tenant responses. If conditional reads
  are supported, define validators and 304 responses without content.

## Contract checks

For each selected operation, make method/path, authorization, input constraints,
success status/body/headers, relevant failures, and retry semantics inspectable in
the project's schema or examples. Review meaningful boundaries: empty versus
missing, omitted versus null, stale updates, duplicate writes, and page traversal
where supported. Reuse existing checks; do not require every feature or a new test
for every rule. Check evolution with the compatibility guidance.

## Technical sources

- [RFC 9110](https://httpwg.org/specs/rfc9110.html): methods, status codes,
  negotiation, validators, and preconditions.
- [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html): PATCH semantics and atomicity.
- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html): machine-readable error details.
- [RFC 9111](https://httpwg.org/specs/rfc9111.html): cache controls and reuse.
