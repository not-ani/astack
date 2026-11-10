# astack

Ani's central repository for personal agent skills. It contains the 58 skills from Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/236e5481d05cbadc315b374a5de54971858c27bb/pstack), adapted to T3 Code using [p3-stack](https://github.com/uzairansaruzi/p3-stack), and [under-the-hood](skills/under-the-hood/SKILL.md).

## Install locally

Run from this checkout:

```bash
./install.sh --dry-run
./install.sh
```

The installer links each skill directly to this checkout from `~/.agents/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`. Editing a skill here updates every installation. It also links the existing model settings from `p3-models.md` into `~/.agents/p3-models.md`.

To replace conflicting skill copies and delete other personal skills:

```bash
./install.sh --prune --dry-run
./install.sh --prune
```

Pruning includes broken links and nested personal skill folders. It clears the old Skills CLI records and removes discarded skills from managed global instruction blocks. It preserves plugin caches, Codex's `.system` skills and `codex-primary-runtime` directory, and Claude's `synced` bundle. Rerunning the installer leaves correct links untouched. Python 3 is required.

The old `~/p3-stack` checkout remains an upstream source copy. Installed personal skills resolve to `astack`.

## Use the skills

Invoke `/p3-mode` for the p3 workflows, `/setup-p3` to configure models, or `/p3-help` to find a workflow. The p3 playbooks and references are bundled with their skills. Supporting agent prompts are in `agents/`.

The current upstream collection also includes `/create-formal-verification-skill`, `/maintain-formal-verification-skill`, and `/statechart` for checking system behavior, `/ketchup` and `/ketchup-video` for catching up, `/sharpen` for deepening a task, and `/in-your-own-words` for restating its goal.

Upstream source hashes, adaptation rules, and validation commands are recorded in the [pstack update guide](docs/pstack/README.md).

`under-the-hood` creates an interactive HTML slideshow explaining a PR, branch, or subsystem through its data shapes and state transitions. It includes the slideshow template, build scripts, and fonts. For example:

> Use under-the-hood to walk me through this PR and prepare me to explain its design at a whiteboard.

To install only that skill from GitHub with the Skills CLI:

```bash
npx skills add not-ani/astack --skill under-the-hood
```

Add `-g` for a global installation. Use the local installer above when this checkout should own the installed files.

## Credits

The p3 skills adapt Lauren Tan's pstack for T3 Code. Both the [pstack MIT license](LICENSE.pstack) and the [p3 adaptation license](LICENSE.p3-stack) are included. The slideshow's Geist fonts use the [SIL Open Font License](skills/under-the-hood/assets/slideshow/fonts/OFL.txt).
