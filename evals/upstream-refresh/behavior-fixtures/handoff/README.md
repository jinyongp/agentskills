# Cleanup preview

This CLI plans removal of old local archive files. The current task implements a
dry-run preview, with no deletion, network, or cloud synchronization. Retention is
read from config.json. Files older than that number of days appear in the plan;
files exactly at the boundary remain. Do not modify or remove real user files.

`python3 -m unittest discover -s tests -v` runs the focused checks. `python3 preview.py`
prints a preview for the bundled sample. Existing decisions live in DECISIONS.md.
