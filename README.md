# astack

Ani's agent skills.

## Install

Install `under-the-hood` with the [Skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add not-ani/astack --skill under-the-hood
```

Choose your coding agent when prompted. Add `-g` to install globally instead of in the current project.

This command installs the current files from GitHub. To install the fixed `v1.0.0` release:

```bash
npx skills add https://github.com/not-ani/astack/tree/v1.0.0 --skill under-the-hood
```

## Update

Update an existing project installation:

```bash
npx skills update under-the-hood
```

Add `-g` for a global installation. To reinstall the same fixed release, use its release-specific install command.

## Skills

- [under-the-hood](skills/under-the-hood/SKILL.md) creates an interactive HTML slideshow that explains a PR, branch, or subsystem through its data shapes and state transitions. Includes the slideshow template, build scripts, and fonts.

View [under-the-hood on skills.sh](https://skills.sh/not-ani/astack/under-the-hood).

After installing, ask your agent:

> Use under-the-hood to walk me through this PR and prepare me to explain its design at a whiteboard.

The template uses fictional software examples. Adapt its layouts to your codebase; replace the example code, states, and source captions.

The bundled Geist fonts use the [SIL Open Font License](skills/under-the-hood/assets/slideshow/fonts/OFL.txt).
