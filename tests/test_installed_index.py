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
    def test_pages_preserve_all_intents_and_paths_without_reading_skill_bodies(self):
        with tempfile.TemporaryDirectory(prefix="agentskills-$&-'한글'-") as directory:
            root = Path(directory)
            (root / "templates").mkdir()
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
