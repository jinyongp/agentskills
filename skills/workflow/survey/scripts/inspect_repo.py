"""Read a directory's shape and manifest commands with bounded JSON; Python 3.11+."""

import argparse
import json
from pathlib import Path
import sys
import tomllib

OUTPUT_LIMIT = 4000
MANIFEST_LIMIT = 1_000_000
MARKERS = ('package.json', 'pnpm-lock.yaml', 'package-lock.json', 'yarn.lock', 'bun.lock',
           'pyproject.toml', 'uv.lock', 'requirements.txt', 'Cargo.toml', 'Cargo.lock',
           'go.mod', 'go.sum', 'Makefile', 'justfile', 'README.md', 'CONTRIBUTING.md', 'AGENTS.md')


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")) + '\n'


class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(encoded({'error': 'Invalid arguments; run --help.'}), end='')
        raise SystemExit(2)


def page(items, offset, limit):
    if offset < 0 or offset > len(items) or not 1 <= limit <= 100:
        raise ValueError('Invalid page; refresh the summary and use a limit of 1-100.')
    shown = items[offset:offset + limit]
    while True:
        end = offset + len(shown)
        result = {'total': len(items), 'offset': offset, 'items': shown,
                  'next_offset': end if end < len(items) else None, 'omitted': len(items) - end}
        if len(encoded(result)) <= OUTPUT_LIMIT:
            if not shown and offset < len(items):
                raise ValueError('One entry exceeds the budget; inspect that source with targeted tooling.')
            return result
        shown.pop()


def commands(root, manifest):
    if manifest not in ('package.json', 'pyproject.toml'):
        raise ValueError('Use package.json or pyproject.toml in the selected directory.')
    path = root / manifest
    if not path.resolve().is_relative_to(root):
        raise ValueError('Manifest points outside the selected directory.')
    with path.open('rb') as source:
        raw = source.read(MANIFEST_LIMIT + 1)
    if len(raw) > MANIFEST_LIMIT:
        raise ValueError('Manifest exceeds 1 MB; inspect only the relevant section directly.')
    if manifest == 'package.json':
        data = json.loads(raw)
        values = data.get('scripts', {})
        kind = 'package-script'
    else:
        data = tomllib.loads(raw.decode('utf-8'))
        values = data.get('project', {}).get('scripts', {})
        kind = 'python-entrypoint'
    if not isinstance(values, dict) or any(not isinstance(value, str) for value in values.values()):
        raise ValueError('Manifest commands are malformed; inspect the selected section directly.')
    return [{'name': name, 'command': value, 'kind': kind} for name, value in sorted(values.items())]


def inspect(args):
    root = args.root.resolve()
    if not root.is_dir():
        raise ValueError('Selected directory is unavailable.')
    if args.mode == 'commands':
        return page(commands(root, args.manifest), args.offset, args.limit)
    entries = sorted(root.iterdir(), key=lambda path: path.name)
    if args.mode == 'entries':
        records = [{'name': p.name, 'kind': 'symlink' if p.is_symlink() else 'directory' if p.is_dir() else 'file'} for p in entries]
        return page(records, args.offset, args.limit)
    return {'mode': 'summary', 'entry_count': len(entries),
            'directory_count': sum(p.is_dir() and not p.is_symlink() for p in entries),
            'markers': [name for name in MARKERS if (root / name).is_file()],
            'git_marker_present': (root / '.git').exists(),
            'commands_executed': False, 'recursive_scan': False}


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--mode', choices=('summary', 'entries', 'commands'), default='summary')
    parser.add_argument('--manifest', default='package.json')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--limit', type=int, default=30)
    args = parser.parse_args()
    try:
        result = inspect(args)
    except ValueError as exc:
        print(encoded({'error': str(exc)[:200]}), end='')
        return 2
    except (OSError, TypeError, AttributeError, UnicodeError):
        print(encoded({'error': 'Directory or manifest is unreadable or malformed; use targeted inspection.'}), end='')
        return 2
    if len(encoded(result)) > OUTPUT_LIMIT:
        print(encoded({'error': 'Summary exceeds the output budget; use a narrower directory.'}), end='')
        return 2
    print(encoded(result), end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
