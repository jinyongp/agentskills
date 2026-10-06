# Consumer compatibility

Read for serialization, defaults, schema evolution, SDK changes, or migration policy.

## Check the actual boundary

Source, wire, and behavior compatibility can fail independently. Code may compile
while interpreting a changed response differently; a valid payload may violate the
consumer's assumptions. Inspect supported clients, generated code, strict decoders,
persisted values, and public promises relevant to the selected change.
The [Google compatibility guidance](https://google.aip.dev/180) illustrates these
distinctions for its API conventions. Use the project's actual support contract;
its organizational rules are not universal requirements for every API.

## Values and representation

Define absent, null, empty, zero, defaulted, and explicitly cleared values separately
where they matter. A new default or changed omission behavior can alter old clients.
Preserve documented units, time-zone meaning, numeric precision, identifier format,
encoding, and error interpretation. Changing a field's representation can affect
stored values or parser assumptions even when its type name stays the same.

Additive fields, enum values, or parameters need evidence of tolerated expansion.
Strict decoding, exhaustive branches, SDK overloads, or positional invocation can
make an apparently optional addition incompatible. Keep old supported operations
working through the intended transition. Independently justify conformance samples;
snapshots of current output alone are not an authoritative contract.

## Versions and transition

Use the selected protocol's and project's version/support policy. A separate URL,
schema version, package major, or negotiated capability can be appropriate; none is
required merely because a change exists. Explain the actual break and affected
consumers before selecting a transition. Preserve deprecation and migration windows
only when they are established; do not invent a service commitment or deadline.

Keep generated artifacts aligned with their authoritative schemas and tool versions.
Identify a migration path, affected examples, and the checks that establish both
old and new required behavior. Unknown consumers or unavailable target versions
remain explicit coverage gaps, not evidence that nobody depends on the interface.
