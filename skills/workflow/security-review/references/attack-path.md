# Trace the boundary

| Trigger | Evidence to inspect | Decision |
| --- | --- | --- |
| User selects an object, tenant, or action | Identity, resource ownership, role checks and final mutation/read | Authentication alone does not establish authorization |
| User data reaches SQL, shell, HTML, or a parser | Exact API semantics, parameter boundaries, escaping context and downstream use | Report a reachable interpretation change, not an API name |
| User controls a filename or archive entry | Canonical destination, symlinks, extraction behavior and final file operation | Check whether attacker-selected data can escape the permitted root |
| Code fetches an external URL | Input ownership, redirects, DNS resolution, egress rules and credential forwarding | Check reachable restricted targets and data exposure |
| Secret or token appears in output/storage | Actual sensitivity, readers, serialization and redaction boundaries | Report exposure without copying secret values into evidence |
| CI executes PR content with credentials | Event, checkout revision, local scripts/actions, token permissions and gates | Trace untrusted code to the privileged execution context |

For GitHub Actions, follow values through shell interpolation and action consumers;
an expression in an input is not automatically safe or exploitable. Inspect fork
code, artifact/cache handoffs, and reusable workflows when they cross trust boundaries.
Full SHA pins identify content; they do not prove that the content or execution is safe.

Sources for verification:
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP SSRF guidance](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

Workflow inspiration: [Sentry security-review](https://github.com/getsentry/skills/tree/main/skills/security-review).
This guidance is independently written; upstream OWASP-derived reference files
(CC BY-SA 4.0) are not bundled. Sentry's repository uses Apache-2.0.
