### Authoring or modifying a skill

**You own the skill's voice.**

1. Use the harness's skill-authoring skill when one is installed, such as **skill-creator**. Do not copy a plugin skill into this repository. Otherwise write `SKILL.md` with `name` and `description` frontmatter. Keep it thin, follow the repo's AGENTS.md conventions, test the description trigger, and reference other skills by path.
2. Validate the skill: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve. In the astack checkout, run `python3 scripts/check_skills.py`, then `./install.sh --dry-run`.
3. Test cases if structural. Skip if subjective.
4. Run **Opening a PR** (`playbooks/opening-a-pr.md`).

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per the **encode-lessons-in-structure** principle skill. Delegate to other skills by path. Don't restate. A workflow you keep hitting but isn't captured → propose a new skill.

**Reply:** summary of the skill, key design decisions, validation notes.
