# survey evaluation

Six helper tests use temporary directories and actual JSON/TOML manifests.
They verify mechanical discovery, output bounds, and read-only behavior.
Independent agent repository interpretation and routing are not evaluated.

| Scenario | Expected result | Observed coverage |
| --- | --- | --- |
| Root summary and executable script strings | Identify markers without running project code | A marker-writing script remains inert; manifest unchanged |
| 160 Unicode/space/newline names | Exact paginated recovery | All names reassembled without duplicates or shortening |
| 120 package scripts | Bounded command pages with exact values | Reassembled records equal the source mapping |
| Python project entrypoint | Distinguish an entrypoint from a test command | Entry classified as python-entrypoint |
| Malformed, oversized, or external manifest | Explicit bounded failure, no partial result | Invalid data, 1 MB limit, oversized item, and external symlink covered |
| Nonexistent directory or invalid page | Bounded error without mutation | No files created |
| Ambiguous project manager or adjacent implementation request | Inspect sources; do not infer execution permission | Instruction review only |

## Input budget

Each JSON report is at most 4,000 characters including escaping and newline.
Default output contains counts and fixed marker names, not source or command contents.
Detail pages expose totals, omissions, and continuation offsets. Scripts do not run.
The helper reads direct children only; nested packages require a selected root.
Manifests are capped at 1 MB and external symlink targets are rejected.

## Environment and validation

- Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
- Tests: Python 3.11+ on Linux/WSL, isolated temporary directories.
- Eight skills validated; all 52 tests and CLI installation checks passed.
- Creator validation and actual selective installation passed; all three bundled files match.
- Independent monorepo mapping, large real-repository inference, and automatic routing remain untested.
