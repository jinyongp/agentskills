"""Run repository checks using the Python environment prepared by uv."""

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
CHECKS = {
    "validate": ("scripts/validate_skills.py",),
    "test": ("-m", "unittest", "discover", "-s", "tests", "-v"),
    "smoke": ("scripts/smoke_install.py",),
    "package": ("scripts/smoke_package.py",),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", nargs="?", default="all", choices=("all", *CHECKS))
    parser.add_argument("--check-index", action="store_true", help="Check index freshness without regenerating it (all or validate)")
    args = parser.parse_args()
    if args.check_index and args.check not in ("all", "validate"):
        parser.error("--check-index requires all or validate")
    selected = CHECKS if args.check == "all" else (args.check,)
    if "validate" in selected and not args.check_index:
        print("Refreshing skill index...", flush=True)
        result = subprocess.run([sys.executable, "scripts/generate_index.py"], cwd=ROOT)
        if result.returncode:
            return result.returncode
    for name in selected:
        print(f"Running {name}...", flush=True)
        result = subprocess.run([sys.executable, *CHECKS[name]], cwd=ROOT)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
