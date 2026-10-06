# Target and compatibility decisions

Read when choosing a version, diagnosing compatibility, or addressing an advisory.

## Version policy

Resolve the user's meaning of update from scope and project policy: newest permitted
resolution, changed manifest range, explicit target, or required remediation. Confirm
published versions and tags against the intended registry. Latest, stable, supported,
and compatible are different questions; account for prereleases and platform builds.

Version syntax is ecosystem-specific. [Semantic Versioning](https://semver.org/)
describes a public compatibility contract when a project follows it, not a guarantee
that every minor or patch release works in every consumer. Read relevant release
notes and actual usage, especially for pre-1.0 or differently versioned projects.

For example, [npm update](https://docs.npmjs.com/cli/v11/commands/npm-update/)
respects applicable dependency ranges; its command semantics do not mean every
selected manifest becomes an unconstrained latest release. Verify flags against the
installed tool version rather than transferring npm behavior to another resolver.

## Coherent groups and remediation

Inspect peer dependencies, runtime engines, adapters, plugins, generated clients,
SSR/build boundaries, and native SDK requirements when the selected package uses them.
Update a coupled set only when compatibility evidence requires it. A transitive
constraint may belong to a parent dependency rather than the top-level manifest.

For a security update, use a primary advisory, affected versions, reachable usage,
and the documented fix. Keep urgency and actual exposure distinct. A clean advisory
scan does not establish general security, and an override must be supported by the
consumer's compatibility rather than merely hiding a scanner finding.

Explain material license, support, size, or platform tradeoffs. If the named target
does not satisfy a hard constraint, propose an evidenced alternative or report the
blocker; do not silently select a different package or expand the upgrade scope.
