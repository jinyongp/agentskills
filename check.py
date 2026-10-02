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
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", nargs="?", default="all", choices=("all", *CHECKS))
    args = parser.parse_args()
    selected = CHECKS if args.check == "all" else (args.check,)
    for name in selected:
        print(f"Running {name}...", flush=True)
        result = subprocess.run([sys.executable, *CHECKS[name]], cwd=ROOT)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
