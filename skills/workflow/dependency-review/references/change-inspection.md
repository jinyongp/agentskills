# Inspect the selected change

Use Git and Python 3.11+. Commands are relative to this installed skill directory;
`--repo` identifies the project being inspected. Execute the bundled helper
without reading its source. It fetches nothing and changes no project files/index.

Start with counts:

```bash
python3 scripts/inspect_changes.py --repo <root>
```

For a comparison add `--base <ref> --head <ref>`. Add `--merge-base` for branch
additions when appropriate, not for every endpoint or commit comparison. Establish
the intended base from the user/project instead of assuming a branch name. The
response returns resolved IDs; reuse them for subsequent detail queries.

- `--mode files` lists paths and layers; select relevant pages.
- `--mode diff --path <file>` reads that path's diff. Repeat `--path` to narrow scope.
- For local index inspection use `--layer staged`; do not mix it with working changes.
- Follow `--offset <next_offset>` until needed evidence is complete. Each JSON
  response is at most 4,000 characters including escaping and its newline.

Counts cover omitted items. Preserve exact paths; oversized entries fail visibly.
Refresh inspection after local changes. Renames appear as deletion/addition.
Read selected untracked content separately; Git diffs do not contain it. Keep
credentials out of reports and avoid unrestricted diff/log dumps. Binary files,
submodules, and generated outputs may need their own evidence. An error or partial
listing is not proof that no relevant change exists.
