#!/usr/bin/env python3
"""Check skill metadata, local links, and T3 orchestration instructions."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")
FORBIDDEN = {
    r"\bsubagent_type\s*:": "use native delegation or delegate_task",
    r"\brun_in_background\s*:": "use the delegate's supported execution mode",
    r"\bTask\s*\(": "use native delegation or delegate_task",
    r"\bTask tool\b": "use the T3 delegation contract",
    r"\btask_status\b": "follow the delegate's next instruction",
    r"\b(?:t3_thread_launch|create_threads|workspaceStrategy)\b": "top-level thread tools require an explicit user request",
    r"\bgit\s+reset\s+--hard\b": "preserve shared work and use tool-created child isolation",
    r"\b(?:gh|origin)\s+pr\s+[^`\n]*--watch\b": "use watch_pull_request",
    r"scripts/watch-pr": "use watch_pull_request",
    r"\bagent-transcripts/": "use t3_thread_read and t3_thread_search",
    r"\b(?:poteto-mode|poteto-help|setup-pstack|poteto-agent)\b": "use the p3 skill and agent names",
}
REQUIRED_T3 = {
    "skills/p3-mode/SKILL.md": ("delegate_task", "orchestrator_capabilities", "p3-models.md"),
    "skills/setup-p3/SKILL.md": ("orchestrator_capabilities", "p3-models.md"),
    "skills/p3-mode/playbooks/babysit.md": ("watch_pull_request",),
    "skills/p3-mode/playbooks/shipping.md": ("watch_pull_request",),
    "skills/p3-mode/playbooks/session-pickup.md": ("t3_thread_read",),
    "skills/p3-mode/playbooks/eval.md": ("t3_thread_read",),
}


def is_prohibition(line, match):
    before = re.split(r"(?<=[.!?;])\s+", line[:match.start()])[-1]
    if re.search(r"\b(?:never|do not|don't)\b[^.!?;]*$", before, flags=re.I):
        return True
    return bool(re.search(r"\b(?:instead of|rather than|replaces?)\s*`?$", before, flags=re.I))


def is_requested_thread_rule(line, match):
    if match.group() not in {"t3_thread_launch", "create_threads", "workspaceStrategy"}:
        return False
    before = re.split(r"(?<=[.!?;])\s+", line[:match.start()])[-1]
    after = re.split(r"(?<=[.!?;])\s+", line[match.start():])[0]
    sentence = before + after
    if re.search(r"only (?:when|if).*user.*(?:asks?|requests?).*(?:new|top-level) thread", sentence, flags=re.I):
        return True
    return bool(re.search(r"\b(?:make|makes|create|creates) (?:new )?top-level threads", sentence) and re.search(r"only.*user.*(?:asks?|requests?)", line, flags=re.I))


def check(root):
    errors = []
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        return ["No skills found."]
    for relative, tools in REQUIRED_T3.items():
        path = root / relative
        if path.is_file():
            text = path.read_text()
            for tool in tools:
                if tool not in text:
                    errors.append(f"{path}: preserve the T3 mechanism {tool}")
    for path in skill_files:
        text = path.read_text()
        frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, flags=re.S)
        if not frontmatter:
            errors.append(f"{path}: missing frontmatter")
            continue
        fields = frontmatter.group(1)
        for key in ("name", "description"):
            match = re.search(rf"^{key}:\s*(\S.*)$", fields, flags=re.M)
            if not match:
                errors.append(f"{path}: missing {key}")
            elif key == "name" and match.group(1).strip("\"'") != path.parent.name:
                errors.append(f"{path}: name must match its directory")
        if re.search(r"^(icon|color|mode|reminder):", fields, flags=re.M):
            errors.append(f"{path}: remove Cursor-only frontmatter")

    markdown = sorted((root / "skills").rglob("*.md")) + sorted((root / "agents").rglob("*.md"))
    for path in markdown:
        if "test" in path.relative_to(root).parts:
            continue
        text = path.read_text()
        in_code = False
        for number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if not in_code:
                prose = re.sub(r"`[^`]*`", "", line)
                for match in LINK.finditer(prose):
                    target = unquote(match.group(1).strip("<>"))
                    if target == "url" and path.name.endswith("-prompt.md"):
                        continue
                    parsed = urlsplit(target)
                    if parsed.scheme or target.startswith(("#", "/", "~")):
                        continue
                    destination = path.parent / parsed.path
                    if not destination.exists():
                        errors.append(f"{path}:{number}: missing link {target}")
            for pattern, replacement in FORBIDDEN.items():
                for match in re.finditer(pattern, line):
                    if not is_prohibition(line, match) and not is_requested_thread_rule(line, match):
                        errors.append(f"{path}:{number}: {replacement}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check(args.root)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"Metadata, local links, and selected T3 instruction checks passed for {len(list((args.root / 'skills').glob('*/SKILL.md')))} skills.")


if __name__ == "__main__":
    main()
