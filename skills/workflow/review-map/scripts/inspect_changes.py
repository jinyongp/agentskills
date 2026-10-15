"""Read worktree layers or a commit comparison with bounded JSON; Python 3.11+."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

OUTPUT_LIMIT = 4000


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(',', ':')) + '\n'


class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(encoded({'error': 'Invalid arguments; run --help.'}), end='')
        raise SystemExit(2)


def git(repo, *args):
    result = subprocess.run(['git', '--no-optional-locks', '--literal-pathspecs', '-c', 'core.fsmonitor=false', '-C', str(repo), *args],
                            env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}, capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError('Git query failed; verify repository, refs, and access.')
    return result.stdout.decode('utf-8', 'surrogateescape')


def paginate(items, offset, limit, metadata):
    if not 0 <= offset <= len(items) or not 1 <= limit <= 100:
        raise ValueError('Invalid page; refresh the query.')
    shown = items[offset:offset + limit]
    while True:
        end = offset + len(shown)
        result = {**metadata, 'total': len(items), 'offset': offset, 'items': shown,
                  'next_offset': end if end < len(items) else None, 'omitted': len(items) - end}
        if len(encoded(result)) <= OUTPUT_LIMIT:
            if not shown and offset < len(items):
                raise ValueError('One entry exceeds the output budget; use targeted tooling.')
            return result
        if not shown:
            raise ValueError('Comparison metadata exceeds the output budget.')
        shown.pop()


def text_page(text, offset, metadata):
    if not 0 <= offset <= len(text):
        raise ValueError('Offset exceeds current diff length; refresh the query.')
    def page(size):
        end = offset + size
        return {**metadata, 'total_chars': len(text), 'offset': offset, 'text': text[offset:end],
                'next_offset': end if end < len(text) else None, 'omitted_chars': len(text) - end}
    low, high = 0, min(len(text) - offset, OUTPUT_LIMIT)
    while low < high:
        middle = (low + high + 1) // 2
        if len(encoded(page(middle))) <= OUTPUT_LIMIT:
            low = middle
        else:
            high = middle - 1
    if low == 0 and offset < len(text):
        raise ValueError('Diff metadata exceeds the output budget.')
    return page(low)


def inspect(args):
    repo = Path(git(args.repo, 'rev-parse', '--show-toplevel').removesuffix('\n'))
    if (args.head or args.merge_base) and not args.base:
        raise ValueError('Commit comparison needs --base.')
    for value in args.path:
        path = Path(value)
        if path.is_absolute() or '..' in path.parts or value in ('', '.'):
            raise ValueError('Paths must be relative to the repository root.')
    common = ['diff', '--no-ext-diff', '--no-textconv', '--no-color', '--no-renames', '--ignore-submodules=none']
    metadata = {'mode': args.mode}
    if args.base:
        base = git(repo, 'rev-parse', '--verify', '--end-of-options', args.base + '^{commit}').strip()
        head = git(repo, 'rev-parse', '--verify', '--end-of-options', (args.head or 'HEAD') + '^{commit}').strip()
        if args.merge_base:
            base = git(repo, 'merge-base', base, head).strip()
        metadata['comparison'] = {'base': base, 'head': head, 'merge_base': args.merge_base}
        layers = {'comparison': [base, head]}
    else:
        layers = {'staged': ['--cached'], 'working': []}
    if args.mode == 'diff':
        if not args.path or any((repo / value).is_dir() for value in args.path):
            raise ValueError('Diff needs --path naming selected files, not directories.')
        layer = 'comparison' if args.base else args.layer
        metadata['layer'] = layer
        text = git(repo, *common, *layers[layer], '--', *args.path)
        return text_page(text, args.offset, metadata)
    records = []
    for layer, options in layers.items():
        names = git(repo, *common, '--name-only', '-z', *options, '--', *args.path).split('\0')
        records.extend({'layer': layer, 'path': name} for name in names if name)
    if not args.base:
        names = git(repo, 'ls-files', '--others', '--exclude-standard', '-z', '--', *args.path).split('\0')
        records.extend({'layer': 'untracked', 'path': name} for name in names if name)
    if args.mode == 'files':
        return paginate(records, args.offset, args.limit, metadata)
    return {**metadata, 'counts': {layer: sum(r['layer'] == layer for r in records)
                                 for layer in (*layers, *(() if args.base else ('untracked',)))},
            'distinct_paths': len({r['path'] for r in records}), 'diff_in_summary': False}


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--mode', choices=('summary', 'files', 'diff'), default='summary')
    parser.add_argument('--base')
    parser.add_argument('--head')
    parser.add_argument('--merge-base', action='store_true')
    parser.add_argument('--layer', choices=('staged', 'working'), default='working')
    parser.add_argument('--path', action='append', default=[])
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--limit', type=int, default=30)
    args = parser.parse_args()
    try:
        result = inspect(args)
        if len(encoded(result)) > OUTPUT_LIMIT:
            raise ValueError('Output metadata exceeds the budget; use a narrower query.')
    except ValueError as exc:
        print(encoded({'error': str(exc)[:200]}), end='')
        return 2
    except (OSError, subprocess.TimeoutExpired):
        print(encoded({'error': 'Git is unavailable or query timed out; no mutation attempted.'}), end='')
        return 2
    print(encoded(result), end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
