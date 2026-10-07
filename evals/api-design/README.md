# API design evaluation

## Accepted-scope review — 2026-10-07

Parent instruction review; model version not recorded. Paired case:
A scoped synchronous interface needs its accepted semantics; review does not add
asynchronous jobs or automatic retries solely for completeness.
The revised rules recover agreed limits before judging gaps. This is not independent
agent execution. Repository checks and actual selective installation passed for this
revision; earlier results below retain their original scope.


See [parent task execution](../task-execution/README.md) for actual provider/consumer
serialization demonstrating a strict consumer's incompatibility with an additive
field. That review leaves implementation unchanged; it does not test transport.

## Decision cases

Parent instruction review on 2026-10-06 in the current Codex session; model version
not recorded. Cases assess the written rules, not independent API design or provider
conformance.

| Request or condition | Expected decision | Review result |
| --- | --- | --- |
| Existing RPC interface needs one operation | Preserve protocol and consumer conventions | No REST or framework migration |
| Design or review only | Return a contract or findings | No implementation/publication inferred |
| Actual callers and documentation disagree | Establish intended and supported behavior | No guessed canonical contract |
| Routine naming choice has one conventional fit | Choose from project context | No unnecessary approval gate |
| Absent field, null, and empty value mean different things | Specify their separate semantics | No vague optional-field rule |
| Units or identifier representation changes | Check real parser and stored-value assumptions | Same type does not prove compatibility |
| Additive field breaks a strict decoder | Inspect supported consumers before claiming compatibility | No universal additive-is-safe rule |
| New enum member breaks exhaustive client handling | Address supported consumer behavior | No schema-only compatibility claim |
| Optional SDK argument changes overload resolution | Check source and runtime usage | Optional does not imply harmless |
| Changed default alters old client behavior | Preserve the contract or plan a policy-backed transition | No silently broadened semantics |
| HTTP acknowledgement is lost after a write | Define uncertain outcome and safe recovery | No assumed failed mutation or blind retry |
| Duplicate key uses different payload or tenant | Define key scope and conflict behavior | No guessed deduplication guarantee |
| Concurrent updates or partially successful batch | Specify conflict and completion semantics | No invented atomicity |
| Authenticated client accesses another owner's resource | Check resource-level permission | Authentication is not authorization |
| Pagination under changing data | Match traversal and recovery to actual requirements | No universal cursor or page-size mandate |
| Asynchronous request is accepted but work is pending | Keep acceptance, status, and completion distinct | No false completed outcome |
| Existing checks already verify required compatibility | Reuse them | No duplicate snapshots or literal assertions |
| Schema or mock passes while provider is unavailable | Record what was checked and what was not | No provider-conformance claim |
| Large schema and many unknown consumers | Selected operation/consumer summaries, progressive detail and omissions | No whole-schema dump or complete coverage claim |
| Version or deprecation policy is missing | Resolve consequential transition requirements | No invented support deadline or forced version scheme |

## Input budget and evidence limits

No protocol-specific inspection runner is bundled. Native schema tools and selected
caller/interface queries are preferable to an assumed universal API format. Default
input is selected operations, consumer boundaries, and relevant diffs; whole generated
clients and schemas remain outside default input. A reducer, if needed, requires
explicit limits and large-input/failure verification. Universal output sizes and
large-schema recovery have not been measured.

References provide original decision guidance with primary-source links, not copied
organizational policies. Production provider/consumer execution, protocol-specific
generation, independent design quality, security guarantees, and automatic routing
remain unmeasured.

Packaging verification passed: 49 skills, 76 existing tests, and CLI fixtures.
Creator validation and actual selective installation with skills@1.7.0 passed;
all four bundled files matched byte-for-byte. MIT notice and local links passed.
Entrypoint body: 3,849 characters, excluding frontmatter. Initial overflow was
resolved by condensing repeated scope and result wording without removing contracts.
