"""Replay completed parent tasks against explicit fixture contracts; no agent call."""
import argparse
import cProfile
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc


FIXTURES = Path(__file__).parent / 'fixtures'


def load(name):
    spec = importlib.util.spec_from_file_location(name, FIXTURES / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def rejects(action, exception):
    try:
        action()
    except exception:
        return
    raise AssertionError(f'expected {exception.__name__}')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args, cwd, evidence, label, *, code=0, stdin=None):
    completed = subprocess.run(
        args, cwd=cwd, input=stdin, text=True, capture_output=True, timeout=60,
        env={**os.environ, 'npm_config_cache': str(evidence / 'npm-cache')},
    )
    (evidence / f'{label}.log').write_text(
        f'Command: {args!r}\nExit: {completed.returncode}\n'
        f'Stdout:\n{completed.stdout}\nStderr:\n{completed.stderr}',
        encoding='utf-8',
    )
    require(completed.returncode == code, f'{label}: unexpected exit; see saved log')
    return completed


def docs(work, evidence):
    target = work / 'docs'
    target.mkdir()
    for name in ('cli.py', 'guide.md'):
        shutil.copyfile(FIXTURES / name, target / name)
    before = digest(target / 'cli.py')
    valid = command([sys.executable, 'cli.py'], target, evidence, 'docs-valid', stdin='[2,3,0]')
    require(json.loads(valid.stdout) == {'total': 5}, 'documented successful result')
    empty = command([sys.executable, 'cli.py'], target, evidence, 'docs-empty', stdin='[]')
    require(json.loads(empty.stdout) == {'total': 0}, 'empty input result')
    for label, data in (('negative', '[-1]'), ('boolean', '[true]'),
                        ('object', '{}'), ('malformed', '[')):
        failed = command([sys.executable, 'cli.py'], target, evidence, f'docs-{label}',
                         code=2, stdin=data)
        require(failed.stderr and not failed.stdout, 'failure channel and exit contract')
    # Exercise the literal documented pipeline, not just a similar direct call.
    pipeline = command(['bash', '-c', "set -o pipefail; printf '%s\\n' '[2, 3, 0]' | python3 cli.py"],
                       target, evidence, 'docs-pipeline')
    require(json.loads(pipeline.stdout) == {'total': 5}, 'literal documented command result')
    require(digest(target / 'cli.py') == before, 'documentation task changed implementation')
    return {'status': 'pass', 'executed_inputs': 7, 'implementation_unchanged': True}


