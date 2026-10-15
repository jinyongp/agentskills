"""Release a specified version and wait for npm and GitHub publication."""

import argparse
import base64
from copy import deepcopy
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parent
SEMVER = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?")
POLL_SECONDS = 10
RUN_TIMEOUT = 3600
DOWNLOAD_TIMEOUT = 300


class ReleaseError(Exception):
    pass


def version_argument(value: str) -> str:
    match = SEMVER.fullmatch(value)
    if not match or any(x.isdigit() and len(x) > 1 and x.startswith("0")
                        for x in (match[4] or "").split(".")):
        raise argparse.ArgumentTypeError("Use a version such as 0.2.0 or 0.3.0-rc.1 (no v prefix or build metadata).")
    return value


def version_key(value: str) -> tuple:
    try:
        version_argument(value)
    except argparse.ArgumentTypeError as error:
        raise ReleaseError(f"Unsupported package version: {value}") from error
    core, _, pre = value.partition("-")
    identifiers = tuple((0, int(x)) if x.isdigit() else (1, x) for x in pre.split("."))
    return (*map(int, core.split(".")), not bool(pre), identifiers)


def github_repo(url: str) -> str:
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?", url)
    if not match:
        raise ReleaseError("The package repository and origin must identify a GitHub repository.")
    return match[1]


def release_manifest(original: dict, version: str) -> dict:
    result = deepcopy(original)
    result["version"] = version
    config = result.setdefault("publishConfig", {})
    if "-" in version:
        config["tag"] = "next"
    else:
        config.pop("tag", None)
    return result


class Commands:
    def __init__(self, root: Path, log: Path):
        self.root, self.log = root, log

    def run(self, *argv: str, cwd: Path | None = None, timeout: int = 120,
            check: bool = True) -> subprocess.CompletedProcess:
        with self.log.open("ab") as log:
            log.write(("\n$ " + shlex.join(argv) + "\n").encode())
            log.flush()
            # Output goes straight to disk; only structured responses are read below.
            start = log.tell()
            process = subprocess.Popen(argv, cwd=cwd or self.root, stdout=log,
                                       stderr=log, start_new_session=True,
                                       env={**os.environ, "CI": "1", "GH_PROMPT_DISABLED": "1",
                                            "GH_HOST": "github.com", "GIT_TERMINAL_PROMPT": "0",
                                            "NO_COLOR": "1"})
            try:
                process.wait(timeout=timeout)
            except (subprocess.TimeoutExpired, KeyboardInterrupt):
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise ReleaseError(f"Interrupted or timed out: {shlex.join(argv)}. Rerun the same release command to inspect its outcome.")
            if check and process.returncode:
                raise ReleaseError(f"Command failed ({process.returncode}): {shlex.join(argv)}")
            end = log.tell()
        with self.log.open("rb") as log:
            log.seek(start)
            output = log.read(min(end - start, 1_000_001)).decode("utf-8", errors="replace")
        if end - start > 1_000_000:
            output = None  # Large check/install logs are not structured command input.
        return subprocess.CompletedProcess(argv, process.returncode, output)

    def text(self, *argv: str, **options) -> str:
        result = self.run(*argv, **options)
        if result.stdout is None:
            raise ReleaseError(f"Response exceeds 1 MB: {shlex.join(argv)}; inspect the complete log.")
        return result.stdout.strip()

    def json(self, *argv: str, **options):
        try:
            return json.loads(self.text(*argv, **options))
        except json.JSONDecodeError as error:
            raise ReleaseError(f"Expected a bounded JSON response from {shlex.join(argv)}; inspect the log.") from error


def working_tree(commands: Commands, expected: dict | None = None) -> None:
    result = commands.run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if result.stdout is None:
        raise ReleaseError("Worktree inspection exceeds 1 MB; inspect the complete log.")
    status = result.stdout.rstrip("\0\n")
    if not status:
        return
    # An interrupted preparation can leave exactly the requested manifest change.
    entries = status.split("\0")
    allowed = {" M package.json", "M  package.json", "MM package.json", ""}
    if expected is None or any(x not in allowed for x in entries):
        raise ReleaseError("Commit or set aside other work before releasing; the worktree is not clean.")
    current = json.loads((commands.root / "package.json").read_text())
    staged = json.loads(commands.text("git", "show", ":package.json"))
    original = json.loads(commands.text("git", "show", "HEAD:package.json"))
    if current != expected or staged not in (original, expected):
        raise ReleaseError("package.json contains changes beyond this release version and dist-tag.")


