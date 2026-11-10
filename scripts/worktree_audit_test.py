import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1] / "skills/p3-mode/scripts/worktree-audit.sh"


class WorktreeAuditTest(unittest.TestCase):
    def test_paths_and_unmerged_work_are_preserved(self):
        with tempfile.TemporaryDirectory(prefix="astack-worktree-") as directory:
            root = Path(directory).resolve()
            repo = root / "repo"
            tools = root / "bin"
            tools.mkdir()

            def git(*args, cwd=repo):
                return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()

            subprocess.run(["git", "init", "-b", "main", str(repo)], check=True, capture_output=True)
            for key, value in {"user.name": "Audit fixture", "user.email": "audit@example.invalid", "commit.gpgsign": "false", "core.hooksPath": str(root / "hooks")}.items():
                git("config", key, value)
            git("commit", "--allow-empty", "-m", "base")
            paths = {}
            for name in ("merged", "open", "closed", "unpushed", "behind"):
                path = root / f"worktree {name}"
                git("worktree", "add", "-b", name, str(path))
                if name != "merged":
                    git("commit", "--allow-empty", "-m", name, cwd=path)
                if name in ("open", "closed"):
                    git("update-ref", f"refs/remotes/origin/{name}", git("rev-parse", "HEAD", cwd=path))
                if name == "behind":
                    tip = git("commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "remote change", cwd=path)
                    git("update-ref", "refs/remotes/origin/behind", tip)
                paths[name] = str(path)
            prs = [{"number": 1, "state": "OPEN", "headRefName": "open"}, {"number": 2, "state": "CLOSED", "headRefName": "closed"}]
            (tools / "gh").write_text("#!/usr/bin/env python3\nprint(" + repr(json.dumps(prs)) + ")\n")
            (tools / "origin").write_text("#!/bin/sh\nexit 1\n")
            for path in tools.iterdir():
                path.chmod(0o755)
            env = {**os.environ, "PATH": str(tools) + os.pathsep + os.environ["PATH"]}
            result = subprocess.run(["bash", str(AUDIT), "-b", "main", str(repo)], check=True, capture_output=True, text=True, env=env)
            rows = [line.split("\t") for line in result.stdout.splitlines() if line and not line.startswith(("#", "SIZE"))]
            buckets = {row[-1]: row[-2] for row in rows}
            self.maxDiff = None
            self.assertEqual(buckets, {paths["merged"]: "safe", paths["open"]: "hold-open-pr", paths["closed"]: "review", paths["unpushed"]: "hold-unpushed", paths["behind"]: "review"})
            self.assertEqual(next(row[4] for row in rows if row[-1] == paths["behind"]), "behind1")


if __name__ == "__main__":
    unittest.main()
