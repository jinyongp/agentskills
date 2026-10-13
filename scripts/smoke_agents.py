"""Verify real agents discover npm-packed skills without authentication or model requests."""

import argparse
import base64
import hashlib
import json
import os
import platform
from pathlib import Path
import queue
import shutil
import subprocess
import tarfile
import tempfile
import threading
import time
import urllib.request

from npm_cli import npm_command
from smoke_package import ROOT, run


def windows_agents(directory):
    """Fetch immutable official builds, checking pinned publisher integrity values."""
    if os.name != "nt" or platform.machine().lower() not in ("amd64", "x86_64"):
        raise RuntimeError("Automatic native-agent download requires Windows x64")
    artifacts = {
        "claude": (
            "https://downloads.claude.ai/claude-code-releases/2.1.296/win32-x64/claude.exe",
            "sha256", "76de74f7694a5bdc03378a5f837c9e132827bf004c98c276bc4e9094ff06769a"),
        "codex": (
            "https://registry.npmjs.org/@openai/codex/-/codex-0.162.1-win32-x64.tgz",
            "sha512", base64.b64decode("dfl4MhHuEi0ARKyNmrTxk+RQmsWNCQAoVLUtrYq+yrW1C8P2sg5ziwgHUUACHjYLKuACV7ARH5Nq5pnCz3GlaQ==").hex()),
    }
    binaries = {}
    for name, (url, algorithm, expected) in artifacts.items():
        archive = directory / (name + (".exe" if name == "claude" else ".tgz"))
        digest, size = hashlib.new(algorithm), 0
        with urllib.request.urlopen(url, timeout=30) as response, archive.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > 512 * 1024 * 1024:
                    raise RuntimeError("Native-agent download exceeded 512 MiB")
                digest.update(chunk)
                output.write(chunk)
        if digest.hexdigest() != expected:
            raise RuntimeError(f"{name} publisher integrity mismatch")
        if name == "codex":
            destination = directory / name
            destination.mkdir()
            with tarfile.open(archive) as package:
                package.extractall(destination, filter="data")
            matches = list(destination.rglob("codex.exe"))
            if len(matches) != 1:
                raise RuntimeError("Expected exactly one native Codex executable")
            binaries[name] = matches[0]
        else:
            binaries[name] = archive
    return binaries


