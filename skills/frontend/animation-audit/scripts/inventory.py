"""Read-only, bounded motion candidate inventory; Python 3.11+ and Git."""

import argparse
import json
from pathlib import Path
import re
import subprocess

OUTPUT_LIMIT = 4000
FILE_LIMIT = 1_000_000
EXTENSIONS = {'.css', '.scss', '.sass', '.less', '.js', '.jsx', '.ts', '.tsx',
              '.vue', '.svelte', '.html', '.json', '.mjs', '.cjs'}
PATTERN = re.compile(r'@keyframes|\b(?:animation|transition)\s*:|\bmotion[.(]|'
                     r'\b(?:useSpring|useAnimatedStyle|withSpring|withTiming|Animated)\b|'
                     r'\b(?:pointermove|pointerdown|onPointerMove|onPointerDown)\b|'
                     r'\bGesture\.|\.animate\s*\(|prefers-reduced-motion|'
                     r'react-native-reanimated|framer-motion|motion/react|\bgsap\b')


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(',', ':')) + '\n'


class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(encoded({'error': 'Invalid arguments; run --help.'}), end='')
        raise SystemExit(2)


def page(items, offset, limit, scope):
    if not 0 <= offset <= len(items) or not 1 <= limit <= 100:
        raise ValueError('Invalid output page; refresh and use a limit of 1-100.')
    shown = items[offset:offset + limit]
    while True:
        end = offset + len(shown)
        result = {**scope, 'total': len(items), 'offset': offset, 'items': shown,
                  'omitted_before': offset, 'omitted_after': len(items) - end,
                  'next_offset': end if end < len(items) else None}
        if len(encoded(result)) <= OUTPUT_LIMIT:
            if not shown and offset < len(items):
                raise ValueError('An exact entry exceeds the output budget; inspect that scan window directly.')
            return result
        if not shown:
            raise ValueError('Scope exceeds the output budget.')
        shown.pop()


def inspect(args):
    root = args.root.resolve()
    if not root.is_dir():
        raise ValueError('Selected root is unavailable.')
    if not 1 <= args.scan_limit <= 10000:
        raise ValueError('Use a scan limit of 1-10000 files.')
    listing = subprocess.run(['git', '-c', 'core.fsmonitor=false', 'ls-files', '-z',
                              '--cached', '--others', '--exclude-standard'],
                             cwd=root, capture_output=True, timeout=30)
    if listing.returncode != 0:
        raise ValueError('Git file discovery failed; select a worktree directory or use project tooling.')
    names = sorted({p.decode('utf-8').removeprefix('./') for p in listing.stdout.split(b'\0')
                    if p and Path(p.decode('utf-8')).suffix.lower() in EXTENSIONS})
    if not 0 <= args.scan_offset <= len(names):
        raise ValueError('Invalid scan offset; refresh the inventory.')
    window = names[args.scan_offset:args.scan_offset + args.scan_limit]
    candidates, skipped = [], []
    for name in window:
        path = root / name
        try:
            if not path.resolve().is_relative_to(root) or not path.is_file():
                skipped.append({'path': name, 'reason': 'outside-root-or-not-file'})
                continue
            with path.open('rb') as stream:
                raw = stream.read(FILE_LIMIT + 1)
            if len(raw) > FILE_LIMIT:
                skipped.append({'path': name, 'reason': 'over-1MB'})
                continue
            text = raw.decode('utf-8')
            if '\0' in text:
                skipped.append({'path': name, 'reason': 'binary'})
                continue
            matches = [i for i, line in enumerate(text.splitlines(), 1) if PATTERN.search(line)]
            if matches:
                candidates.append({'path': name, 'first_line': matches[0], 'matching_lines': len(matches)})
        except (OSError, UnicodeError):
            skipped.append({'path': name, 'reason': 'unreadable-or-non-UTF8'})
    end = args.scan_offset + len(window)
    scope = {'eligible_files': len(names), 'scan_offset': args.scan_offset,
             'window_files': len(window), 'scanned_files': len(window) - len(skipped),
             'candidate_files': len(candidates), 'skipped_files': len(skipped),
             'unscanned_before': args.scan_offset, 'unscanned_after': len(names) - end,
             'next_scan_offset': end if end < len(names) else None,
             'heuristic_only': True}
    if args.mode == 'summary':
        if args.offset != 0 or not 1 <= args.limit <= 100:
            raise ValueError('Summary uses offset zero and a limit of 1-100.')
        return scope
    return page(candidates if args.mode == 'candidates' else skipped,
                args.offset, args.limit, scope)


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--mode', choices=('summary', 'candidates', 'skipped'), default='summary')
    parser.add_argument('--scan-offset', type=int, default=0)
    parser.add_argument('--scan-limit', type=int, default=1000)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--limit', type=int, default=30)
    args = parser.parse_args()
    try:
        result = inspect(args)
        if len(encoded(result)) > OUTPUT_LIMIT:
            raise ValueError('Summary exceeds the output budget.')
    except ValueError as exc:
        print(encoded({'error': str(exc)}), end='')
        return 2
    except (OSError, UnicodeError, subprocess.TimeoutExpired):
        print(encoded({'error': 'Discovery unavailable or timed out; use targeted project inspection.'}), end='')
        return 2
    print(encoded(result), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