def remote_tag(commands: Commands, tag: str) -> str | None:
    rows = commands.text("git", "ls-remote", "origin", f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}")
    refs = dict(line.split()[::-1] for line in rows.splitlines())
    return refs.get(f"refs/tags/{tag}^{{}}", refs.get(f"refs/tags/{tag}"))


def published_version(commands: Commands, package: str, version: str) -> dict | None:
    result = commands.run("npm", "view", f"{package}@{version}", "version", "dist.integrity", "gitHead", "--json", check=False)
    if result.returncode:
        # Only a registry E404 establishes absence; authentication/network errors do not.
        if result.stdout and re.search(r'"code"\s*:\s*"E404"', result.stdout):
            return None
        raise ReleaseError("npm could not establish whether this version exists; inspect the log.")
    try:
        value = json.loads(result.stdout or "")
    except json.JSONDecodeError as error:
        raise ReleaseError("npm returned an invalid version response.") from error
    if not isinstance(value, dict) or value.get("version") != version:
        raise ReleaseError("npm returned an unexpected package version.")
    return value


def check_published_tarball(commands: Commands, manifest: dict, live: dict) -> None:
    deadline = time.monotonic() + DOWNLOAD_TIMEOUT
    with tempfile.TemporaryDirectory(prefix="agentskills-registry-pack-") as directory:
        temp = Path(directory)
        while True:
            result = commands.run(
                "npm", "pack", f"{manifest['name']}@{manifest['version']}", "--json",
                "--ignore-scripts", "--cache", str(temp / "cache"),
                "--pack-destination", directory, "--fetch-retries=0",
                "--fetch-timeout=30000", cwd=temp, timeout=45, check=False)
            if result.returncode == 0:
                try:
                    packed = json.loads(result.stdout or "")
                    info, = packed
                    filename = info["filename"]
                    if Path(filename).name != filename:
                        raise ValueError("Unexpected archive path")
                    archive = temp / filename
                    with archive.open("rb") as stream:
                        digest = "sha512-" + base64.b64encode(
                            hashlib.file_digest(stream, "sha512").digest()
                        ).decode("ascii")
                except (ValueError, TypeError, KeyError, OSError) as error:
                    raise ReleaseError("Invalid downloaded npm archive or response.") from error
                if ((info.get("name"), info.get("version")) !=
                        (manifest["name"], manifest["version"]) or
                        digest != live.get("dist.integrity")):
                    raise ReleaseError("Downloaded npm archive identity or integrity differs from publication.")
                print("Registry archive downloaded with matching integrity.", flush=True)
                return
            transient = re.search(r"\b(E404|ETIMEDOUT|ECONNRESET|EAI_AGAIN|ENOTFOUND)\b",
                                  result.stdout or "")
            if not transient or time.monotonic() >= deadline:
                raise ReleaseError("Published npm archive could not be downloaded; inspect the log. Metadata alone is not a completed release.")
            print("Registry archive unavailable; waiting for download readiness...", flush=True)
            time.sleep(min(POLL_SECONDS, max(0, deadline - time.monotonic())))


