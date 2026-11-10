---
name: setup-p3
description: Configure which models p3-stack uses per role and at what reasoning budget. Detects your available T3 models and writes p3-models.md, which overrides the skill defaults. Use for /setup-p3, "configure p3 models", "p3 budget", or changing p3-stack's model choices.
---

# Setup p3

Write `p3-models.md`, a file that sets p3-stack's model per role. Default location is the current project root. Offer `~/.agents/p3-models.md` as the global option, and ask which one. A project file wins over the global one. `./install.sh` links `~/.agents/p3-models.md` to `p3-models.md` in the astack checkout, so writing the global file edits that checkout's copy.

## Steps

### 1. Detect available models

Call `orchestrator_capabilities`. It lists the providers and models you can pass to `delegate_task` in this session, custom models included, with each one's provider instance ID and the options it accepts, such as reasoning effort or speed. That is the dependable source. Use its `search` to find a model the short list leaves out. If it returns nothing, stop and tell the user. Never write a provider or model it did not return. The aliases `inherit-parent` and `auto` are always valid even though they are not detected models.

### 2. Load current state

The roles are the labels shown in step 5. If `p3-models.md` already exists at the chosen location, read it and treat its `# budget` line and its role values as the current choices. Keep every comment line the user added beyond the standard header, such as a provider override note. Otherwise start from the mapping in step 3(b). A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask with the harness's question tool when it has one, otherwise in plain text. Offer these four options with these exact labels, and name the current budget when the file records one. With no file, say that `large` matches the starting level p3-mode assumes.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table. On a fresh run, give code roles (`feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`) and the explorer, investigator, swarm, and `reflect tooling` roles the fastest strong coding model detected. Give `judgment and prose`, `hardest tasks`, the explainer, and the synthesizers the most capable model detected. Fill each panel role with one entry per distinct provider detected, up to three. On a re-run, keep any role the user changed by provider, model, list, or alias (`inherit-parent`, `auto`).

`unlimited`, `large`, `medium`, and `small` set the effort of every real entry, panel entries included, to `max`, `xhigh`, `high`, or `medium`. The ladder is `max` > `xhigh` > `high` > `medium` > `low`. Effort is an option the catalog lists for a model, never part of its name. If the model does not list the target, use the highest listed level at or below it, else mark the role as needing a choice. When the catalog lists no effort option for a model, write no effort for it. The budget label is still recorded. `inherit-parent` and `auto` do not change. Speed is not recorded here, because p3-mode picks a fast speed per spawn only for urgent work.

**(c) Show the roles and confirm.** Show every role with its model, marking any entry not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, with the harness's question tool when it has one, offering the detected models plus `inherit-parent` and `auto` as the options. Both aliases mean this role runs on the parent thread's model, so p3-mode omits the `delegate_task` model. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one delegate runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena runs one judge. It tries only values from a provider family other than the parent's, in list order, so order it by preference. An `inherit-parent` or `auto` value never judges. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real entry written must be in the `orchestrator_capabilities` result, under the provider instance it came from, and every effort must be an option that model lists. `inherit-parent` and `auto` always pass. If a chosen entry is not available, stop and ask again. Never swap in another model on your own.

### 5. Write the file

Write `p3-models.md` with a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels p3-mode uses. Write each entry as `<providerInstanceId>/<model>`, followed by its effort in parentheses when step 3(b) set one. Overwrite the whole file so re-runs stay idempotent, carrying forward the user's comment lines from step 2 after the standard header. Shape:

```
# p3 model configuration. One line per role. Delete a line to use the calling skill's documented default, or the parent model when no default exists.
# `inherit-parent` or `auto` as a value: the role runs on the parent thread's model (omit the delegate_task model). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: <providerInstanceId>/<model> (<effort>)
bug-fix: <providerInstanceId>/<model> (<effort>)
perf-issue: <providerInstanceId>/<model> (<effort>)
hillclimb: <providerInstanceId>/<model> (<effort>)
judgment and prose: <providerInstanceId>/<model> (<effort>)
hardest tasks: <providerInstanceId>/<model> (<effort>)
how explorer: <providerInstanceId>/<model> (<effort>)
how explainer: <providerInstanceId>/<model> (<effort>)
why investigators: <providerInstanceId>/<model> (<effort>)
why synthesizer: <providerInstanceId>/<model> (<effort>)
reflect tooling: <providerInstanceId>/<model> (<effort>)
reflect judgment, divergent, synthesizer: <providerInstanceId>/<model> (<effort>)
arena runners: <entry>, <entry>, <entry>
arena cross-judge pool: <entry>, <entry>, <entry>
swarm workers: <providerInstanceId>/<model> (<effort>)
architect runners: <entry>, <entry>, <entry>
interrogate reviewers: <entry>, <entry>, <entry>
```

### 6. Confirm

Tell the user the file was written, where, and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, invoke `/create-formal-verification-skill`. On no, move on without pushing.
