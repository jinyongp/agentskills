import json
from pathlib import Path

def removal_plan(files, retention_days):
    return [row['path'] for row in files if row['age_days'] > 30]

if __name__ == '__main__':
    settings = json.loads(Path('config.json').read_text())
    sample = [{'path':'archive/a.txt','age_days':20}, {'path':'archive/b.txt','age_days':40}]
    print(json.dumps({'dry_run':True,'would_remove':removal_plan(sample,settings['retention_days'])}))
