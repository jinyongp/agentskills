import json
from pathlib import Path
import unittest
from preview import removal_plan

class PreviewTests(unittest.TestCase):
    def test_configured_retention(self):
        days = json.loads(Path('config.json').read_text())['retention_days']
        self.assertEqual(removal_plan([{'path':'archive/a.txt','age_days':20}], days),
                         ['archive/a.txt'] if 20 > days else [])

    def test_boundary(self):
        self.assertEqual(removal_plan([{'path':'archive/b.txt','age_days':30}], 30), [])

    def test_old_archive(self):
        self.assertEqual(removal_plan([{'path':'archive/c.txt','age_days':40}], 30), ['archive/c.txt'])