def check_tarball(commands: Commands, manifest: dict) -> None:
    with tempfile.TemporaryDirectory(prefix="agentskills-release-pack-") as directory:
        temp = Path(directory)
        packed = commands.json("npm", "pack", "--json", "--pack-destination", directory, timeout=300)
        if len(packed) != 1:
            raise ReleaseError("Expected one npm package.")
        info = packed[0]
        if (info["name"], info["version"]) != (manifest["name"], manifest["version"]):
            raise ReleaseError("Packed package identity does not match package.json.")
        allowed = ["package.json", "README*", "LICENSE*", *(p for p in manifest["files"] if not p.startswith("!"))]
        excluded = [p[1:] for p in manifest["files"] if p.startswith("!")]

        def matches(path, patterns):
            return any(path == pattern.rstrip("/") or path.startswith(pattern.rstrip("/") + "/")
                       or fnmatch.fnmatchcase(path, pattern) for pattern in patterns)

        def bundled(path):
            return matches(path, allowed) and not matches(path, excluded)

        for entry in info["files"]:
            path = entry["path"]
            if not bundled(path):
                raise ReleaseError(f"Unexpected packaged file: {path}")
        bins = manifest.get("bin", {})
        if not isinstance(bins, dict) or len(bins) != 1:
            raise ReleaseError("Expected one bundled installer entrypoint in package.json.")
        binary = next(iter(bins))
        tarball = temp / info["filename"]
        project = temp / "project"
        project.mkdir()
        for arguments in (("--help",), ("add", "--agent", "codex", "--yes")):
            commands.run("npx", "--yes", "--package", str(tarball), binary,
                         *arguments, cwd=project, timeout=300)
        # The installed bundle must retain scripts, references and license notices.
        expected_skills = set()
        for skill in commands.root.glob("skills/*/*/SKILL.md"):
            if not bundled(skill.relative_to(commands.root).as_posix()):
                continue
            source = skill.parent
            expected_skills.add(source.name)
            installed = project / ".agents/skills" / source.name
            for path in source.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    target = installed / path.relative_to(source)
                    if not target.is_file() or target.read_bytes() != path.read_bytes():
                        raise ReleaseError(f"Installed bundle differs: {path.relative_to(commands.root)}")
        from skills_ref import read_properties, validate
        index = project / ".agents/skills/index"
        problems = validate(index)
        if problems:
            raise ReleaseError(f"Generated index is invalid: {problems}")
        index_base = (read_properties(index).metadata or {}).get("catalog-base")
        if not isinstance(index_base, str) or Path(index_base).resolve() != index.resolve():
            raise ReleaseError("Generated index has an incorrect catalog base.")
        paths = [relative for page in (index / "references/catalog").glob("*.md")
                 for relative in re.findall(r"Path: `([^`]+)`", page.read_text(encoding="utf-8"))]
        expected_paths = {(project / ".agents/skills" / name / "SKILL.md").resolve() for name in expected_skills}
        if len(paths) != len(expected_paths) or {(Path(index_base) / path).resolve() for path in paths} != expected_paths:
            raise ReleaseError("Generated index does not match the installed task skills.")
        print("Package execution, bundled skill files and generated index passed.", flush=True)


def workflow_file(root: Path) -> str:
    paths = [p for p in (root / ".github/workflows").iterdir()
             if p.suffix in (".yml", ".yaml") and
             re.search(r"uses:\s*releaseway/npm-actions@", p.read_text())]
    if len(paths) != 1:
        raise ReleaseError("Expected one releaseway npm publication workflow.")
    return paths[0].name