def dependencies(work, evidence):
    target = work / 'dependencies'
    target.mkdir()

    def pack(name, version, source, peers=None):
        folder = target / f'{name}-{version}'
        folder.mkdir()
        manifest = {'name': name, 'version': version, 'main': 'index.js'}
        if peers:
            manifest['peerDependencies'] = peers
        (folder / 'package.json').write_text(json.dumps(manifest), encoding='utf-8')
        (folder / 'index.js').write_text(source, encoding='utf-8')
        packed = command(['npm', 'pack', '--ignore-scripts', '--json'], folder, evidence,
                         f'pack-{name}-{version}')
        path = folder / json.loads(packed.stdout)[0]['filename']
        return 'file:' + str(path)

    core1 = pack('local-core', '1.0.0', 'exports.format = value => `value:${value}`;')
    core2 = pack('local-core', '2.0.0',
                 "exports.format = input => { if (!input || typeof input !== 'object') "
                 "throw new TypeError('object required'); return `value:${input.value}`; };")
    adapter1 = pack('local-adapter', '1.0.0', "exports.ready = true;", {'local-core': '^1.0.0'})
    adapter2 = pack('local-adapter', '2.0.0', "exports.ready = true;", {'local-core': '^2.0.0'})
    unrelated = pack('local-unrelated', '1.0.0', 'exports.ready = true;')
    app = target / 'app'
    app.mkdir()
    sentinel = app / 'user-notes.txt'
    sentinel.write_text('Preserve this existing user change.\n', encoding='utf-8')
    sentinel_hash = digest(sentinel)

    def manifest(core, adapter):
        (app / 'package.json').write_text(json.dumps({
            'name': 'fixture-app', 'version': '1.0.0', 'private': True,
            'dependencies': {'local-core': core, 'local-adapter': adapter,
                             'local-unrelated': unrelated},
        }), encoding='utf-8')

    def npm(operation, label, code=0):
        return command(['npm', operation, '--offline', '--ignore-scripts',
                        '--no-audit', '--no-fund'], app, evidence, label, code=code)

    manifest(core1, adapter1)
    npm('install', 'dependency-baseline-install')
    old_client = "console.log(require('local-core').format('ok'));\n"
    (app / 'app.js').write_text(old_client, encoding='utf-8')
    result = command(['node', 'app.js'], app, evidence, 'dependency-baseline-app')
    require(result.stdout.strip() == 'value:ok', 'original consumer result')
    old_lock = json.loads((app / 'package-lock.json').read_text())
    unrelated_entry = old_lock['packages']['node_modules/local-unrelated']
    manifest(core2, adapter1)
    warning = npm('install', 'dependency-peer-warning')
    require('overriding peer dependency' in warning.stderr, 'peer warning not observed')
    invalid = command(['npm', 'ls', '--all', '--json'], app, evidence,
                      'dependency-invalid-installed-tree', code=1)
    require('invalid' in invalid.stdout, 'successful install did not expose invalid peer')
    lock_hash = digest(app / 'package-lock.json')
    failed = command(['npm', 'install', '--strict-peer-deps', '--offline',
                      '--ignore-scripts', '--no-audit', '--no-fund'], app, evidence,
                     'dependency-peer-conflict', code=1)
    require('ERESOLVE' in failed.stderr, 'expected strict peer resolution conflict')
    require(digest(app / 'package-lock.json') == lock_hash, 'failed update changed old lock')
    require(digest(sentinel) == sentinel_hash, 'failure overwrote existing user work')
    # The adapter must move with the explicitly requested major core upgrade.
    manifest(core2, adapter2)
    npm('install', 'dependency-compatible-group')
    runtime_failure = command(['node', 'app.js'], app, evidence,
                              'dependency-installed-runtime-failure', code=1)
    require('object required' in runtime_failure.stderr, 'missed required consumer migration')
    (app / 'app.js').write_text(
        "console.log(require('local-core').format({value: 'ok'}));\n", encoding='utf-8',
    )
    result = command(['node', 'app.js'], app, evidence, 'dependency-migrated-app')
    require(result.stdout.strip() == 'value:ok', 'consumer result changed')
    new_lock = json.loads((app / 'package-lock.json').read_text())
    require(new_lock['packages']['node_modules/local-unrelated'] == unrelated_entry,
            'unrelated resolved dependency changed')
    npm('ci', 'dependency-clean-install')
    result = command(['node', 'app.js'], app, evidence, 'dependency-clean-app')
    require(result.stdout.strip() == 'value:ok', 'clean install runtime result')
    require(digest(sentinel) == sentinel_hash, 'update overwrote existing user work')
    return {'status': 'pass', 'core_versions': ['1.0.0', '2.0.0'],
            'peer_warning_exit_zero_observed': True, 'invalid_peer_tree_observed': True,
            'strict_peer_conflict_observed': True, 'install_success_runtime_failure_observed': True,
            'consumer_migration_verified': True, 'unrelated_resolution_preserved': True,
            'clean_install_verified': True, 'lifecycle_scripts': 'disabled in owned fixtures'}


def optimization(work, evidence):
    before, after = load('join_before').join, load('join_after').join
    cases = [([], [], []), ([9, 9], [], [(9, None), (9, None)]),
             ([2, 1, 2, 0], [{'id': 1, 'label': 'first'}, {'id': 1, 'label': 'later'},
                              {'id': 2, 'label': ''}, {'id': 0, 'label': 0}],
              [(2, ''), (1, 'first'), (2, ''), (0, 0)])]
    for ids, rows, expected in cases:
        require(before(ids, rows) == expected, 'baseline violates fixture contract')
        require(after(ids, rows) == expected, 'candidate changes order/duplicates/missing values')
    # Negative control: a last-wins index must fail the independently specified case.
    wrong = {row['id']: row['label'] for row in cases[-1][1]}
    require([(key, wrong.get(key)) for key in cases[-1][0]] != cases[-1][2],
            'duplicate-value oracle cannot detect a plausible regression')
    rows = [{'id': key, 'label': f'label-{key}'} for key in range(2500)]
    ids = list(reversed(range(2000)))
    expected = [(key, f'label-{key}') for key in ids]
    profile = cProfile.Profile()
    profile.runcall(before, ids, rows)
    profile.dump_stats(str(evidence / 'join-before.prof'))
    samples = {'before': [], 'after': []}
    functions = {'before': before, 'after': after}
    for function in functions.values():
        require(function(ids, rows) == expected, 'warmup result')
    for turn in range(7):
        for name in (('before', 'after') if turn % 2 == 0 else ('after', 'before')):
            start = time.perf_counter_ns()
            result = functions[name](ids, rows)
            samples[name].append((time.perf_counter_ns() - start) / 1_000_000)
            require(result == expected, 'timed result violates contract')
    peaks = {}
    for name, function in functions.items():
        tracemalloc.start()
        result = function(ids, rows)
        peaks[name] = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        require(result == expected, 'memory sample result')
    # No timing assertion: measurement variation is not a skill correctness failure.
    supported = max(samples['after']) < min(samples['before'])
    return {'status': 'pass', 'correctness_cases': 3, 'negative_control_detected': True,
            'workload': {'catalog_rows': len(rows), 'query_ids': len(ids)},
            'boundary': 'complete function call including index construction',
            'elapsed_ms': samples, 'median_ms': {key: statistics.median(value)
                                              for key, value in samples.items()},
            'traced_peak_bytes': peaks,
            'performance_conclusion': 'observed local improvement' if supported else 'inconclusive',
            'production_inference': False}


