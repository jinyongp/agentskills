"""Replay a parent-authored workflow trajectory; does not invoke an agent."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


def fingerprint(project):
    return {name: hashlib.sha256((project / name).read_bytes()).hexdigest()
            for name in ('core.py', 'cli.py', 'shipping.py', 'settings.json')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    project = output / 'project'
    project.mkdir()
    records = []

    def write(name, text):
        (project / name).write_text(text, encoding='utf-8')

    def check(label, command, *, expect=0, stdout=None):
        result = subprocess.run(command, cwd=project, capture_output=True, text=True,
                                timeout=30)
        (output / (label + '.log')).write_text(
            f'Command: {command!r}\nExit: {result.returncode}\n'
            f'{result.stdout}{result.stderr}', encoding='utf-8')
        records.append({'label': label, 'exit': result.returncode,
                        'command': command, 'state': fingerprint(project)})
        assert result.returncode == expect, label
        if stdout is not None:
            assert result.stdout.strip() == stdout, label
        return records[-1]

    py = sys.executable
    write('contract.md', '# Accepted contract\n\nA: CLI prints price times quantity.\n'
          'B: core.total(price, quantity) supports nonnegative integer inputs.\n'
          'C: shipping is free at subtotal 50 or more; below that use settings fee.\n'
          'Manual receipt export is deliberate; no payment provider or auto-export.\n')
    write('plan.md', '# Plan\n\nReview A, B, C. Keep manual receipts.\n'
          'Correct demonstrated defects; verify direct callers after API edits.\n')
    write('user-note.txt', 'Keep this unrelated draft.\n')
    write('core.py', 'def total(price, quantity):\n    return price + quantity\n')
    write('cli.py', 'from core import total\nimport sys\n'
          'print(total(int(sys.argv[1]), int(sys.argv[2])))\n')
    write('settings.json', '{"fee": 5}\n')
    write('shipping.py', 'import json\nfrom pathlib import Path\n'
          'def charge(subtotal):\n'
          '    fee = json.loads(Path("settings.json").read_text())["fee"]\n'
          '    return 0 if subtotal > 50 else fee\n')
    cli_hash = fingerprint(project)['cli.py']
    contract = (project / 'contract.md').read_bytes()
    first_a = check('A-first', [py, 'cli.py', '2', '2'], stdout='4')
    check('B-defect', [py, '-B', '-c',
          'from core import total; assert total(7, 3) == 21'], expect=1)

    # Deliberately faulty candidate: fixes arithmetic but breaks a caller's import.
    write('core.py', 'def line_total(price, quantity):\n    return price * quantity\n')
    check('B-candidate-pass', [py, '-B', '-c',
          'from core import line_total; assert line_total(7, 3) == 21'])
    assert fingerprint(project)['cli.py'] == cli_hash
    assert first_a['state']['core.py'] != fingerprint(project)['core.py']
    check('A-reopened-fail', [py, 'cli.py', '2', '2'], expect=1)
    write('core.py', 'def total(price, quantity):\n    return price * quantity\n')
    check('A-corrected', [py, 'cli.py', '7', '3'], stdout='21')
    check('B-corrected', [py, '-B', '-c',
          'from core import total; assert total(7, 0) == 0'])

    fee_command = [py, '-B', '-c',
                   'from shipping import charge; assert charge(49) == 5']
    fee_pass = check('C-fee-before', fee_command)
    write('settings.json', '{"fee": 8}\n')
    current_fee_hash = fingerprint(project)['settings.json']
    assert fee_pass['state']['settings.json'] != fingerprint(project)['settings.json']
    check('C-stale-expectation', fee_command, expect=1)
    check('C-current-fee', [py, '-B', '-c',
          'from shipping import charge; assert charge(49) == 8'])

    write('handoff.md', '# Handoff\n\nNext: review C inclusive free-shipping boundary.\n'
          'Context: manual receipt export remains accepted; no live integration.\n'
          'Lookups: contract.md, plan.md, settings.json.\n'
          'Evidence: ../A-corrected.log, ../B-corrected.log; fee changed 5 to 8.\n')
    # A new process recovers packet and current files; this is not a new agent.
    write('resume.py', 'from pathlib import Path\n'
          'packet = Path("handoff.md").read_text()\n'
          'print(packet)\n'
          'print(Path("contract.md").read_text())\n'
          'assert Path("../A-corrected.log").is_file()\n'
          'from shipping import charge\nassert charge(49) == 8\n'
          'assert charge(50) == 0\n')
    check('C-resume-fail', [py, '-B', 'resume.py'], expect=1)
    write('shipping.py', (project / 'shipping.py').read_text().replace(
          'subtotal > 50', 'subtotal >= 50'))
    check('C-resumed-pass', [py, '-B', 'resume.py'])
    check('C-preserved-fee', [py, '-B', '-c',
          'from shipping import charge; assert charge(49) == 8'])
    check('final-A', [py, 'cli.py', '7', '3'], stdout='21')
    check('final-B', [py, '-B', '-c',
          'from core import total; assert total(0, 3) == 0'])
    assert fingerprint(project)['cli.py'] == cli_hash
    assert (project / 'contract.md').read_bytes() == contract
    assert (project / 'user-note.txt').read_text() == 'Keep this unrelated draft.\n'
    assert fingerprint(project)['settings.json'] == current_fee_hash
    report = {'kind': 'parent-authored replay', 'python': platform.python_version(),
              'records': records, 'preserved': ['CLI source', 'accepted contract',
              'manual receipt scope', 'unrelated draft', 'current fee configuration']}
    (output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'result': 'pass', 'checks': len(records), 'output': str(output)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
