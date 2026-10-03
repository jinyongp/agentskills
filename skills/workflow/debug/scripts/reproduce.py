"""Run an explicit check with a complete log and bounded JSON reports (POSIX)."""

import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys

OUTPUT_LIMIT = 4000


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")) + "\n"


def emit(value):
    if len(encoded(value)) > OUTPUT_LIMIT:
        value = {"error": "Report metadata exceeds the output budget; use the supplied log path directly."}
        print(encoded(value), end="")
        return False
    print(encoded(value), end="")
    return True


class Parser(argparse.ArgumentParser):
    def error(self, message):
        emit({"error": "Invalid arguments; run --help."})
        raise SystemExit(2)


def run(args):
    if os.name != "posix":
        raise ValueError("The runner needs POSIX process groups; use the check directly on other platforms.")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise ValueError("Timeout must be a positive finite number.")
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise ValueError("Provide a check command after --.")
    if not args.cwd.is_dir():
        raise ValueError("Check working directory is unavailable.")
    log = args.log.resolve()
    with log.open("xb") as output:
        process = subprocess.Popen(command, cwd=args.cwd, stdout=output,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        timed_out = False
        try:
            process.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
    result = {"result": "timeout" if timed_out else "pass" if process.returncode == 0 else "fail",
              "returncode": process.returncode, "log": str(log), "output_bytes": log.stat().st_size,
              "output_in_summary": False}
    return result, 124 if timed_out else 0 if process.returncode == 0 else 1


def read_log(args):
    if args.offset < 0:
        raise ValueError("Offset must be nonnegative.")
    with args.log.open("rb") as source:
        total = os.fstat(source.fileno()).st_size
        if args.offset > total:
            raise ValueError("Offset exceeds log size; refresh the query.")
        source.seek(args.offset)
        chunk = source.read(OUTPUT_LIMIT)
    # surrogateescape preserves invalid UTF-8 bytes rather than silently dropping them.
    def page(size):
        end = args.offset + size
        return {"offset_bytes": args.offset, "total_bytes": total,
                "text": chunk[:size].decode("utf-8", "surrogateescape"),
                "next_offset": end if end < total else None,
                "omitted_bytes": total - end, "encoding": "utf-8/surrogateescape"}
    low, high = 0, len(chunk)
    while low < high:
        middle = (low + high + 1) // 2
        if len(encoded(page(middle))) <= OUTPUT_LIMIT:
            low = middle
        else:
            high = middle - 1
    return page(low), 0


def main():
    parser = Parser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True, parser_class=Parser)
    execute = modes.add_parser("run", help="Run a finite command without shell expansion")
    execute.add_argument("--cwd", type=Path, required=True)
    execute.add_argument("--log", type=Path, required=True, help="New log file; existing files are preserved")
    execute.add_argument("--timeout", type=float, default=300)
    execute.add_argument("command", nargs=argparse.REMAINDER)
    detail = modes.add_parser("log", help="Read one bounded log page")
    detail.add_argument("--log", type=Path, required=True)
    detail.add_argument("--offset", type=int, default=0, help="Byte offset from next_offset")
    args = parser.parse_args()
    try:
        result, code = run(args) if args.mode == "run" else read_log(args)
    except (OSError, ValueError):
        # Do not echo executable arguments, output, or potentially sensitive exception text.
        emit({"error": "Check could not run or log could not be read; verify command, paths, and arguments."})
        return 2
    return code if emit(result) else 2


if __name__ == "__main__":
    sys.exit(main())