class JsonProcess:
    def __init__(self, argv, project, env):
        self.process = subprocess.Popen(argv, cwd=project, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.messages = queue.Queue(maxsize=64)
        self.stderr = b""
        self.stderr_bytes = 0
        self.threads = [threading.Thread(target=target, daemon=True)
                        for target in (self.read_stdout, self.read_stderr)]
        for thread in self.threads:
            thread.start()

    def read_stdout(self):
        while line := self.process.stdout.readline(1024 * 1024 + 1):
            if len(line) > 1024 * 1024:
                message = {"error": "Agent JSON line exceeded 1 MiB"}
            else:
                try:
                    message = json.loads(line)
                except (ValueError, UnicodeDecodeError):
                    message = {"error": "Agent emitted invalid JSON"}
            try:
                self.messages.put_nowait(message)
            except queue.Full:
                return
        try:
            self.messages.put_nowait({"eof": True})
        except queue.Full:
            pass

    def read_stderr(self):
        while chunk := self.process.stderr.read(4096):
            self.stderr_bytes += len(chunk)
            self.stderr = (self.stderr + chunk)[-4096:]

    def send(self, payload):
        self.process.stdin.write((json.dumps(payload) + "\n").encode())
        self.process.stdin.flush()

    def request(self, payload, matches):
        self.send(payload)
        deadline = time.monotonic() + 45
        try:
            while True:
                response = self.messages.get(timeout=max(0.001, deadline - time.monotonic()))
                if response.get("eof") or response.get("error"):
                    raise RuntimeError(str(response)[:4096])
                if matches(response):
                    return response
                if time.monotonic() >= deadline:
                    raise queue.Empty
        except (queue.Empty, RuntimeError) as error:
            omitted = max(0, self.stderr_bytes - len(self.stderr))
            raise RuntimeError(f"Agent discovery failed: {error}; stderr ({omitted} bytes omitted): {self.stderr!r}") from error

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        for thread in self.threads:
            thread.join(timeout=1)
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            stream.close()


def discover(agent, binary, project, env):
    if agent == "claude":
        argv = [str(binary), "--print", "--input-format", "stream-json", "--output-format",
                "stream-json", "--verbose", "--setting-sources", "user,project",
                "--no-session-persistence", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    else:
        argv = [str(binary), "app-server", "--stdio"]
    client = JsonProcess(argv, project, env)
    try:
        if agent == "claude":
            response = client.request({"type": "control_request", "request_id": "discovery",
                                       "request": {"subtype": "initialize"}},
                                      lambda r: r.get("type") == "control_response" and
                                      r.get("response", {}).get("request_id") == "discovery")["response"]
            if response.get("subtype") != "success":
                raise RuntimeError(str(response)[:4096])
            return [{"name": c["name"], "description": c["description"]}
                    for c in response["response"]["commands"] if c["name"] == "survey"]
        response = client.request({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "agentskills_acceptance", "version": "0.1.0"},
            "capabilities": {"experimentalApi": True, "explicitGatewayOauth": True}}},
            lambda r: r.get("id") == 1)
        if "error" in response:
            raise RuntimeError(str(response)[:4096])
        client.send({"method": "initialized"})
        response = client.request({"id": 2, "method": "skills/list", "params": {
            "cwds": [str(project)], "forceReload": True}}, lambda r: r.get("id") == 2)
        if "error" in response:
            raise RuntimeError(str(response)[:4096])
        return [{"name": s["name"], "path": s["path"], "scope": s["scope"]}
                for item in response["result"]["data"] for s in item["skills"]
                if s["name"] == "survey" and s["enabled"]]
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude", type=Path)
    parser.add_argument("--codex", type=Path)
    parser.add_argument("--download-windows-agents", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not (args.claude or args.codex or args.download_windows_agents):
        parser.error("Supply native agent paths or --download-windows-agents")
    results = []
    with tempfile.TemporaryDirectory(prefix="agentskills-agents-") as directory:
        temp = Path(directory).resolve()
        agents = windows_agents(temp) if args.download_windows_agents else {}
        agents.update({name: path.resolve() for name, path in (("claude", args.claude), ("codex", args.codex)) if path})
        home, project, prefix = (temp / name for name in ("home", "project 한글's space", "tools"))
        for path in (home, project, prefix):
            path.mkdir()
        # Local discovery must not reuse account credentials, hooks, plugins or providers.
        env = {k: v for k, v in os.environ.items() if not any(token in k.upper() for token in
               ("API_KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL", "AWS_", "GOOGLE_", "AZURE_", "ANTHROPIC", "CLAUDE", "CODEX", "OTEL_"))}
        env.update(HOME=str(home), USERPROFILE=str(home), CODEX_HOME=str(home / ".codex"),
                   CLAUDE_CONFIG_DIR=str(home / ".claude"), CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
                   DISABLE_AUTOUPDATER="1", CLAUDE_CODE_USE_NATIVE_FILE_SEARCH="1",
                   ANTHROPIC_BASE_URL="http://127.0.0.1:9", OPENAI_BASE_URL="http://127.0.0.1:9",
                   npm_config_cache=str(temp / "npm-cache"))
        (home / ".codex").mkdir()
        node = shutil.which("node")
        if Path(run([node, "-p", "require('node:os').homedir()"], project, env).strip()).resolve() != home:
            raise RuntimeError("Home isolation failed; refusing global installation")
        packed = json.loads(run([*npm_command(), "pack", "--json", "--ignore-scripts",
                                 "--pack-destination", str(temp)], ROOT, env))[0]
        run([*npm_command(), "install", "--prefix", str(prefix), "--ignore-scripts", "--no-audit",
             "--no-fund", str(temp / packed["filename"])], project, env)
        cli = prefix / "node_modules/@jinyongp/agentskills/agentskills.js"
        for agent, binary in agents.items():
            version = run([str(binary), "--version"], project, env).strip()
            for global_scope in (False, True):
                scope = ["--global"] if global_scope else ["--project", str(project)]
                if discover(agent, binary, project, env):
                    raise RuntimeError("Unexpected survey skill before isolated installation")
                run([node, str(cli), "add", "--agent", agent, "--skill", "survey", "--no-rules", "--yes", *scope], project, env)
                found = discover(agent, binary, project, env)
                if len(found) != 1:
                    raise RuntimeError(f"{agent} must discover exactly one installed survey skill: {found}")
                shared = (home if global_scope else project) / ".agents/skills/survey/SKILL.md"
                if agent == "codex" and Path(found[0]["path"]).resolve() != shared.resolve():
                    raise RuntimeError("Codex discovered a different skill source")
                run([node, str(cli), "remove", "--no-rules", "--yes", *scope], project, env)
                if discover(agent, binary, project, env):
                    raise RuntimeError(f"{agent} still discovers the removed skill")
                results.append({"agent": agent, "version": version, "scope": "global" if global_scope else "project",
                                "before": "absent", "installed": "discovered", "removed": "absent"})
    report = {"results": results, "model_requests": False, "credentials": "isolated", "providers": "closed localhost port"}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
