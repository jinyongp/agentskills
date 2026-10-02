# Repository instructions

This repository distributes standalone Agent Skills through the skills CLI.

- Keep installable skills at `skills/<category>/<skill-name>/SKILL.md`.
- Keep skill names unique across the repository and equal to their directory names.
- Use lowercase ASCII letters, digits, and single hyphens for skill and category names.
- Keep each skill self-contained. Bundle runtime references, scripts, and assets inside its directory.
- Use skill-root-relative paths for bundled files. Repository instructions are for maintainers, not installed skill dependencies.
- Keep templates under `templates/` with a `.tmpl` extension.
- Prepare new skills with `uv run new_skill.py <category> <name>`, then write the generated instructions and evaluation cases.
- Update the root and category catalogs when adding, moving, or removing a skill.
- Follow `CONTRIBUTING.md` for authoring and verification.
- Keep descriptions within 300 characters and SKILL.md bodies within 4,000 characters. Include only task-changing guidance; preserve essential context and boundaries.
- Load references only for a stated condition. Execute bundled helpers without reading their source by default.
- Use scripts for repeated mechanical inspection or large-output reduction. Start with bounded summaries; request only relevant detail, with explicit omission counts and pagination.
- Define and test inspection output limits, including large inputs and failures. Never treat truncated information as complete or shorten exact paths silently.
- Run `uv run check.py` for full verification, or `uv run check.py validate` for skill format and catalog checks. CI adds `--locked` to enforce the committed dependency lockfile.
- Preserve third-party licenses and attribution. Original repository content uses MIT.
- Use `rg` for searches and preserve unrelated changes.
- Validate each meaningful work unit before committing it. Keep independent changes in separate Conventional Commits.
- For workspaces under `/home/`, run environment-sensitive tooling in interactive Linux bash using Linux paths.
