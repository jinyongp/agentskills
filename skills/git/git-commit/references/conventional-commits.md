# Conventional Commits

Read when requested or when repository policy/history uses this convention.
Repository configuration wins. Apply the format to each logical change:

```text
type(scope)!: description

Optional body explaining motivation or migration.

Optional footers.
```

- Type is required; scope and `!` are optional. Separate the prefix and description
  with a colon and space. Separate body/footers with blank lines.
- Use `feat` for features and `fix` for bug fixes. Common repository types:

  | Type | Change |
  | --- | --- |
  | docs | Documentation |
  | refactor | Restructuring without feature/fix |
  | perf | Performance |
  | test | Tests |
  | build | Dependencies/build |
  | ci | CI configuration |
  | chore | Other maintenance |
  | revert | Reversion |

- Breaking changes require `!` before the colon or an uppercase
  `BREAKING CHANGE:` footer explaining incompatibility; both may be used.
  `BREAKING-CHANGE:` is also accepted. Any type can break compatibility.
- Choose an existing component scope. Imperative wording and a 72-character
  subject are repository conventions, not requirements of the specification.
  Split independent concerns; do not invent effects from filenames alone.

```text
feat(git): add bounded inspection
fix(parser): preserve empty values
refactor(api)!: remove positional options

BREAKING CHANGE: pass options as a named object.
```

Specification: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
