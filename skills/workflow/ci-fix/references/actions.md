# Stable GitHub Actions

Use when authoring or changing workflows or composite actions.

1. Resolve external actions and reusable workflows to the newest compatible stable
   upstream release permitted by user/project pins, exclusions and release-age policy.
   Check release notes, inputs/outputs, runtime/runner requirements and the release
   commit. A moving major tag or updater suggestion alone does not verify the version.
   Prefer the newest stable major when compatible; explain a required older pin.
   Branch tips and prereleases require an explicit project choice.
2. Follow the project's updater. Where actions-up is required, run the appropriate
   scoped invocation. `npx actions-up --dry-run` previews changes;
   `npx actions-up --yes` applies updates. Its scan may cover more than the selected
   workflow: review and retain only authorized changes. Honor exclusions/cooldowns
   and inspect skipped or unresolved references; do not disable them to claim latest.
3. Pin external actions/workflows to the verified full commit SHA with a version
   comment. Local actions retain local paths. Confirm that the SHA belongs to the
   intended upstream release; immutability alone does not establish trust.
4. Use an explicit supported runner image, for example ubuntu-24.04 when suitable,
   rather than ubuntu-latest. Keep self-hosted labels and required OS/platform
   support. Image labels still receive updates; an explicit label is not a frozen OS.
5. Trace changed triggers, checkout revisions, secrets, permissions, caches and
   artifact handoffs. Keep untrusted PR code separate from privileged execution.
   Inspect the updater's diff; syntax/lint checks do not prove runtime compatibility.
   Verify affected CI on the actual revision when execution is authorized.

Sources: [actions-up](https://github.com/azat-io/actions-up),
[GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use),
[GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
Versions are resolved at task time; examples are not permanent version pins.
