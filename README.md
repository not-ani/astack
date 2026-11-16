# astack

Ani's personal collection of agent skills. It's a working set: I pull in skills from other people's stacks, adapt them, and drop the ones I stop using. Most of the skills here were not written by me. See [Credits](#credits) for where each one comes from.

## Skills

**Understanding code and changes**

- `under-the-hood`: Explains a PR, branch, or subsystem through its data shapes and state transitions, then hands the outline to `create-slideshow` (or another presentation skill).
- `blast-radius`: Finds what a change could break outside the diff, and proves the key safety fact by running real code.
- `statechart`: Checks a TLA+ model of a stateful system and draws it as a Mermaid statechart.

**Verification**

- `create-verification-skill` / `maintain-verification-skill`: Generate and maintain a project-local skill that drives your app the way a user would.
- `create-formal-verification-skill` / `maintain-formal-verification-skill`: Generate and maintain formal verification for the code where bugs cost the most.
- `review-loop`: Runs rounds of review on your changes and makes the smallest fixes that resolve the findings.
- `prove-and-file`: Takes work from its current state to a merged PR without the user watching.

**Writing and communication**

- `create-slideshow`: Builds an interactive, offline HTML slideshow on any subject, with step-by-step diagrams, quoted sources, and speaker notes.
- `ketchup` / `ketchup-video`: Catch you up on what happened in the chat and list what's waiting on you.
- `bro`: Restates the last message in plain language.
- `unslop`: Removes AI tells from writing.
- `technical-writing`: A layered standard for docs, RFCs, and READMEs.
- `no-comments`: Runs the Comment Sicko reviewer (`agents/comment-sicko.md`) and fixes the findings it accepts.

## Install locally

Run from this checkout:

```bash
./install.sh --dry-run
./install.sh
```

The installer links each skill from `~/.agents/skills/`, `~/.claude/skills/`, and `~/.codex/skills/` back to this checkout, so editing a skill here updates it everywhere.

To replace conflicting copies and delete every other personal skill:

```bash
./install.sh --prune --dry-run
./install.sh --prune
```

Pruning also removes broken links, nested personal skill folders, old Skills CLI records, and managed instruction blocks for skills that no longer exist. It leaves plugin caches, Codex's `.system` skills and `codex-primary-runtime` directory, and Claude's `synced` bundle alone. Running the installer again leaves correct links untouched.

## Install one skill from GitHub

```bash
npx skills add not-ani/astack --skill under-the-hood
```

Add `-g` for a global install. Use the local installer instead if you want this checkout to own the installed files.

## Updating from upstream

Upstream source hashes, adaptation rules, and validation commands are in the [pstack update guide](docs/pstack/README.md). The pinned pstack revision is in `pstack.lock.json`.

## Credits

- [pstack](https://github.com/cursor/plugins/tree/236e5481d05cbadc315b374a5de54971858c27bb/pstack) by Lauren Tan: `blast-radius`, `bro`, `statechart`, `ketchup`, `ketchup-video`, `unslop`, `technical-writing`, `no-comments`, and the verification skills. Licensed under [MIT](LICENSE.pstack).
- [p3-stack](https://github.com/uzairansaruzi/p3-stack): the T3 Code adaptation of pstack used here. See [its license](LICENSE.p3-stack).
- [tstack](https://github.com/t3dotgg/tstack/): ideas and skills I've borrowed.
- `under-the-hood` and `create-slideshow` are mine. The slideshow's Geist fonts use the [SIL Open Font License](skills/create-slideshow/assets/slideshow/fonts/OFL.txt).
