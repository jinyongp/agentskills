"""Read worktree registry or selected worktree state with bounded JSON; Python 3.11+."""

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
    result = subprocess.run(['git', '--no-optional-locks', '-c', 'core.fsmonitor=false', '-C', str(repo), *args],
                            env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}, capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError('Git query failed; verify repository, worktree access, and Git support.')
    return result.stdout.decode('utf-8', 'surrogateescape')


def registry(repo):
    records, entry = [], {}
    for raw in git(repo, 'worktree', 'list', '--porcelain', '-z').split('\0'):
        if not raw:
            if entry:
                records.append(entry)
                entry = {}
            continue
        key, separator, value = raw.partition(' ')
        entry[key] = value if separator else True
    if entry:
        records.append(entry)
    for index, entry in enumerate(records):
        if 'worktree' not in entry:
            raise ValueError('Unsupported registry record; inspect directly with Git.')
        entry['main'] = index == 0
    return records


def page(records, offset, limit):
    if not 0 <= offset <= len(records) or not 1 <= limit <= 100:
        raise ValueError('Invalid page; refresh the registry and use a limit of 1-100.')
    shown = records[offset:offset + limit]
    while True:
        end = offset + len(shown)
        result = {'total': len(records), 'offset': offset, 'items': shown,
                  'next_offset': end if end < len(records) else None, 'omitted': len(records) - end}
        if len(encoded(result)) <= OUTPUT_LIMIT:
            if not shown and offset < len(records):
                raise ValueError('One registry entry exceeds the budget; inspect it directly with Git.')
            return result
        shown.pop()


def state(repo):
    records = iter(git(repo, 'status', '--porcelain=v2', '-z', '--untracked-files=all').split('\0'))
    counts = {'staged': 0, 'unstaged': 0, 'untracked': 0, 'conflicted': 0}
    for raw in records:
        if not raw:
            continue
        if raw.startswith('? '):
            counts['untracked'] += 1
        elif raw[0] == 'u':
            counts['conflicted'] += 1
        elif raw[0] in '12':
            xy = raw.split(' ', 2)[1]
            counts['staged'] += xy[0] != '.'
            counts['unstaged'] += xy[1] != '.'
            if raw[0] == '2':
                next(records)
        else:
            raise ValueError('Unsupported worktree status record; inspect directly with Git.')
    git_dir = Path(git(repo, 'rev-parse', '--absolute-git-dir').removesuffix('\n'))
    operations = [label for marker, label in (
        ('MERGE_HEAD', 'merge'), ('rebase-merge', 'rebase'), ('rebase-apply', 'rebase-or-am'),
        ('CHERRY_PICK_HEAD', 'cherry-pick'), ('REVERT_HEAD', 'revert'), ('sequencer', 'sequencer'),
    ) if (git_dir / marker).exists()]
    ignored = git(repo, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').split('\0')
    return {'mode': 'state', 'counts': counts, 'dirty': any(counts.values()),
            'ignored_files': sum(bool(name) for name in ignored), 'operations': operations}


def inspect(args):
    records = registry(args.repo)
    if args.mode == 'list':
        return page(records, args.offset, args.limit)
    if args.mode in ('state', 'ignored'):
        if args.path is None:
            raise ValueError('State inspection needs --path for a registered worktree.')
        selected = args.path.resolve()
        match = next((r for r in records if Path(r['worktree']).resolve() == selected), None)
        if match is None or match.get('bare') or not selected.is_dir():
            raise ValueError('Selected path is not an accessible registered checkout.')
        if args.mode == 'ignored':
            names = git(selected, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').split('\0')
            return page([{'path': name} for name in names if name], args.offset, args.limit)
        return state(selected)
    return {'mode': 'summary', 'total': len(records),
            'linked': sum(not r['main'] for r in records),
            'locked': sum('locked' in r for r in records),
            'prunable': sum('prunable' in r for r in records),
            'detached': sum('detached' in r for r in records), 'states_inspected': False}


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--mode', choices=('summary', 'list', 'state', 'ignored'), default='summary')
    parser.add_argument('--path', type=Path)
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    try:
        result = inspect(args)
        if len(encoded(result)) > OUTPUT_LIMIT:
            raise ValueError('Metadata exceeds the output budget; inspect directly with Git.')
    except ValueError as exc:
        print(encoded({'error': str(exc)[:200]}), end='')
        return 2
    except (OSError, subprocess.TimeoutExpired, StopIteration):
        print(encoded({'error': 'Worktree inspection unavailable; no mutation attempted.'}), end='')
        return 2
    print(encoded(result), end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
