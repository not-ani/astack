# astack

Personal skills live in `skills/`. Edit them here, then run `./install.sh` to link them into the user-level Agents, Claude, and Codex folders. `--dry-run` previews changes. `--prune` also deletes other personal skills and replaces conflicting copies. Plugin and built-in skills are excluded.

Lauren Tan's pstack owns the p3 skills' behavior and wording. The original `~/p3-stack` supplies T3 adaptation conventions. For upstream updates, read `docs/pstack/README.md` and validate against `pstack.lock.json`. Keep `under-the-hood` and the user's `p3-models.md` outside synchronization.

Supporting prompts live in `agents/`; resolve those paths from this repository when reading an installed skill. Preserve both `LICENSE.pstack` and `LICENSE.p3-stack`.
