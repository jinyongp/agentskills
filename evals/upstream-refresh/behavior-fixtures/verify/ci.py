import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'ci_state'
STATE.mkdir(exist_ok=True)

def fingerprint():
    digest = hashlib.sha256()
    for name in ['pricing.py', 'config.json', 'tests/test_pricing.py']:
        digest.update(name.encode() + b'\0' + (ROOT / name).read_bytes())
    return digest.hexdigest()

def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def output(data):
    print(json.dumps(data))

action = sys.argv[1]
if action == 'latest':
    output({'target': fingerprint(), 'jobs': [json.loads(p.read_text()) for p in sorted(STATE.glob('*.json')) if not p.name.endswith('.result.json')]})
elif action == 'start':
    check = sys.argv[2]
    if check not in ['unit', 'config', 'contract']:
        raise SystemExit('Unknown check')
    job = 'job-' + uuid.uuid4().hex[:10]
    receipt = {'job_id': job, 'check': check, 'target': fingerprint(), 'state': 'queued'}
    save(STATE / f'{job}.json', receipt)
    with (STATE / 'requests.log').open('a') as audit:
        audit.write(json.dumps(receipt) + '\n')
    subprocess.Popen([sys.executable, __file__, '_work', job], cwd=ROOT,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    output(dict(receipt, dispatch='delegated_to_worker', prompt=f'Execute the {check} check.'))
elif action == '_work':
    job = sys.argv[2]
    path = STATE / f'{job}.json'
    receipt = json.loads(path.read_text())
    time.sleep(.2)
    if receipt['check'] == 'contract':
        receipt.update(state='worker_failed', error='PARTNER_SANDBOX_TOKEN is unavailable; contract command was not executed')
        save(path, receipt)
    else:
        command = ([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v']
                   if receipt['check'] == 'unit' else
                   [sys.executable, '-c', "import json; d=json.load(open('config.json')); assert d=={'currency':'EUR','schema':1}; print('Configuration valid')"])
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        save(STATE / f'{job}.result.json', dict(receipt, command=command, executed_target=fingerprint(),
             returncode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        receipt.update(state='completed', result_path=f'ci_state/{job}.result.json')
        save(path, receipt)
elif action in ['status', 'result']:
    job = sys.argv[2]
    receipt = json.loads((STATE / f'{job}.json').read_text())
    if action == 'result' and 'result_path' in receipt:
        output(json.loads((ROOT / receipt['result_path']).read_text()))
    else:
        output(receipt)
else:
    raise SystemExit('Unknown action')
