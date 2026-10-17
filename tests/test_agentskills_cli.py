"""Exercise CLI installation ownership and updates through real Node subprocesses."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import stat
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]


def is_connection(file):
    try:
        info = file.lstat()
        return stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", None) == getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", -1)
    except FileNotFoundError:
        return False


class AgentskillsCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agentskills 한글's ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source"
        self.project = self.root / "project"
        self.home = self.root / "home"
        for directory in (self.source, self.project, self.home):
            directory.mkdir()
        shutil.copyfile(ROOT / "agentskills.js", self.source / "agentskills.js")
        shutil.copyfile(ROOT / "package.json", self.source / "package.json")
        shutil.copyfile(ROOT / "LICENSE", self.source / "LICENSE")
        shutil.copytree(ROOT / "lib", self.source / "lib")
        (self.source / "templates").mkdir()
        shutil.copyfile(ROOT / "templates/installed-index.md.tmpl", self.source / "templates/installed-index.md.tmpl")
        (self.source / "rules").mkdir()
        (self.source / "rules/base.md").write_text("# Shared rules\nRespect agreed scope.\n", encoding="utf-8", newline="\n")
        for name in ("alpha", "beta"):
            skill = self.source / "skills/workflow" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\nInitial guidance.\n", encoding="utf-8", newline="\n")
            (skill / "LICENSE").write_text("Fixture license\n", encoding="utf-8", newline="\n")
            (skill / "references").mkdir()
            (skill / "references/detail.md").write_text("Bundled detail\n", encoding="utf-8", newline="\n")
        self.cli = self.source / "agentskills.js"
        self.env = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home), "PYTHONUTF8": "1"}
        resolved = subprocess.run(["node", "-p", "require('node:os').homedir()"],
                                  env=self.env, capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(Path(resolved.stdout.strip()).resolve(), self.home.resolve())

    def connection(self, target, destination):
        # Real junctions need no Windows symlink privilege or Developer Mode.
        subprocess.run(["node", "-e", "const fs=require('node:fs'),p=require('node:path');"
                        "fs.symlinkSync(p.resolve(process.argv[1]),process.argv[2],"
                        "process.platform==='win32'?'junction':'dir');", str(target), str(destination)],
                       check=True, env=self.env, capture_output=True)

    def unlink_connection(self, destination):
        subprocess.run(["node", "-e", "require('node:fs').rmSync(process.argv[1],{recursive:true,force:true})",
                        str(destination)], check=True, env=self.env, capture_output=True)

    def preload(self, file):
        return {"NODE_OPTIONS": f'--require="{file.as_posix()}"'}

    def run_cli(self, command, *args, success=True, env_extra=None):
        result = subprocess.run(
            ["node", str(self.cli), command, *args, *(["--yes"] if command in ("add", "update", "remove") else [])],
            cwd=self.project,
            env={**self.env, **(env_extra or {})},
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def skill(self, name, global_scope=False):
        return (self.home / ".codex/skills" if global_scope else self.project / ".agents/skills") / name

    def legacy_install(self, names=("alpha", "beta"), global_scope=True):
        base = self.home if global_scope else self.project
        state = {"version": 1, "agents": {}}
        for agent in ("codex", "claude"):
            record = {"skills": {}}
            state["agents"][agent] = record
            directory = ".agents/skills" if agent == "codex" and not global_scope else f".{agent}/skills"
            for name in names:
                target = base / directory / name
                shutil.copytree(self.source / "skills/workflow" / name, target)
                record["skills"][name] = {
                    file.relative_to(target).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
                    for file in target.rglob("*") if file.is_file()
                }
        state_file = base / (".local/share/agentskills/install.json" if global_scope else ".agents/agentskills.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(state), encoding="utf-8", newline="\n")
        return state_file

    def test_shared_source_updates_all_connections_and_survives_partial_removal(self):
        for global_scope in (False, True):
            with self.subTest(global_scope=global_scope):
                scope = ["--global"] if global_scope else []
                base = self.home if global_scope else self.project
                self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules", *scope)
                shared = base / ".agents/skills/alpha"
                inode = shared.stat().st_ino
                self.run_cli("add", "--agent", "claude", "--skill", "alpha", "--no-rules", *scope)
                claude = base / ".claude/skills/alpha"
                codex = self.skill("alpha", global_scope)
                self.assertEqual(shared.stat().st_ino, inode)
                self.assertFalse(is_connection(shared))
                self.assertTrue(is_connection(claude))
                self.assertEqual(claude.resolve(), shared)
                self.assertEqual(is_connection(codex), global_scope)
                (self.source / "skills/workflow/alpha/SKILL.md").write_text(f"Updated {global_scope}\n", encoding="utf-8", newline="\n")
                result = self.run_cli("update", "--agent", "codex", "--no-rules", *scope)
                self.assertIn("Update (1): alpha", result.stdout)
                self.assertEqual((claude / "SKILL.md").read_text(encoding="utf-8"), f"Updated {global_scope}\n")
                self.run_cli("remove", "--agent", "codex", "--no-rules", *scope)
                self.assertTrue(shared.exists())
                self.assertTrue(claude.exists())
                if global_scope:
                    self.assertFalse(is_connection(codex))
                self.run_cli("remove", "--agent", "claude", "--no-rules", *scope)
                self.assertFalse(shared.exists())
                self.assertFalse(is_connection(claude))

    def test_legacy_update_consolidates_both_agents_in_each_scope(self):
        for global_scope in (False, True):
            with self.subTest(global_scope=global_scope):
                state_file = self.legacy_install(names=("alpha",), global_scope=global_scope)
                scope = ["--global"] if global_scope else []
                base = self.home if global_scope else self.project
                self.run_cli("update", "--agent", "codex", "--skill", "alpha", "--no-rules", *scope)
                state = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertEqual(state["version"], 2)
                self.assertEqual(set(state["skills"]), {"alpha", "index"})
                for agent in ("codex", "claude"):
                    self.assertEqual(state["agents"][agent]["skills"], {"alpha": True, **({"index": True} if agent == "codex" else {})})
                    self.assertNotIn("legacy", state["agents"][agent])
                self.assertTrue(is_connection(base / ".claude/skills/alpha"))
                self.assertEqual((base / ".claude/skills/alpha").resolve(), base / ".agents/skills/alpha")
                self.assertEqual((self.skill("alpha", global_scope) / "LICENSE").read_text(encoding="utf-8"), "Fixture license\n")

    def test_migration_record_failure_restores_copies_and_retry_keeps_progress(self):
        state_file = self.legacy_install()
        original = state_file.read_bytes()
        preload = self.root / "fail-migration.cjs"
        for failure in (1, 2):
            preload.write_text(
                "const fs=require('node:fs');const rename=fs.renameSync;let count=0;"
                f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state_file))}&&++count==={failure})"
                "{throw new Error('Injected record failure');}return rename.apply(this,arguments);};\n"
            , encoding="utf-8", newline="\n")
            self.run_cli("update", "--agent", "codex", "--global", "--no-rules", success=False,
                         env_extra=self.preload(preload))
            if failure == 1:
                self.assertEqual(state_file.read_bytes(), original)
            else:
                state = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertEqual(set(state["skills"]), {"alpha"})
                self.assertEqual(set(state["agents"]["claude"]["legacy"]), {"beta"})
                self.assertTrue(is_connection(self.skill("alpha", True)))
            for agent in ("codex", "claude"):
                beta = self.home / f".{agent}/skills/beta"
                self.assertTrue(beta.is_dir())
                self.assertFalse(is_connection(beta))
        self.run_cli("update", "--global", "--no-rules")
        for name in ("alpha", "beta"):
            self.assertTrue(is_connection(self.skill(name, True)))
            self.assertTrue(is_connection(self.home / f".claude/skills/{name}"))

    def test_migration_rejects_foreign_source_and_cannot_fall_back_to_copies(self):
        state_file = self.legacy_install(names=("alpha",))
        before = state_file.read_bytes()
        shared = self.home / ".agents/skills/alpha"
        shutil.copytree(self.source / "skills/workflow/alpha", shared)
        self.run_cli("update", "--global", "--no-rules", success=False)
        self.assertEqual(state_file.read_bytes(), before)
        shutil.rmtree(shared)
        preload = self.root / "deny-symlink.cjs"
        preload.write_text("require('node:fs').symlinkSync=()=>{throw new Error('Links unavailable');};\n", encoding="utf-8", newline="\n")
        self.run_cli("update", "--global", "--no-rules", success=False,
                     env_extra=self.preload(preload))
        self.assertFalse(shared.exists())
        self.assertEqual(state_file.read_bytes(), before)
        self.assertFalse(is_connection(self.skill("alpha", True)))

    def test_update_checks_other_agents_links_and_shared_edits(self):
        for agent in ("codex", "claude"):
            self.run_cli("add", "--agent", agent, "--skill", "alpha", "--no-rules")
        claude = self.project / ".claude/skills/alpha"
        link = os.readlink(claude)
        foreign = self.root / "foreign"
        foreign.mkdir()
        (foreign / "note").write_text("Preserve\n", encoding="utf-8", newline="\n")
        self.unlink_connection(claude)
        self.connection(foreign, claude)
        self.run_cli("update", "--agent", "codex", "--no-rules", success=False)
        self.run_cli("remove", "--agent", "codex", "--no-rules", success=False)
        self.assertEqual((foreign / "note").read_text(encoding="utf-8"), "Preserve\n")
        self.unlink_connection(claude)
        self.connection(Path(os.path.abspath(claude.parent / link)), claude)
        (claude / "SKILL.md").write_text("User edit through Claude\n", encoding="utf-8", newline="\n")
        self.run_cli("update", "--agent", "codex", "--no-rules", success=False)
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_text(encoding="utf-8"), "User edit through Claude\n")

    def test_legacy_removal_leaves_other_copy_available_for_migration(self):
        state_file = self.legacy_install(names=("alpha",), global_scope=False)
        self.run_cli("remove", "--agent", "codex", "--no-rules")
        self.assertFalse(self.skill("alpha").exists())
        claude = self.project / ".claude/skills/alpha"
        self.assertTrue(claude.is_dir())
        self.assertFalse(is_connection(claude))
        self.run_cli("update", "--agent", "claude", "--skill", "alpha", "--no-rules")
        self.assertTrue(is_connection(claude))
        self.assertEqual(claude.resolve(), self.skill("alpha"))
        self.assertEqual(set(json.loads(state_file.read_text(encoding="utf-8"))["skills"]), {"alpha", "index"})

    def test_missing_shared_source_requires_explicit_record_removal(self):
        for agent in ("codex", "claude"):
            self.run_cli("add", "--agent", agent, "--global", "--skill", "alpha", "--no-rules")
        shutil.rmtree(self.home / ".agents/skills/alpha")
        self.run_cli("update", "--global", "--no-rules", success=False)
        self.run_cli("remove", "--global", "--no-rules")
        for agent in ("codex", "claude"):
            self.assertFalse(is_connection(self.home / f".{agent}/skills/alpha"))
        state = json.loads((self.home / ".local/share/agentskills/install.json").read_text(encoding="utf-8"))
        self.assertEqual(state["skills"], {})

    def test_existing_absolute_connection_is_reused_without_rewriting(self):
        self.run_cli("add", "--agent", "claude", "--skill", "alpha", "--no-rules")
        link = self.project / ".claude/skills/alpha"
        self.unlink_connection(link)
        self.connection(self.skill("alpha"), link)
        before = link.lstat().st_mtime_ns
        result = self.run_cli("update", "--no-rules")
        self.assertIn("Already up to date", result.stdout)
        self.assertEqual(link.lstat().st_mtime_ns, before)
        self.run_cli("remove", "--no-rules")
        self.assertFalse(is_connection(link))

    def test_link_probe_failure_prevents_all_selected_changes(self):
        preload = self.root / "deny-links.cjs"
        preload.write_text("require('node:fs').symlinkSync=()=>{throw new Error('Links unavailable');};\n",
                           encoding="utf-8", newline="\n")
        result = self.run_cli("add", "--agent", "claude", success=False, env_extra=self.preload(preload))
        self.assertIn("destination volume", result.stderr)
        self.assertIn(str(self.project / ".agents"), result.stderr)
        self.assertFalse(self.skill("alpha").exists())
        self.assertFalse(self.skill("beta").exists())
        self.assertFalse((self.project / "CLAUDE.md").exists())
        self.assertFalse((self.project / ".agents/agentskills.json").exists())
        self.assertEqual(list((self.project / ".agents").iterdir()), [])

    def test_connection_staging_failure_preserves_legacy_installation(self):
        record = self.legacy_install(names=("alpha",))
        before = record.read_bytes()
        preload = self.root / "fail-staged-link.cjs"
        preload.write_text(
            "const fs=require('node:fs'),link=fs.symlinkSync;"
            "fs.symlinkSync=function(a,b){if(!b.includes('.agentskills-link-probe-'))"
            "throw new Error('Injected staging failure');return link.apply(this,arguments);};\n",
            encoding="utf-8", newline="\n")
        result = self.run_cli("update", "--global", "--skill", "alpha", "--no-rules", success=False, env_extra=self.preload(preload))
        self.assertIn("Completed 0/", result.stderr)
        self.assertEqual(record.read_bytes(), before)
        for agent in ("codex", "claude"):
            directory = self.home / f".{agent}/skills/alpha"
            self.assertFalse(is_connection(directory))
            self.assertEqual((directory / "LICENSE").read_text(encoding="utf-8"), "Fixture license\n")
        self.assertFalse((self.home / ".agents/skills/alpha").exists())

    @unittest.skipUnless(os.name == "nt", "Windows path namespace and junction behavior")
    def test_windows_namespace_and_drive_case_connection_remains_unchanged(self):
        self.run_cli("add", "--agent", "claude", "--skill", "alpha", "--no-rules")
        link = self.project / ".claude/skills/alpha"
        shared = str(self.skill("alpha"))
        self.unlink_connection(link)
        self.connection(Path("\\\\?\\" + shared[0].lower() + shared[1:]), link)
        result = self.run_cli("update", "--no-rules")
        self.assertIn("Already up to date", result.stdout)
        self.assertEqual(link.resolve(), self.skill("alpha").resolve())

    def test_rule_replace_failure_restores_original_and_record(self):
        rules = self.project / "AGENTS.md"
        rules.write_bytes(b"# Existing\r\nKeep exact bytes\r\n")
        self.run_cli("add", "--agent", "codex", "--rules-only")
        before = rules.read_bytes()
        record = self.project / ".agents/agentskills.json"
        original_record = record.read_bytes()
        (self.source / "rules/base.md").write_text("Changed rules\n", encoding="utf-8", newline="\n")
        preload = self.root / "fail-rules-rename.cjs"
        preload.write_text(
            "const fs=require('node:fs'),rename=fs.renameSync;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(rules))}&&a.endsWith('.tmp'))"
            "{const e=new Error('File in use');e.code='EPERM';throw e;}return rename.apply(this,arguments);};\n",
            encoding="utf-8", newline="\n")
        self.run_cli("update", success=False, env_extra=self.preload(preload))
        self.assertEqual(rules.read_bytes(), before)
        self.assertEqual(record.read_bytes(), original_record)
        self.assertEqual(list(self.project.glob("AGENTS.md.*")), [])

    def test_partial_skill_copy_failure_preserves_installed_version(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        record = self.project / ".agents/agentskills.json"
        before = record.read_bytes()
        original = (self.skill("alpha") / "SKILL.md").read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New version\n", encoding="utf-8", newline="\n")
        preload = self.root / "fail-copy.cjs"
        preload.write_text("const fs=require('node:fs'),copy=fs.copyFileSync;let n=0;"
                           "fs.copyFileSync=function(){if(++n===2)throw new Error('Copy failed');"
                           "return copy.apply(this,arguments);};\n", encoding="utf-8", newline="\n")
        self.run_cli("update", "--no-rules", success=False, env_extra=self.preload(preload))
        self.assertEqual(record.read_bytes(), before)
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_bytes(), original)
        self.assertEqual({p.name for p in self.skill("alpha").parent.iterdir()}, {"alpha", "index"})

    def test_help_examples_execute_with_current_catalog_and_package_entrypoint(self):
        package_file = self.source / "package.json"
        package = json.loads(package_file.read_text(encoding="utf-8"))
        package["bin"] = {"fixture-skills": "agentskills.js"}
        package_file.write_text(json.dumps(package), encoding="utf-8", newline="\n")
        for old, new in (("alpha", "delta"), ("beta", "epsilon")):
            directory = self.source / "skills/workflow" / old
            directory.rename(directory.with_name(new))
        for topic in (None, "add", "update", "remove", "list"):
            result = self.run_cli(topic, "--help") if topic else self.run_cli("--help")
            examples = result.stdout.split("Examples:\n", 1)[1].split("\n\n", 1)[0].splitlines()
            for example in examples:
                with self.subTest(topic=topic, example=example):
                    self.run_cli("add", "--agent", "codex")
                    self.run_cli("add", "--agent", "codex", "--global")
                    binary, command, *args = shlex.split(example)
                    self.assertEqual(binary, "fixture-skills.cmd" if os.name == "nt" else "fixture-skills")
                    if command == "add" and "--agent" not in args:
                        args += ["--agent", "codex"]
                    self.run_cli(command, *args)
                    state = json.loads((self.project / ".agents/agentskills.json").read_text(encoding="utf-8"))
                    expected = {"epsilon"} if command == "remove" and "--skill" in args else {"delta", "epsilon"}
                    self.assertEqual(set(state["agents"]["codex"]["skills"]), expected | {"index"})
                    self.run_cli("remove")
                    if command != "remove" or "--global" not in args:
                        self.run_cli("remove", "--global")

    def test_noninteractive_retry_preserves_scope_selection_and_shell_quoting(self):
        project = self.root / "project's retry space"
        project.mkdir()
        for scope_args, base in ((["--global"], self.home), (["--project", str(project)], project)):
            with self.subTest(scope=scope_args):
                result = subprocess.run(
                    ["node", str(self.cli), "add", "-a", "claude", *scope_args, "-s", "beta", "--no-rules"],
                    cwd=self.project, env=self.env,
                    stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", timeout=20,
                )
                self.assertNotEqual(result.returncode, 0)
                advice = result.stderr.split("Retry with ", 1)[1].split(", or run in a terminal", 1)[0]
                if os.name == "nt":
                    script = "function agentskills.cmd { & node '" + str(self.cli).replace("'", "''") + "' @args }; " + advice
                    result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
                                            cwd=self.project, env=self.env, capture_output=True, timeout=20)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                else:
                    _, command, *args = shlex.split(advice)
                    self.run_cli(command, *args)
                installed = base / ".claude/skills"
                self.assertEqual({entry.name for entry in installed.iterdir()}, {"beta", "index"})
                rules = base / (".claude/CLAUDE.md" if base == self.home else "CLAUDE.md")
                self.assertFalse(rules.exists())
                self.assertFalse((self.project / ".claude").exists())

    def test_aliases_install_selected_global_skill_and_list_rejects_mutation_flags(self):
        self.run_cli("add", "-a", "codex", "-g", "-s", "beta", "-y", "--no-rules")
        self.assertTrue(self.skill("beta", global_scope=True).exists())
        self.assertFalse(self.skill("alpha", global_scope=True).exists())
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())
        for args in (("--yes",), ("--skill", "beta"), ("--rules-only",)):
            self.run_cli("list", *args, success=False)
        self.run_cli("list", "-a", "codex", "-g")

    def confirm_after(self, args, mutate, response=b"y\n", wait_for=None):
        if wait_for is None:
            wait_for = b"Apply? [y/N]" if args[0] == "remove" else b"Apply? [Y/n]"
        if os.name == "nt":
            from windows_terminal import confirm_after
            return confirm_after(["node", str(self.cli), *args], self.project, self.env, mutate, response, wait_for)
        import pty
        import select

        master, slave = pty.openpty()
        process = subprocess.Popen(
            ["node", str(self.cli), *args], cwd=self.project,
            stdin=slave, stdout=slave, stderr=slave, env=self.env,
        )
        os.close(slave)
        try:
            output = b""
            deadline = time.monotonic() + 10
            while wait_for not in output:
                self.assertLess(time.monotonic(), deadline, output)
                if select.select([master], [], [], 0.1)[0]:
                    output += os.read(master, 65536)
            mutate()
            os.write(master, response)
            return process.wait(timeout=10)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            os.close(master)

    def test_round_trip_updates_saved_selections_and_preserves_project_prose(self):
        original = b"# Project instructions\n\nPreserve this exact text, without a final newline."
        rules = self.project / "AGENTS.md"
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        self.assertFalse(self.skill("beta").exists())
        self.assertEqual((self.skill("alpha") / "LICENSE").read_text(encoding="utf-8"), "Fixture license\n")
        self.run_cli("add", "--agent", "codex", "--skill", "beta")
        source = self.source / "skills/workflow/alpha"
        (source / "references/detail.md").unlink()
        (source / "references/new.md").write_text("Changed public guidance\n", encoding="utf-8", newline="\n")
        (self.source / "rules/base.md").write_text("New shared rules\n", encoding="utf-8", newline="\n")
        self.run_cli("update")
        self.assertFalse((self.skill("alpha") / "references/detail.md").exists())
        self.assertEqual((self.skill("alpha") / "references/new.md").read_text(encoding="utf-8"), "Changed public guidance\n")
        self.assertIn("New shared rules", rules.read_text(encoding="utf-8"))
        self.run_cli("remove", "--skill", "alpha", "--no-rules")
        self.assertTrue(self.skill("beta").exists())
        self.assertIn("New shared rules", rules.read_text(encoding="utf-8"))
        self.run_cli("remove")
        self.assertFalse(self.skill("beta").exists())
        self.assertEqual(rules.read_bytes(), original)

    def test_update_skips_identical_trees_rules_and_record_writes(self):
        self.run_cli("add", "--agent", "codex")
        paths = [self.skill("alpha"), self.skill("beta"), self.project / "AGENTS.md",
                 self.project / ".agents/agentskills.json"]
        before = {p: (p.stat().st_ino, p.stat().st_mtime_ns) for p in paths}
        preload = self.root / "deny-writes.cjs"
        preload.write_text("const fs=require('node:fs');for(const k of ['renameSync','copyFileSync','writeFileSync'])fs[k]=()=>{throw new Error('Unexpected write');};\n", encoding="utf-8", newline="\n")
        result = self.run_cli("update", env_extra=self.preload(preload))
        self.assertIn("Already up to date", result.stdout)
        self.assertIn("Unchanged: 3 skills", result.stdout)
        self.assertNotIn("Apply?", result.stdout)
        self.assertEqual(before, {p: (p.stat().st_ino, p.stat().st_mtime_ns) for p in paths})
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("Updated guidance\n", encoding="utf-8", newline="\n")
        result = self.run_cli("update")
        self.assertIn("Update (1): alpha", result.stdout)
        self.assertIn("Unchanged: 2 skills", result.stdout)
        self.assertEqual(before[self.skill("beta")], (self.skill("beta").stat().st_ino, self.skill("beta").stat().st_mtime_ns))
        self.assertEqual(before[self.project / "AGENTS.md"], ((self.project / "AGENTS.md").stat().st_ino, (self.project / "AGENTS.md").stat().st_mtime_ns))
        # Removing remains an explicit mutation even when source and target match.
        self.run_cli("remove")
        self.assertFalse(self.skill("beta").exists())

    def test_update_discovers_new_skills_without_restoring_excluded_or_removed_skills(self):
        for global_scope in (False, True):
            with self.subTest(global_scope=global_scope):
                for name in ("gamma", "delta"):
                    shutil.rmtree(self.source / "skills/workflow" / name, ignore_errors=True)
                scope = ["--global"] if global_scope else []
                base = self.home if global_scope else self.project
                state_file = base / (".local/share/agentskills/install.json" if global_scope else ".agents/agentskills.json")
                self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules", *scope)
                source = self.source / "skills/workflow/gamma"
                shutil.copytree(self.source / "skills/workflow/alpha", source)
                result = self.run_cli("update", "--no-rules", *scope)
                self.assertIn("Add (1): gamma", result.stdout)
                self.assertTrue((self.skill("gamma", global_scope) / "SKILL.md").is_file())
                self.assertFalse(self.skill("beta", global_scope).exists())
                self.run_cli("remove", "--skill", "gamma", "--no-rules", *scope)
                shutil.copytree(source, source.with_name("delta"))
                self.run_cli("update", "--skill", "alpha", "--no-rules", *scope)
                self.assertFalse(self.skill("delta", global_scope).exists())
                self.run_cli("update", "--no-rules", *scope)
                self.assertTrue(self.skill("delta", global_scope).is_dir())
                self.assertFalse(self.skill("gamma", global_scope).exists())
                state = json.loads(state_file.read_text(encoding="utf-8"))
                self.assertEqual(set(state["agents"]["codex"]["catalog"]), {"alpha", "beta", "gamma", "delta"})
                shutil.rmtree(source)
                shutil.rmtree(source.with_name("delta"))

    def test_generated_index_tracks_installed_sources_across_agents_and_removal(self):
        for global_scope in (False, True):
            with self.subTest(global_scope=global_scope):
                scope = ["--global"] if global_scope else []
                base = self.home if global_scope else self.project
                index = base / ".agents/skills/index"

                def indexed_paths():
                    import re
                    pages = list((index / "references/catalog").glob("*.md"))
                    text = "\n".join(page.read_text(encoding="utf-8") for page in pages)
                    paths = re.findall(r"Path: `([^`]+)`", text)
                    self.assertTrue(all((index / relative).is_file() for relative in paths))
                    return {Path(relative).parent.name for relative in paths}

                self.run_cli("add", "--agent", "codex", "--rules-only", *scope)
                self.assertTrue((index / "SKILL.md").is_file())
                self.assertEqual(indexed_paths(), set())
                self.run_cli("remove", "--agent", "codex", *scope)
                self.assertFalse(index.exists())
                self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules", *scope)
                self.assertEqual(indexed_paths(), {"alpha"})
                self.run_cli("update", "--agent", "claude", "--no-rules", *scope, success=False)
                self.assertEqual(indexed_paths(), {"alpha"})
                self.run_cli("add", "--agent", "claude", "--skill", "beta", "--no-rules", *scope)
                self.assertEqual(indexed_paths(), {"alpha", "beta"})
                self.assertEqual((base / ".claude/skills/index").resolve(), index.resolve())
                self.run_cli("remove", "--agent", "claude", "--no-rules", *scope)
                self.assertEqual(indexed_paths(), {"alpha"})
                self.assertFalse((base / ".claude/skills/index").exists())
                self.run_cli("remove", "--agent", "codex", "--no-rules", *scope)
                self.assertFalse(index.exists())

    def test_task_decisions_refresh_with_partial_install_and_removal(self):
        for name in ('spec-generator', 'plan'):
            shutil.copytree(self.source / 'skills/workflow/alpha', self.source / 'skills/workflow' / name)
        self.run_cli('add', '--agent', 'codex', '--skill', 'alpha', 'spec-generator', '--no-rules')
        route = self.skill('index') / 'references/routes/define.md'
        self.assertIn('Skill: `spec-generator`', route.read_text())
        self.assertNotIn('Skill: `plan`', route.read_text())
        self.run_cli('add', '--agent', 'codex', '--skill', 'plan', '--no-rules')
        self.assertIn('Skill: `plan`', route.read_text())
        self.run_cli('remove', '--skill', 'spec-generator', '--no-rules')
        self.assertNotIn('Skill: `spec-generator`', route.read_text())
        self.assertIn('Skill: `plan`', route.read_text())
        self.run_cli('remove', '--skill', 'plan', '--no-rules')
        self.assertFalse(route.exists())
        self.assertTrue(self.skill('alpha').is_dir())

    def test_old_owned_bundled_index_is_replaced_and_user_edits_are_preserved(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        index = self.skill("index")
        shutil.rmtree(index)
        index.mkdir()
        (index / "SKILL.md").write_text("Old bundled index lists uninstalled beta\n", encoding="utf-8")
        (index / "old-page.md").write_text("Old static catalog\n", encoding="utf-8")
        state_file = self.project / ".agents/agentskills.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        state["skills"]["index"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in index.iterdir()}
        state_file.write_text(json.dumps(state), encoding="utf-8")
        self.run_cli("update", "--no-rules")
        self.assertFalse((index / "old-page.md").exists())
        page = index / "references/catalog/workflow.md"
        self.assertIn("../alpha/SKILL.md", page.read_text(encoding="utf-8"))
        self.assertNotIn("beta", page.read_text(encoding="utf-8"))
        original = (index / "SKILL.md").read_bytes()
        (index / "SKILL.md").write_bytes(original + b"\nUser edit\n")
        before = state_file.read_bytes()
        self.run_cli("update", "--no-rules", success=False)
        self.assertEqual(state_file.read_bytes(), before)
        self.assertEqual((index / "SKILL.md").read_bytes(), original + b"\nUser edit\n")
        (index / "SKILL.md").write_bytes(original)
        shutil.rmtree(index)
        self.run_cli("update", "--no-rules")
        self.assertEqual((index / "SKILL.md").read_bytes(), original)

    def test_generated_index_replace_failure_restores_previous_catalog_and_retry_recovers(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        index = self.skill("index")
        before = {p.relative_to(index): p.read_bytes() for p in index.rglob("*") if p.is_file()}
        preload = self.root / "fail-index-replace.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;let failed=false;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(index))}&&!failed)"
            "{failed=true;throw new Error('Injected generated index failure');}return rename.apply(this,arguments);};\n",
            encoding="utf-8", newline="\n")
        self.run_cli("add", "--agent", "codex", "--skill", "beta", "--no-rules", success=False, env_extra=self.preload(preload))
        self.assertEqual({p.relative_to(index): p.read_bytes() for p in index.rglob("*") if p.is_file()}, before)
        self.assertTrue(self.skill("beta").is_dir())  # Completed items remain under the batch contract.
        self.run_cli("update", "--no-rules")
        self.assertIn("../beta/SKILL.md", (index / "references/catalog/workflow.md").read_text(encoding="utf-8"))

    def test_update_backfills_old_records_only_for_selected_skill_agents(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--global", "--no-rules")
        self.run_cli("add", "--agent", "claude", "--global", "--rules-only")
        state_file = self.home / ".local/share/agentskills/install.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        for record in state["agents"].values():
            record.pop("catalog", None)
        state_file.write_text(json.dumps(state), encoding="utf-8")
        shutil.copytree(self.source / "skills/workflow/alpha", self.source / "skills/workflow/gamma")
        result = self.run_cli("update", "--agent", "codex", "--global", "--no-rules")
        self.assertIn("gamma", result.stdout)
        state = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(set(state["agents"]["codex"]["skills"]), {"alpha", "beta", "gamma", "index"})
        self.assertEqual(state["agents"]["claude"]["skills"], {"index": True})
        self.run_cli("update", "--global")
        state = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertEqual(state["agents"]["claude"]["skills"], {"index": True})
        self.assertIn("Already up to date", self.run_cli("update", "--global").stdout)

    def test_rules_only_then_partial_add_keeps_unselected_tasks_excluded(self):
        self.run_cli("add", "--agent", "codex", "--global", "--rules-only")
        self.run_cli("add", "--agent", "codex", "--global", "--skill", "alpha", "--no-rules")
        self.run_cli("update", "--global", "--no-rules")
        self.assertTrue(self.skill("alpha", True).is_dir())
        self.assertFalse(self.skill("beta", True).exists())

    def test_explicitly_removed_new_skill_stays_excluded_across_catalog_changes(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        source = self.source / "skills/workflow/gamma"
        shutil.copytree(self.source / "skills/workflow/alpha", source)
        self.run_cli("add", "--agent", "codex", "--skill", "gamma", "--no-rules")
        self.run_cli("remove", "--skill", "gamma", "--no-rules")
        self.run_cli("update", "--no-rules")
        self.assertFalse(self.skill("gamma").exists())
        shutil.rmtree(source)
        self.run_cli("update", "--no-rules")
        shutil.copytree(self.source / "skills/workflow/alpha", source)
        self.run_cli("update", "--no-rules")
        self.assertFalse(self.skill("gamma").exists())

    def test_legacy_index_paths_use_exact_ownership_for_constructor(self):
        import re
        shutil.copytree(self.source / "skills/workflow/alpha", self.source / "skills/workflow/constructor")
        self.legacy_install(names=("alpha", "constructor"))
        self.run_cli("remove", "--agent", "codex", "--global", "--skill", "constructor", "--no-rules")
        index = self.home / ".agents/skills/index"
        text = "\n".join(page.read_text(encoding="utf-8") for page in (index / "references/catalog").glob("*.md"))
        paths = re.findall(r"Path: `([^`]+)`", text)
        self.assertTrue(all((index / relative).is_file() for relative in paths))
        constructor = next(index / relative for relative in paths if Path(relative).parent.name == "constructor")
        self.assertEqual(constructor.resolve(), self.home / ".claude/skills/constructor/SKILL.md")

    def test_unselected_index_input_removed_during_confirmation_aborts(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        state_file = self.project / ".agents/agentskills.json"
        before = state_file.read_bytes()
        result = self.confirm_after(["add", "--agent", "codex", "--project", str(self.project), "--skill", "beta", "--no-rules"],
                                    lambda: shutil.rmtree(self.skill("alpha")))
        self.assertNotEqual(result, 0)
        self.assertFalse(self.skill("beta").exists())
        self.assertEqual(state_file.read_bytes(), before)

    def test_discovery_preserves_catalog_until_changes_are_saved_and_can_retry(self):
        self.run_cli("add", "--agent", "codex", "--no-rules")
        state_file = self.project / ".agents/agentskills.json"
        before = state_file.read_bytes()
        shutil.copytree(self.source / "skills/workflow/alpha", self.source / "skills/workflow/gamma")
        foreign = self.skill("gamma")
        foreign.mkdir()
        (foreign / "SKILL.md").write_text("Unmanaged skill\n", encoding="utf-8")
        self.run_cli("update", "--no-rules", success=False)
        self.assertEqual(state_file.read_bytes(), before)
        self.assertEqual((foreign / "SKILL.md").read_text(encoding="utf-8"), "Unmanaged skill\n")
        shutil.rmtree(foreign)
        preload = self.root / "fail-discovery-record.cjs"
        for failure in (1, 2):
            preload.write_text(
                "const fs=require('node:fs');const rename=fs.renameSync;let count=0;"
                f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state_file))}&&++count==={failure})"
                "{throw new Error('Injected discovery record failure');}return rename.apply(this,arguments);};\n",
                encoding="utf-8", newline="\n")
            self.run_cli("update", "--no-rules", success=False, env_extra=self.preload(preload))
            state = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertNotIn("gamma", state["agents"]["codex"]["catalog"])
            if failure == 1:
                self.assertEqual(state_file.read_bytes(), before)
                self.assertFalse(self.skill("gamma").exists())
            else:
                self.assertTrue(self.skill("gamma").is_dir())
        self.run_cli("update", "--no-rules")
        state = json.loads(state_file.read_text(encoding="utf-8"))
        self.assertIn("gamma", state["agents"]["codex"]["catalog"])
        self.assertIn("Already up to date", self.run_cli("update", "--no-rules").stdout)

    def test_grouped_preview_preserves_names_and_separates_agents_and_rules(self):
        names = [f"example-skill-{index:02}" for index in range(30)]
        for name in names:
            skill = self.source / "skills/workflow" / name
            skill.mkdir()
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\nGuidance\n", encoding="utf-8", newline="\n")
        self.run_cli("add", "--agent", "codex")
        self.run_cli("add", "--agent", "claude", "--skill", "alpha")
        for name in names:
            (self.source / "skills/workflow" / name / "SKILL.md").write_text("Updated guidance\n", encoding="utf-8", newline="\n")
        (self.source / "rules/base.md").write_text("Updated shared rules\n", encoding="utf-8", newline="\n")
        result = self.run_cli("update")
        self.assertEqual(result.stdout.count(str(self.project / ".agents/skills")), 1)
        self.assertEqual(result.stdout.count(str(self.project / ".claude/skills")), 1)
        self.assertIn("Update (30):", result.stdout)
        for name in names:
            self.assertIn(name, result.stdout)
        self.assertIn(str(self.project / "AGENTS.md"), result.stdout)
        self.assertIn(str(self.project / "CLAUDE.md"), result.stdout)
        self.assertNotIn("update codex/", result.stdout)
        for row in result.stdout.splitlines():
            if "example-skill-" in row:
                self.assertLessEqual(len(row), 88)

    def test_preflight_conflict_preserves_all_selected_skills(self):
        self.run_cli("add", "--agent", "codex")
        modified = self.skill("beta") / "references/detail.md"
        modified.write_text("User edit\n", encoding="utf-8", newline="\n")
        before = (self.skill("alpha") / "SKILL.md").read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New alpha version\n", encoding="utf-8", newline="\n")
        self.run_cli("update", success=False)
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_bytes(), before)
        self.run_cli("remove", success=False)
        self.assertEqual(modified.read_text(encoding="utf-8"), "User edit\n")
        modified.write_text("Bundled detail\n", encoding="utf-8", newline="\n")
        (self.skill("beta") / "user-note.txt").write_text("Additional user file\n", encoding="utf-8", newline="\n")
        self.run_cli("remove", success=False)
        self.assertTrue(self.skill("alpha").exists())

    def test_unowned_skill_and_rules_blocks_are_never_adopted(self):
        target = self.skill("alpha")
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("Someone else's skill\n", encoding="utf-8", newline="\n")
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "Someone else's skill\n")
        self.assertFalse((self.project / "AGENTS.md").exists())
        original = "<!-- agentskills:rules:start -->\nExisting rules\n<!-- agentskills:rules:end -->\n"
        (self.project / "AGENTS.md").write_text(original, encoding="utf-8", newline="\n")
        self.run_cli("add", "--agent", "codex", "--rules-only", success=False)
        self.assertEqual((self.project / "AGENTS.md").read_text(encoding="utf-8"), original)

    def test_rules_edits_and_damaged_markers_block_updates_and_removal(self):
        self.run_cli("add", "--agent", "codex", "--rules-only")
        rules = self.project / "AGENTS.md"
        original = rules.read_text(encoding="utf-8")
        for modified in (
            original.replace("Respect agreed scope.", "User's rules."),
            original.replace("<!-- agentskills:rules:end -->", ""),
            original + "<!-- agentskills:rules:start -->",
        ):
            with self.subTest(modified=modified):
                rules.write_text(modified, encoding="utf-8", newline="\n")
                self.run_cli("update", success=False)
                self.run_cli("remove", success=False)
                self.assertEqual(rules.read_text(encoding="utf-8"), modified)

    def test_global_and_agent_scopes_are_isolated(self):
        self.run_cli("add", "--agent", "codex", "--global", "--skill", "alpha")
        self.run_cli("add", "--agent", "claude", "--rules-only")
        self.assertTrue(self.skill("alpha", global_scope=True).exists())
        self.assertFalse(self.skill("alpha").exists())
        self.assertTrue((self.home / ".codex/AGENTS.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").exists())
        self.run_cli("update", "--global")
        self.run_cli("remove", "--global")
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").exists())
        self.run_cli("remove")
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_symlinked_parents_and_installed_files_are_left_untouched(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.connection(outside, self.project / ".agents")
        self.run_cli("add", "--agent", "codex", success=False)
        self.assertEqual(list(outside.iterdir()), [])
        self.unlink_connection(self.project / ".agents")
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        target = self.skill("alpha") / "references/detail.md"
        target.unlink()
        external = outside / "detail.md"
        external.write_text("Outside the installation\n", encoding="utf-8", newline="\n")
        if os.name == "nt":
            shutil.rmtree(target.parent)
            self.connection(outside, target.parent)
        else:
            target.symlink_to(external)
        self.run_cli("update", success=False)
        self.run_cli("remove", success=False)
        self.assertEqual(external.read_text(encoding="utf-8"), "Outside the installation\n")

    def test_invalid_selection_and_busy_lock_do_not_install(self):
        self.run_cli("add", "--agent", "codex", "--skill", "unknown", success=False)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / ".agents/skills").exists())
        self.run_cli("add", "--agent", "codex", "--skill", "../escape", success=False)
        lock = self.project / ".agents/agentskills.json.lock"
        lock.write_text("Another operation\n", encoding="utf-8", newline="\n")
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
        self.assertEqual(lock.read_text(encoding="utf-8"), "Another operation\n")
        lock.unlink()
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        state = json.loads((self.project / ".agents/agentskills.json").read_text(encoding="utf-8"))
        self.assertEqual(set(state["agents"]["codex"]["skills"]), {"alpha", "index"})

    def test_changes_during_confirmation_abort_before_mutating_any_item(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        installed = self.skill("alpha") / "SKILL.md"
        rules = self.project / "AGENTS.md"
        state = self.project / ".agents/agentskills.json"
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New version\n", encoding="utf-8", newline="\n")
        for edited in (installed, rules, state):
            with self.subTest(edited=edited.name):
                originals = {file: file.read_bytes() for file in (installed, rules, state)}
                try:
                    result = self.confirm_after(["update"], lambda: edited.write_bytes(originals[edited] + b"\nUser edit while pending\n"))
                    self.assertNotEqual(result, 0)
                    for file, original in originals.items():
                        self.assertEqual(file.read_bytes(), original + (b"\nUser edit while pending\n" if file == edited else b""))
                finally:
                    for file, original in originals.items():
                        file.write_bytes(original)

    def test_parent_redirect_during_confirmation_does_not_touch_outside_files(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        outside = self.root / "outside"
        outside.mkdir()
        lock = outside / "agentskills.json.lock"
        lock.write_text("Unrelated lock\n", encoding="utf-8", newline="\n")
        original = (self.skill("alpha") / "SKILL.md").read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("Updated guidance\n", encoding="utf-8", newline="\n")

        def redirect():
            (self.project / ".agents").rename(self.project / ".agents-original")
            self.connection(outside, self.project / ".agents")

        self.assertNotEqual(self.confirm_after(["update"], redirect), 0)
        self.assertEqual({file.name for file in outside.iterdir()}, {"agentskills.json.lock"})
        self.assertEqual(lock.read_text(encoding="utf-8"), "Unrelated lock\n")
        self.assertEqual((self.project / ".agents-original/skills/alpha/SKILL.md").read_bytes(), original)

    def test_record_write_failure_rolls_back_install_update_and_removal(self):
        state = self.project / ".agents/agentskills.json"
        preload = self.root / "fail-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))})"
            "{throw new Error('Injected record write failure');}"
            "return rename.apply(this,arguments);};\n"
        , encoding="utf-8", newline="\n")
        injected = self.preload(preload)
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules", success=False, env_extra=injected)
        self.assertFalse(self.skill("alpha").exists())
        self.assertFalse(state.exists())
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        installed = self.skill("alpha") / "SKILL.md"
        original = installed.read_bytes()
        original_state = state.read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New guidance\n", encoding="utf-8", newline="\n")
        self.run_cli("update", "--no-rules", success=False, env_extra=injected)
        self.assertEqual(installed.read_bytes(), original)
        self.assertEqual(state.read_bytes(), original_state)
        self.run_cli("update", "--no-rules")
        self.assertEqual(installed.read_text(encoding="utf-8"), "New guidance\n")
        before_remove = state.read_bytes()
        self.run_cli("remove", "--no-rules", success=False, env_extra=injected)
        self.assertEqual(installed.read_text(encoding="utf-8"), "New guidance\n")
        self.assertEqual(state.read_bytes(), before_remove)
        self.run_cli("remove", "--no-rules")
        self.assertFalse(self.skill("alpha").exists())

    def test_record_failure_restores_shared_rules_and_retry_succeeds(self):
        state = self.project / ".agents/agentskills.json"
        preload = self.root / "fail-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))})"
            "{throw new Error('Injected record write failure');}"
            "return rename.apply(this,arguments);};\n"
        , encoding="utf-8", newline="\n")
        injected = self.preload(preload)
        rules = self.project / "AGENTS.md"
        original = b"# Keep project instructions\n"
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--rules-only", success=False, env_extra=injected)
        self.assertEqual(rules.read_bytes(), original)
        self.run_cli("add", "--agent", "codex", "--rules-only")
        installed = rules.read_bytes()
        before_remove = state.read_bytes()
        self.run_cli("remove", success=False, env_extra=injected)
        self.assertEqual(rules.read_bytes(), installed)
        self.assertEqual(state.read_bytes(), before_remove)
        self.run_cli("remove")
        self.assertEqual(rules.read_bytes(), original)

    def test_non_utf8_rules_are_rejected_before_install_and_bom_is_preserved(self):
        rules = self.project / "AGENTS.md"
        for original in ("# Existing instructions\n".encode("utf-16"), b"# Existing\n\xff\xfe"):
            with self.subTest(original=original):
                rules.write_bytes(original)
                self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
                self.assertEqual(rules.read_bytes(), original)
                self.assertFalse(self.skill("alpha").exists())
        original = b"\xef\xbb\xbf" + "# Project instructions\r\nNon-ASCII: café\r\n".encode()
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--rules-only")
        self.assertTrue(rules.read_bytes().startswith(b"\xef\xbb\xbf<!-- agentskills:rules:start -->"))
        self.assertIn("Already up to date", self.run_cli("update").stdout)
        (self.source / "rules/base.md").write_text("Updated shared rules\n", encoding="utf-8", newline="\n")
        self.run_cli("update")
        self.run_cli("remove")
        self.assertEqual(rules.read_bytes(), original)

    def test_prototype_name_is_an_exact_selection_not_an_inherited_entry(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        rules = self.project / "AGENTS.md"
        original = rules.read_bytes()
        self.run_cli("remove", "--skill", "constructor", success=False)
        self.run_cli("add", "--agent", "codex", "--skill", "constructor", success=False)
        self.assertEqual(rules.read_bytes(), original)
        extra = self.skill("alpha") / "__proto__"
        extra.write_text("Additional user file\n", encoding="utf-8", newline="\n")
        self.run_cli("update", "--no-rules", success=False)
        self.run_cli("remove", "--no-rules", success=False)
        self.assertEqual(extra.read_text(encoding="utf-8"), "Additional user file\n")
        extra.unlink()
        source = self.source / "skills/workflow/constructor"
        shutil.copytree(self.source / "skills/workflow/alpha", source)
        unowned = self.skill("constructor")
        unowned.mkdir()
        self.run_cli("add", "--agent", "codex", "--skill", "constructor", success=False)
        unowned.rmdir()
        self.run_cli("add", "--agent", "codex", "--skill", "constructor")
        self.assertTrue((unowned / "SKILL.md").exists())
        self.run_cli("remove", "--skill", "constructor", "--no-rules")
        self.assertFalse(unowned.exists())
        self.assertTrue(self.skill("alpha").exists())
        self.assertEqual(rules.read_bytes(), original)

    def test_help_aliases_are_side_effect_free_and_support_each_command(self):
        root_help = self.run_cli("--help")
        self.assertTrue(root_help.stdout.strip())
        self.assertEqual(root_help.stderr, "")
        for args in (("-h",), ("help",), ("help", "--help")):
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(*args).stdout, root_help.stdout)
        for command in ("add", "update", "remove", "list"):
            with self.subTest(command=command):
                by_flag = self.run_cli(command, "--help", "--project", str(self.root / "missing"), "--agent", "invalid")
                by_command = self.run_cli("help", command)
                self.assertTrue(by_flag.stdout.strip())
                self.assertEqual(by_flag.stdout, by_command.stdout)
                self.assertEqual(by_flag.stderr, "")
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_add_and_update_apply_on_empty_confirmation(self):
        args = ["add", "--agent", "codex", "--project", str(self.project), "--skill", "alpha", "--no-rules"]
        self.assertEqual(self.confirm_after(args, lambda: None, response=b"\n"), 0)
        self.assertTrue(self.skill("alpha").is_dir())
        source = self.source / "skills/workflow/alpha/SKILL.md"
        source.write_bytes(source.read_bytes() + b"Updated guidance.\n")
        self.assertEqual(self.confirm_after(["update"], lambda: None, response=b"\n"), 0)
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_bytes(), source.read_bytes())

    def test_add_and_update_cancel_on_negative_or_invalid_confirmation(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        installed = (self.skill("alpha") / "SKILL.md").read_bytes()
        state = self.project / ".agents/agentskills.json"
        original = state.read_bytes()
        source = self.source / "skills/workflow/alpha/SKILL.md"
        source.write_bytes(source.read_bytes() + b"Updated guidance.\n")
        add = ["add", "--agent", "codex", "--project", str(self.project), "--skill", "beta", "--no-rules"]
        for args in (add, ["update"]):
            for response in (b"n\n", b"invalid\n"):
                with self.subTest(command=args[0], response=response):
                    self.assertEqual(self.confirm_after(args, lambda: None, response=response), 0)
                    self.assertEqual(state.read_bytes(), original)
                    self.assertEqual((self.skill("alpha") / "SKILL.md").read_bytes(), installed)
                    self.assertFalse(self.skill("beta").exists())
                    self.assertFalse(state.with_suffix(".json.lock").exists())

    def test_cancelling_confirmation_does_not_leave_a_lock_or_change_files(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        state = self.project / ".agents/agentskills.json"
        original = state.read_bytes()
        for response, expected in ((b"\n", 0), (b"n\n", 0), (b"invalid\n", 0), (b"\x03", 130)):
            with self.subTest(response=response):
                result = self.confirm_after(["remove"], lambda: None, response=response)
                # cmd.exe can report the native CTRL_C_EXIT status for the
                # ConPTY process group even when Node handles cancellation.
                accepted = (130, 0xC000013A) if os.name == "nt" and response == b"\x03" else (expected,)
                self.assertIn(result, accepted)
                self.assertEqual(state.read_bytes(), original)
                self.assertTrue(self.skill("alpha").exists())
                self.assertFalse((self.project / ".agents/agentskills.json.lock").exists())
        self.run_cli("update")

    def test_invalid_interactive_scope_cannot_fall_back_to_project_install(self):
        result = self.confirm_after(["add", "--agent", "codex"], lambda: None, response=b"globla\n", wait_for=b"Scope [")
        self.assertNotEqual(result, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_failure_after_one_completed_item_preserves_that_progress_and_can_retry(self):
        self.run_cli("add", "--agent", "codex", "--no-rules")
        state = self.project / ".agents/agentskills.json"
        for name in ("alpha", "beta"):
            (self.source / "skills/workflow" / name / "SKILL.md").write_text(f"Updated {name}\n", encoding="utf-8", newline="\n")
        preload = self.root / "fail-second-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;let count=0;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))}&&++count===2)"
            "{throw new Error('Injected second record write failure');}"
            "return rename.apply(this,arguments);};\n"
        , encoding="utf-8", newline="\n")
        result = self.run_cli("update", "--no-rules", success=False, env_extra=self.preload(preload))
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_text(encoding="utf-8"), "Updated alpha\n")
        self.assertNotEqual((self.skill("beta") / "SKILL.md").read_text(encoding="utf-8"), "Updated beta\n")
        self.assertIn(str(state), result.stderr)
        self.run_cli("update", "--no-rules")
        self.assertEqual((self.skill("beta") / "SKILL.md").read_text(encoding="utf-8"), "Updated beta\n")
