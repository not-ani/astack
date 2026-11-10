# Updating the pstack adaptation

Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/236e5481d05cbadc315b374a5de54971858c27bb/pstack) owns the skill behavior and wording. The original p3 codebase supplies the T3 Code adaptation conventions. This repository is the installed, editable copy.

The upstream revision is recorded in [pstack.lock.json](../../pstack.lock.json). It lists the source file hashes and every omitted helper with its T3 replacement. It covers the top-level skill collection and supporting agent prompts. The separate Benny automation package, Cursor plugin registration, marketing assets, and Cursor installation guides are outside this port.

## Preserve behavior and adapt the harness

Keep upstream instructions when they apply to T3 Code. Change tool calls, installation paths, model configuration, transcript access, and lifecycle rules to match the actual T3 runtime. Retain the local names `p3-mode`, `p3-help`, `setup-p3`, and `p3-agent`.

Use native delegation for a child on the same provider and model with inherited settings. Use `delegate_task` for cross-provider work, explicit settings, or child worktree isolation. Resolve available models and settings through `orchestrator_capabilities`, then read the user's named roles from `p3-models.md`. Preserve the role's model family and review diversity. Report an unavailable requested model rather than silently replacing it.

Follow a delegated run's `next` instruction. T3 owns completion delivery. PR monitoring uses `watch_pull_request`, and only the parent watches. Top-level threads require a user request. User-only credentials use `request_secret`. These rules replace Cursor-specific Task arguments, transcript files, PR polling, and cloud-agent setup.

Keep `under-the-hood`, the user's model settings, and installed plugin or built-in skills outside upstream synchronization.

## Validate an update

Run the structural checks from this repository:

```bash
python3 scripts/check_skills_test.py
python3 scripts/worktree_audit_test.py
python3 scripts/check_skills.py
python3 scripts/check_pstack.py
./install.sh --dry-run
```

The checks cover skill names and descriptions, local Markdown links, obsolete orchestration instructions, and upstream file coverage. They do not prove that prose produces the intended behavior in every future agent run. Review semantic changes against the pinned source too.

To compare a fetched upstream checkout with the recorded source:

```bash
python3 scripts/check_pstack.py --upstream /path/to/plugins/pstack
```

After reviewing and porting a new revision, record it with the same command and `--write`. Missing source files fail the check unless their omission has an explicit T3 substitution in the script. A source hash is provenance, not proof of an unchanged local port.

Run the bundled helper tests when their code changes. Then run `./install.sh` to link newly added skills. Existing skill links already read their updated files from this checkout. Do not use `--prune` for routine upstream updates.

The [decision trail](decisions.tsv) records this synchronization's choices and evidence. Both Lauren's [upstream license](../../LICENSE.pstack) and the [p3 adaptation license](../../LICENSE.p3-stack) are retained.
