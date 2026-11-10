#!/usr/bin/env python3
"""Link astack's skills into personal agent folders."""

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def remove(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing.")
    parser.add_argument("--prune", action="store_true", help="Delete other personal skills and replace conflicting copies.")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Override the user home, including for isolated verification.")
    args = parser.parse_args()
    skills = {p.name: p for p in sorted((ROOT / "skills").iterdir()) if (p / "SKILL.md").is_file()}
    if not skills:
        parser.error("No source skills found; refusing to change installations.")
    home = args.home.expanduser().resolve()
    links = []
    removals = []
    for agent in (".agents", ".claude", ".codex"):
        target = home / agent / "skills"
        if target.is_symlink():
            parser.error(f"Expected a real skills directory: {target}")
        protected = {
            ".codex": {".system", "codex-primary-runtime"},
            ".claude": {"synced"},
        }.get(agent, set())
        for entry in sorted(target.iterdir()) if target.exists() else []:
            if args.prune and entry.name not in skills and entry.name not in protected:
                if entry.is_dir() or entry.is_symlink():
                    removals.append(entry)
        for name, source in skills.items():
            dest = target / name
            if dest.is_symlink() and dest.resolve() == source:
                continue
            if dest.exists() and not dest.is_symlink() and not args.prune:
                parser.error(f"Conflicting copy: {dest}. Use --prune to replace it.")
            links.append((dest, source))

    config = ROOT / "p3-models.md"
    if config.is_file():
        dest = home / ".agents" / "p3-models.md"
        if not (dest.is_symlink() and dest.resolve() == config):
            if dest.exists() and not dest.is_symlink() and dest.read_bytes() != config.read_bytes() and not args.prune:
                parser.error(f"Conflicting model settings: {dest}.")
            links.append((dest, config))

    edits = {}
    if args.prune:
        lock = home / ".agents" / ".skill-lock.json"
        if lock.is_file():
            data = json.loads(lock.read_text())
            data["skills"] = {}
            edits[lock] = json.dumps(data, indent=2) + "\n"
        for path in (home / ".claude" / "CLAUDE.md", home / ".codex" / "AGENTS.md"):
            if not path.is_file():
                continue

            def update_block(match):
                lines = []
                for line in match.group().splitlines():
                    marker = re.search(r"<!-- skill:([^ ]+) -->", line)
                    if marker:
                        name = marker.group(1)
                        if name not in skills:
                            continue
                        line = re.sub(r"\]\([^)]*/SKILL\.md\)", f"]({skills[name]}/SKILL.md)", line, count=1)
                    lines.append(line)
                return "\n".join(lines)

            edits[path] = re.sub(r"<!-- create-skill\.sh:skills:start -->.*?<!-- create-skill\.sh:skills:end -->", update_block, path.read_text(), flags=re.S)
    edits = {p: body for p, body in edits.items() if p.read_text() != body}
    print(f"{'Would create' if args.dry_run else 'Creating'} {len(links)} links, remove {len(removals)} other entries, update {len(edits)} metadata files.")
    for path in removals:
        print(f"remove {path}")
    if args.dry_run:
        return
    for path in removals:
        remove(path)
    for dest, source in links:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() or dest.is_symlink():
            remove(dest)
        dest.symlink_to(source, target_is_directory=source.is_dir())
    for path, body in edits.items():
        path.write_text(body)
    for agent in (".agents", ".claude", ".codex"):
        for name, source in skills.items():
            dest = home / agent / "skills" / name
            if not dest.is_symlink() or dest.resolve() != source or not (dest / "SKILL.md").is_file():
                raise RuntimeError(f"Invalid skill link: {dest}")
    print(f"Verified {len(skills)} skill links in each of .agents, .claude, and .codex.")


if __name__ == "__main__":
    main()
