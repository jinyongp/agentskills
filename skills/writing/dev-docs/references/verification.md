# Documentation evidence

Read when validating examples, generated references, or support/version claims.

## Claims and generated content

Resolve supported public behavior from the selected version's interfaces, tests,
release policy, and official documentation. Internal implementation is evidence,
not permission to advertise every incidental behavior as a stable API.
When a spec and implementation disagree, identify the discrepancy and requested
version; do not silently rewrite either to make the document appear consistent.

Edit generated documentation at its authoritative source, regenerate using the
project's commands, and inspect the resulting scope. A generated file's existence
does not prove accuracy. Preserve existing notices and quoted source meaning.

## Examples and commands

Use an owned temporary project or disposable fixture when practical. State relevant
runtime, package version, directory, prerequisites, and placeholders. Confirm the
documented invocation, meaningful result, and cleanup when execution is available.
Check environment-sensitive quoting, paths, encoding, shell differences, and supported
platform assumptions only where the audience or command requires them.

Examples that create accounts, mutate remote data, or spend money need the applicable
task authorization and isolation. Clearly distinguish illustrative output from an
observed run. If authentication or infrastructure is unavailable, validate what is
possible and list the untested operation rather than fabricate a successful transcript.

Prefer sufficient existing snippet, type, schema, build, and link checks. A spelling
or build pass does not establish behavior. A one-off documentation fix does not need
tests that merely pin a heading, literal sentence, or page layout.