def migration(work, evidence):
    module = load('migration')
    path = work / 'migration.sqlite'
    db = module.connect(path)
    try:
        db.executescript('CREATE TABLE items (id INTEGER PRIMARY KEY, old_label TEXT NOT NULL);'
                         'CREATE TABLE progress (id INTEGER PRIMARY KEY, last_id INTEGER);'
                         'INSERT INTO progress VALUES (1, 0);')
        db.executemany('INSERT INTO items VALUES (?, ?)', [(key, f'label-{key}') for key in range(1, 9)])
        original = db.execute('SELECT * FROM items ORDER BY id').fetchall()
        db.execute('ALTER TABLE items ADD COLUMN new_label TEXT')
        db.execute("UPDATE items SET new_label = 'owner-updated' WHERE id = 3")

        def snapshot():
            return (db.execute('SELECT * FROM items ORDER BY id').fetchall(),
                    db.execute('SELECT * FROM progress').fetchall())

        initial = snapshot()
        rejects(lambda: module.batch(db, fail_after=2), RuntimeError)
        require(snapshot() == initial, 'interruption did not roll back data and checkpoint')
        module.batch(db)
        db.close()
        db = module.connect(path)
        while module.batch(db):
            pass
        completed = snapshot()
        require(not module.batch(db) and snapshot() == completed, 'completed retry changed data')
        require(db.execute('SELECT id, old_label FROM items ORDER BY id').fetchall() == original,
                'old consumer data changed')
        expected = [(key, 'owner-updated' if key == 3 else label) for key, label in original]
        require(db.execute('SELECT id, COALESCE(new_label, old_label) FROM items ORDER BY id').fetchall()
                == expected, 'new consumer contract or owned target violated')
        db.execute("INSERT INTO items VALUES (0, 'late-row', NULL)")
        require(not module.batch(db) and module.missing(db) == 1,
                'cursor-complete negative control did not expose missing data')
        module.reconcile(db)
        require(module.missing(db) == 0, 'reconciliation failed')
        # Verify a backup by restoring it and reading values, not by file existence.
        backup_path = work / 'backup.sqlite'
        restored = module.connect(backup_path)
        try:
            db.backup(restored)
            require(restored.execute('SELECT * FROM items ORDER BY id').fetchall()
                    == db.execute('SELECT * FROM items ORDER BY id').fetchall(), 'restored values differ')
        finally:
            restored.close()
        return {'status': 'pass', 'sqlite_version': sqlite3.sqlite_version,
                'interruption_atomic': True, 'reopen_resume': True, 'retry_preserves_data': True,
                'late_row_gap_detected': True, 'reconciliation_verified': True,
                'disposable_backup_readback_verified': True, 'real_concurrent_writers': False}
    finally:
        db.close()


def api(work, evidence):
    source_hash = digest(FIXTURES / 'api.py')
    module = load('api')
    require(module.consumer(module.provider()) == ('item-1', 'ready'), 'current consumer failed')
    rejects(lambda: module.consumer(module.provider(proposed=True)), ValueError)
    require(digest(FIXTURES / 'api.py') == source_hash, 'review task edited provider')
    return {'status': 'pass', 'current_provider_consumer_pass': True,
            'proposed_additive_break_observed': True, 'review_only_source_unchanged': True,
            'transport': 'in-process JSON serialization and decoding; no HTTP server'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='fresh evidence directory')
    options = parser.parse_args()
    options.output.mkdir(parents=True, exist_ok=False)
    report = {'kind': 'parent-authored task replay; no independent agent invocation',
              'environment': {'python': platform.python_version(), 'platform': platform.platform()},
              'fixture_sha256': {str(path.relative_to(FIXTURES)): digest(path)
                                 for path in sorted(FIXTURES.iterdir()) if path.is_file()}, 'tasks': {}}
    try:
        for tool in ('node', 'npm'):
            report['environment'][tool] = command([tool, '--version'], FIXTURES, options.output,
                                                  f'version-{tool}').stdout.strip()
        report['environment']['shell_python'] = command(
            ['python3', '--version'], FIXTURES, options.output, 'version-shell-python',
        ).stdout.strip()
        with tempfile.TemporaryDirectory(prefix='agentskills-task-replay-') as directory:
            for name, task in (('dev-docs', docs), ('dependency-update', dependencies),
                               ('optimize', optimization), ('db-migrate', migration), ('api-design', api)):
                try:
                    report['tasks'][name] = task(Path(directory), options.output)
                except Exception as error:
                    report['tasks'][name] = {'status': 'fail', 'error': str(error)}
                    raise
    finally:
        (options.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'statuses': {key: value['status'] for key, value in report['tasks'].items()},
                          'report': str(options.output.resolve() / 'report.json')}))


if __name__ == '__main__':
    main()