def wait_for_run(commands: Commands, repo: str, workflow: str, tag: str, commit: str,
                 retry_failed: bool = False) -> dict:
    deadline = time.monotonic() + 120
    while True:
        runs = commands.json("gh", "run", "list", "--repo", repo, "--workflow", workflow,
                             "--branch", tag, "--commit", commit, "--event", "push",
                             "--limit", "1", "--json", "databaseId,status,conclusion,url,headSha,headBranch,attempt")
        if runs:
            run = runs[0]
            if run["headSha"] != commit or run["headBranch"] != tag:
                raise ReleaseError("Workflow identity does not match the release tag and commit.")
            break
        if time.monotonic() >= deadline:
            raise ReleaseError("The tag is pushed but its release run has not appeared. Rerun this command later.")
        time.sleep(POLL_SECONDS)
    print(f"Actions: {run['url']}", flush=True)
    minimum_attempt = run["attempt"]
    if retry_failed and run["status"] == "completed" and run["conclusion"] != "success":
        if run["conclusion"] not in ("failure", "timed_out", "cancelled"):
            raise ReleaseError(f"Resolve the {run['conclusion']} run before retrying: {run['url']}")
        commands.run("gh", "run", "view", str(run["databaseId"]), "--repo", repo, "--log-failed", check=False)
        print("Resuming the previous failed release (one retry this invocation).", flush=True)
        options = ("--failed",) if run["conclusion"] != "cancelled" else ()
        commands.run("gh", "run", "rerun", str(run["databaseId"]), "--repo", repo, *options)
        minimum_attempt += 1
    deadline = time.monotonic() + RUN_TIMEOUT
    last_status = None
    while True:
        current = commands.json("gh", "run", "view", str(run["databaseId"]), "--repo", repo,
                                "--json", "status,conclusion,attempt,headSha,headBranch,url")
        if current["headSha"] != commit or current["headBranch"] != tag:
            raise ReleaseError("Workflow identity changed while waiting.")
        status = (current["attempt"], current["status"])
        if status != last_status:
            print(f"Actions: {current['status']} (attempt {current['attempt']}).", flush=True)
            last_status = status
        if current["attempt"] >= minimum_attempt and current["status"] == "completed":
            if current["conclusion"] != "success":
                commands.run("gh", "run", "view", str(run["databaseId"]), "--repo", repo, "--log-failed", check=False)
                raise ReleaseError(f"Release run ended with {current['conclusion']}: {current['url']}")
            return current
        if time.monotonic() >= deadline:
            raise ReleaseError(f"Timed out waiting; the run may still be active: {current['url']}. Rerun this command to resume.")
        time.sleep(POLL_SECONDS)


