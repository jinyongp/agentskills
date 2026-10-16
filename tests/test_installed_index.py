"""Check complete bounded installed catalogs without loading skill bodies."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InstalledIndexTests(unittest.TestCase):
    def test_decisions_use_only_installed_paths_and_keep_catalog_fallback(self):
        with tempfile.TemporaryDirectory(prefix="agentskills-routing-") as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "templates", root / "templates")
            shutil.copytree(ROOT / "lib", root / "lib")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            names = ["spec-generator", "plan", "code-review", "review-loop", "custom"]
            category = root / "skills/workflow"
            category.mkdir(parents=True)
            (category / "README.md").write_text("\n".join(f"- [{name}]({name}/SKILL.md) — Task {name}." for name in names))
            available = {name: {"category": "workflow", "source": str(category / name)} for name in names}
            script = "const fs=require('node:fs'),input=JSON.parse(fs.readFileSync(0,'utf8'));" \
                     "const read=fs.readFileSync;fs.readFileSync=function(p,...args){if(String(p).endsWith('SKILL.md'))throw Error('Body read');return read.call(this,p,...args);};" \
                     "const {renderInstalledIndex}=require(process.argv[1]);process.stdout.write(JSON.stringify(renderInstalledIndex(input.root,input.entries,input.available,input.root)));"
            for selected in ([], names[:1], names[1:4], names):
                entries = [{"name": name, "path": f"../{name}/SKILL.md"} for name in selected]
                result = subprocess.run(["node", "-e", script, str(ROOT / "lib/installed-index.js")],
                                        input=json.dumps({"root": str(root), "entries": entries, "available": available}),
                                        text=True, capture_output=True, encoding="utf-8", check=True, timeout=20)
                files = json.loads(result.stdout)
                routes = {name: text for name, text in files.items() if name.startswith("references/routes/")}
                combined = "\n".join(routes.values())
                routed = set(re.findall(r"Skill: `([^`]+)`", combined))
                self.assertEqual(routed, set(selected) - {"custom"})
                self.assertEqual(set(re.findall(r"Path: `([^`]+)`", combined)),
                                 {f"../{name}/SKILL.md" for name in routed})
                for text in routes.values():
                    self.assertLessEqual(len(text.encode('utf-16-le')) // 2, 2500)
                self.assertLessEqual(len(files['SKILL.md'].split('---', 2)[2].strip()), 4000)
                if 'custom' in selected:
                    self.assertIn('1 installed skill(s) have no authored decision route', files['SKILL.md'])
                    self.assertIn('`custom`', files['references/catalog/workflow.md'])
                for name in set(names) - set(selected):
                    self.assertNotIn(f'`{name}`', combined)
            definition = json.loads((root / 'lib/skill-routes.json').read_text())[1]
            excessive = [{**definition, 'id': f'route-{n}', 'when': 'x' * 300} for n in range(20)]
            (root / 'lib/skill-routes.json').write_text(json.dumps(excessive))
            failed = subprocess.run(["node", "-e", script, str(ROOT / "lib/installed-index.js")],
                                    input=json.dumps({'root': str(root), 'entries': [{'name': 'plan', 'path': '../plan/SKILL.md'}], 'available': available}),
                                    text=True, capture_output=True, encoding='utf-8', timeout=20)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn('Index body exceeds', failed.stderr)
            self.assertLess(len(failed.stderr), 4000)

    def test_large_decision_route_recovers_exact_paths_and_rejects_invalid_definitions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'lib').mkdir()
            names = [f'skill-{n:03d}' for n in range(100)]
            paths = {name: f"../한글 $&'/{name}/SKILL.md" for name in names}
            route = {'id': 'decide', 'title': 'Choose work', 'when': 'Choose by task.',
                     'choices': [{'skill': name, 'when': 'Investigate ' + '가' * 200} for name in names]}
            source = root / 'lib/skill-routes.json'
            source.write_text(json.dumps([route]), encoding='utf-8')
            script = "const fs=require('node:fs'),x=JSON.parse(fs.readFileSync(0,'utf8'));const {renderRoutes}=require(process.argv[1]);process.stdout.write(JSON.stringify(renderRoutes(x.root,new Map(Object.entries(x.paths)),2500)));"
            arguments = ['node', '-e', script, str(ROOT / 'lib/skill-routes.js')]
            payload = json.dumps({'root': str(root), 'paths': paths})
            result = subprocess.run(arguments, input=payload, text=True, capture_output=True, encoding='utf-8', check=True, timeout=20)
            files = json.loads(result.stdout)['files']
            page, found, visited = 'references/routes/decide.md', [], set()
            while page:
                self.assertNotIn(page, visited)
                visited.add(page)
                text = files[page]
                self.assertLessEqual(len(text.encode('utf-16-le')) // 2, 2500)
                self.assertIn('of 100;', text)
                found.extend(re.findall(r'Path: `([^`]+)`', text))
                match = re.search(r'Next page: `([^`]+)`', text)
                page = match[1] if match else None
            self.assertEqual(found, list(paths.values()))
            self.assertEqual(visited, set(files))
            for invalid in (None, [route, route], [{**route, 'id': '../outside'}],
                            [{**route, 'choices': [{'skill': 'skill-000', 'when': 'bad\ncondition'}]}]):
                source.write_text(json.dumps(invalid), encoding='utf-8')
                failed = subprocess.run(arguments, input=payload, text=True, capture_output=True, encoding='utf-8', timeout=20)
                self.assertNotEqual(failed.returncode, 0)
                self.assertLess(len(failed.stderr), 4000)

    def test_pages_preserve_all_intents_and_paths_without_reading_skill_bodies(self):
        with tempfile.TemporaryDirectory(prefix="agentskills-$&-'한글'-") as directory:
            root = Path(directory)
            (root / "templates").mkdir()
            (root / "lib").mkdir()
            shutil.copyfile(ROOT / "lib/skill-routes.json", root / "lib/skill-routes.json")
            shutil.copyfile(ROOT / "templates/installed-index.md.tmpl", root / "templates/installed-index.md.tmpl")
            shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
            category = root / "skills/workflow"
            category.mkdir(parents=True)
            names = [f"skill-{n:03}" for n in range(180)]
            (category / "README.md").write_text("\n".join(f"- [{name}]({name}/SKILL.md) — Investigate " + "가" * 180 for name in names), encoding="utf-8")
            entries = [{"name": name, "path": f"../{name}/SKILL.md"} for name in names]
            available = {name: {"category": "workflow", "source": str(category / name)} for name in names}
            script = "const fs=require('node:fs');const input=JSON.parse(fs.readFileSync(0,'utf8'));" \
                     "const read=fs.readFileSync;fs.readFileSync=function(p,...args){if(String(p).endsWith('SKILL.md'))throw Error('Body read');return read.call(this,p,...args);};" \
                     "const {renderInstalledIndex}=require(process.argv[1]);process.stdout.write(JSON.stringify(renderInstalledIndex(input.root,input.entries,input.available,input.root)));"
            result = subprocess.run(["node", "-e", script, str(ROOT / "lib/installed-index.js")],
                                    input=json.dumps({"root": str(root), "entries": entries, "available": available}),
                                    capture_output=True, text=True, encoding="utf-8", timeout=20, check=True)
            files = json.loads(result.stdout)
            self.assertEqual(json.loads(re.search(r"^  catalog-base: (.+)$", files["SKILL.md"], re.MULTILINE)[1]), str(root))
            page = "references/catalog/workflow.md"
            found, paths, intentions, visited = [], [], [], set()
            while page:
                self.assertNotIn(page, visited)
                visited.add(page)
                text = files[page]
                self.assertLessEqual(len(text.encode("utf-16-le")) // 2, 2500)
                found.extend(re.findall(r"^- `([^`]+)` —", text, re.MULTILINE))
                intentions.extend(re.findall(r"^- `[^`]+` — (.+)$", text, re.MULTILINE))
                paths.extend(re.findall(r"Path: `([^`]+)`", text))
                match = re.search(r"Next page: `([^`]+)`", text)
                page = match[1] if match else None
            self.assertEqual(found, names)
            self.assertEqual(intentions, ["Investigate " + "가" * 180] * len(names))
            self.assertEqual(paths, [entry["path"] for entry in entries])
            self.assertEqual(set(files), visited | {"SKILL.md", "LICENSE"})
            adjacent = {"name": "adjacent", "path": "../adjacent/SKILL.md"}
            available["adjacent"] = {"category": "workflow-2", "source": str(root / "skills/workflow-2/adjacent")}
            mixed = subprocess.run(["node", "-e", script, str(ROOT / "lib/installed-index.js")],
                                   input=json.dumps({"root": str(root), "entries": entries + [adjacent], "available": available}),
                                   capture_output=True, text=True, encoding="utf-8", timeout=20, check=True)
            mixed_files = json.loads(mixed.stdout)
            mixed_names = [name for file, text in mixed_files.items() if file.startswith("references/")
                           for name in re.findall(r"^- `([^`]+)` —", text, re.MULTILINE)]
            self.assertCountEqual(mixed_names, names + ["adjacent"])
            entries[0]["path"] = "../" + "long-path/" * 300 + "SKILL.md"
            failure = subprocess.run(["node", "-e", script, str(ROOT / "lib/installed-index.js")],
                                     input=json.dumps({"root": str(root), "entries": entries, "available": available}),
                                     capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assertNotEqual(failure.returncode, 0)
            self.assertLess(len(failure.stderr), 4000)
