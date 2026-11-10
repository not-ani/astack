#!/usr/bin/env python3
"""Record and check coverage of the pinned upstream pstack collection."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "pstack.lock.json"
RENAMES = {
    "poteto-mode": "p3-mode",
    "poteto-help": "p3-help",
    "setup-pstack": "setup-p3",
    "poteto-agent.md": "p3-agent.md",
}
EXCLUSIONS = {
    "skills/poteto-mode/scripts/watch-pr/": "T3 watch_pull_request owns PR event delivery and monitoring.",
    "skills/poteto-mode/scripts/bootstrap.ts": "Bootstraps dependencies for the replaced upstream PR watcher.",
    "skills/poteto-mode/scripts/bun.lock": "Dependency lock for the replaced upstream PR watcher.",
    "skills/poteto-mode/scripts/package.json": "Watcher dependency package; adapted standalone checks need no watcher dependencies.",
}


def destination(source):
    if source == "LICENSE":
        return "LICENSE.pstack"
    return "/".join(RENAMES.get(part, part) for part in source.split("/"))


def exclusion(source):
    for prefix, reason in EXCLUSIONS.items():
        if source == prefix or prefix.endswith("/") and source.startswith(prefix):
            return reason
    return None


def snapshot(upstream):
    revision = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    tracked = subprocess.check_output(["git", "-C", str(upstream), "ls-files", "--", "skills", "agents", "LICENSE"], text=True).splitlines()
    files = [upstream / name for name in tracked]
    sources = {str(p.relative_to(upstream)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    return {
        "repository": "https://github.com/cursor/plugins",
        "revision": revision,
        "path": "pstack",
        "renames": RENAMES,
        "files": sources,
        "excluded": {name: reason for name in sources if (reason := exclusion(name)) and not (ROOT / destination(name)).is_file()},
    }


def validate(data):
    errors = []
    sources = data["files"]
    for source in sources:
        if source in data["excluded"]:
            if not data["excluded"][source]:
                errors.append(f"Missing exclusion reason: {source}")
            continue
        path = ROOT / destination(source)
        if not path.is_file():
            errors.append(f"Missing adapted upstream file: {path}")
    upstream_skills = {destination(name).split("/")[1] for name in sources if name.startswith("skills/") and name.count("/") == 2 and name.endswith("/SKILL.md")}
    installed_skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    if installed_skills != upstream_skills | {"under-the-hood"}:
        errors.append(f"Skill inventory mismatch: missing {sorted(upstream_skills - installed_skills)}, extra {sorted(installed_skills - upstream_skills - {'under-the-hood'})}")
    if "skills/under-the-hood/SKILL.md" in sources:
        errors.append("The local under-the-hood skill must remain outside upstream synchronization.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, help="Path to pstack in a fetched cursor/plugins checkout.")
    parser.add_argument("--write", action="store_true", help="Record a reviewed upstream snapshot after coverage passes.")
    args = parser.parse_args()
    if args.write and not args.upstream:
        parser.error("--write requires --upstream")
    if args.upstream:
        data = snapshot(args.upstream.resolve())
        if not args.write:
            recorded = json.loads(LOCK.read_text())
            if data != recorded:
                parser.error("Upstream differs from pstack.lock.json. Review the update before recording it.")
    else:
        data = json.loads(LOCK.read_text())
    errors = validate(data)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    if args.write:
        LOCK.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    skills = sum(name.count("/") == 2 and name.endswith("/SKILL.md") for name in data["files"])
    print(f"Verified coverage of {skills} upstream skills at {data['revision'][:12]}, {len(data['files']) - len(data['excluded'])} ported files, and {len(data['excluded'])} documented T3 substitutions.")


if __name__ == "__main__":
    main()