def release(commands: Commands, version: str) -> None:
    print(f"Preparing v{version}...", flush=True)
    for tool in ("git", "gh", "uv", "npm", "npx", "node"):
        if not shutil.which(tool):
            raise ReleaseError(f"Required tool unavailable: {tool}")
    manifest_path = commands.root / "package.json"
    manifest = json.loads(manifest_path.read_text())
    original = json.loads(commands.text("git", "show", "HEAD:package.json"))
    expected = release_manifest(original, version)
    working_tree(commands, expected)
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if (commands.root / commands.text("git", "rev-parse", "--git-path", marker)).exists():
            raise ReleaseError("Finish the active Git operation before releasing.")
    repository = manifest["repository"]
    repo = github_repo(repository if isinstance(repository, str) else repository["url"])
    push_urls = commands.text("git", "remote", "get-url", "--push", "--all", "origin").splitlines()
    if (github_repo(commands.text("git", "remote", "get-url", "origin")) != repo
            or len(push_urls) != 1 or github_repo(push_urls[0]) != repo):
        raise ReleaseError("origin must have one push destination matching package.json's repository.")
    metadata = commands.json("gh", "api", f"repos/{repo}")
    branch = metadata["default_branch"]
    if not metadata.get("permissions", {}).get("push"):
        raise ReleaseError("GitHub authentication lacks push access to this repository.")
    if commands.text("git", "branch", "--show-current") != branch:
        raise ReleaseError(f"Run from the repository's default branch: {branch}")
    workflow = workflow_file(commands.root)
    commands.run("git", "fetch", "--no-tags", "origin", branch)
    head = commands.text("git", "rev-parse", "HEAD")
    remote_head = commands.text("git", "rev-parse", "FETCH_HEAD")
    if commands.run("git", "merge-base", "--is-ancestor", remote_head, head, check=False).returncode:
        raise ReleaseError("The local branch is behind or diverged; synchronize it before releasing.")
    tag = f"v{version}"
    local_result = commands.run("git", "rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}", check=False)
    local = local_result.stdout.strip() if local_result.returncode == 0 else None
    remote = remote_tag(commands, tag)
    existing = published_version(commands, manifest["name"], version)
    if local or remote:
        if any(target != head for target in (local, remote) if target) or manifest != expected:
            raise ReleaseError("The existing release tag or manifest does not match HEAD. Use a new version for source changes.")
        working_tree(commands)
    elif existing:
        raise ReleaseError("This npm version is already published without a matching release tag. Choose a new version.")
    else:
        if version_key(version) < version_key(original["version"]):
            raise ReleaseError("The release version must not precede the current package version.")
        working_tree(commands, expected)
        if commands.text("git", "rev-parse", "HEAD") != head or commands.text("git", "branch", "--show-current") != branch:
            raise ReleaseError("The checkout changed during preflight; inspect it before retrying.")
        print("Running repository checks and testing the package...", flush=True)
        manifest_path.write_text(json.dumps(expected, indent=2) + "\n")
        commands.run("uv", "run", "--locked", "check.py", timeout=900)
        check_tarball(commands, expected)
        if commands.text("git", "rev-parse", "HEAD") != head or commands.text("git", "branch", "--show-current") != branch:
            raise ReleaseError("The checkout changed during preparation; inspect it before retrying.")
        working_tree(commands, expected)
        if json.loads(manifest_path.read_text()) != expected:
            raise ReleaseError("The release manifest changed during validation.")
        if commands.text("git", "diff", "HEAD", "--", "package.json"):
            commands.run("git", "add", "--", "package.json")
            commands.run("git", "diff", "--cached", "--check")
            commands.run("git", "commit", "-m", f"chore(release): prepare {tag}")
            committed = commands.text("git", "rev-parse", "HEAD")
            if commands.text("git", "rev-parse", "HEAD^") != head or commands.text("git", "diff", "--name-only", head, committed) != "package.json":
                raise ReleaseError("The commit changed more than release metadata; inspect hook or concurrent changes before retrying.")
            head = committed
        working_tree(commands)
        if json.loads(commands.text("git", "show", "HEAD:package.json")) != expected:
            raise ReleaseError("The committed release manifest was changed by a hook; inspect before retrying.")
    print(f"Publishing {tag} from {head[:12]}...", flush=True)
    if not local:
        if remote:
            commands.run("git", "fetch", "origin", f"refs/tags/{tag}:refs/tags/{tag}")
        else:
            commands.run("git", "tag", "-a", tag, "-m", f"Release {tag}", head)
    working_tree(commands)
    if (commands.text("git", "rev-parse", "HEAD") != head
            or commands.text("git", "branch", "--show-current") != branch
            or commands.text("git", "rev-parse", f"refs/tags/{tag}^{{commit}}") != head):
        raise ReleaseError("The prepared commit or tag changed before push.")
    # Publish both refs together; never force or push unrelated tags.
    commands.run("git", "push", "--atomic", "--no-follow-tags", "origin",
                 f"{head}:refs/heads/{branch}", f"refs/tags/{tag}", timeout=300)
    wait_for_run(commands, repo, workflow, tag, head, retry_failed=remote is not None)
    print("Confirming npm and GitHub publication...", flush=True)
    live = published_version(commands, expected["name"], version)
    dist_tag = "next" if "-" in version else "latest"
    tags = commands.json("npm", "view", expected["name"], "dist-tags", "--json")
    github = commands.json("gh", "api", f"repos/{repo}/releases/tags/{tag}")
    if not live or not live.get("dist.integrity") or (live.get("gitHead") and live["gitHead"] != head):
        raise ReleaseError("npm publication is absent or does not match the release commit.")
    if tags.get(dist_tag) != version:
        raise ReleaseError(f"The version is published but npm {dist_tag} is {tags.get(dist_tag)!r}; inspect registry state before retrying.")
    if github.get("draft") or github.get("prerelease") != ("-" in version) or remote_tag(commands, tag) != head:
        raise ReleaseError("GitHub release or tag does not match the expected publication.")
    check_published_tarball(commands, expected, live)
    print(f"Released {expected['name']}@{version} ({dist_tag}).\n{github['html_url']}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="Running this command publishes the release. Retry the same version to resume; use a new version after source changes.")
    parser.add_argument("version", type=version_argument, help="release version, e.g. 0.2.0 or 0.3.0-rc.1")
    args = parser.parse_args()
    descriptor, name = tempfile.mkstemp(prefix="agentskills-release-", suffix=".log")
    os.close(descriptor)
    log = Path(name)
    print(f"Log: {log}", flush=True)
    try:
        release(Commands(ROOT, log), args.version)
    except (ReleaseError, OSError, ValueError, KeyError) as error:
        print(f"Release stopped: {error}\nLog: {log}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"Release interrupted. Rerun the same command to inspect its outcome.\nLog: {log}", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
