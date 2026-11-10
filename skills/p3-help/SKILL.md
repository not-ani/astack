---
name: p3-help
description: Guides users through p3-stack setup, /p3-mode, and picking the skill, playbook, or principle for a task. Type /p3-help with a question.
disable-model-invocation: true
---

# P3 help

Answer the user's question about p3-stack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a p3-stack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use p3-stack to fix this bug", is not a help question. Read [`p3-mode`](../p3-mode/SKILL.md), do the work under it, and mention once that starting each task with `/p3-mode` keeps the work in this style.

This file maps questions to the skills and playbooks that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here are relative to this skill. Give the user the file's absolute path in their astack checkout, which this skill's real path points into.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/p3-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make p3-stack my own

Check the state that changes the answer, and mention it only when it does:

- No `p3-models.md` in the project root and none at `~/.agents/p3-models.md` means `/setup-p3` hasn't run for this user, so every role runs on the parent model. `./install.sh` links the astack checkout's `p3-models.md` to `~/.agents/p3-models.md`, so a missing global file usually means the installer hasn't run.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `/create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `/maintain-formal-verification-skill` if the question touches that code.

When the model file is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per thread. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/setup-p3` to type, and answer their question too.
- Later: answer their question, and add one line saying every role runs on the parent model until they run `/setup-p3`.

## Get set up

1. Run `./install.sh` from the astack checkout. It links every skill into the personal Agents, Claude, and Codex skill folders (`~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/`) and links `p3-models.md` to `~/.agents/p3-models.md`. Run `./install.sh --dry-run` first to preview. `--prune` also replaces conflicting copies and removes other personal skills, and it keeps plugin, built-in, and Claude-synced skills. There is no per-project install. Editing a skill in the checkout updates every installation.
2. Run [`/setup-p3`](../setup-p3/SKILL.md). It reads the models T3 offers, asks for a reasoning budget, maps a model to each role, and writes `p3-models.md`. The file applies to new sessions. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `/p3-mode`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. Only `/setup-p3` loads from the user's words. The [README](../../README.md) has the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. p3-stack spends extra tokens on delegates and review panels. Rerun `/setup-p3` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the parent thread's model, which saves tokens when that model is cheaper. A shorter panel list runs fewer delegates, one for each entry. Save `/p3-mode` for work that needs rigor.

p3-stack is the T3 Code adaptation of pstack. The skills use the Agent Skills format, so Claude Code and Codex both load them from the folders `./install.sh` links. The orchestration steps call T3 Code tools: `delegate_task` and `orchestrator_capabilities` for delegates and their models, `link_pull_request` and `watch_pull_request` for PRs, `schedule_task` for audit ticks, `html_preview` and `html_render` for visuals, and `preview_*` and `device_*` for browser and simulator work. Outside a T3 Code session those tools are absent, so those steps need a substitute or get skipped with a one-line note.

## Start a task with `/p3-mode`

`/p3-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one.

Skills are invoked by name. There are no mode toggles, so `/p3-mode` applies to the message that invokes it and fades as the thread moves on. Start each new task with `/p3-mode`. Mid-thread, "new task" makes the mode match a fresh playbook. `/p3-mode` already opens every delegate brief with `agents/p3-agent.md` from the astack checkout. To get the same style from a delegate of your own, open its brief with that file and include the absolute path to the installed `p3-mode` skill.

## Pick a skill

The default answer is `/p3-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/p3-mode`](../p3-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`/how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/teach`](../teach/SKILL.md) |
| Walk through a PR, branch, or subsystem as an interactive slideshow of its data shapes and state transitions | [`/under-the-hood`](../under-the-hood/SKILL.md) |
| Catch up on their own recent work on a topic | [`/recall`](../recall/SKILL.md) |
| Catch up on what changed in this thread since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/ketchup`](../ketchup/SKILL.md) |
| Catch up like `/ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`/ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as delegated child tasks | [`/swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`/unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`/statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/setup-p3`](../setup-p3/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/correct`](../correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`/make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around p3-stack | `/p3-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `/how` explains what the code does. `/why` explains the reasons. `/teach` runs one or both and explains the result plainly. `/under-the-hood` presents the same tracing as a slideshow to step through.
- `/arena` gives every worker the same brief and merges the best parts. `/swarm` splits work into slices or a race and returns one report.
- `/architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `/interrogate` reviews the diff. `/blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/recall` rebuilds context across recent threads. `/ketchup` covers only this thread since the user's last message. Resuming one specific thread, delegated task, or branch is the Session pickup playbook.
- `/figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in p3-stack:

- p3-stack ships no `deslop`, `control-cli`, or `control-ui` skill. `/p3-mode` uses an installed `deslop` skill when the harness has one and strips slop from the diff directly otherwise. It proves changes through the project's `verify-*` skill, real commands and runtime APIs, the `device_*` tools for simulators, and the `preview_*` tools when the request is browser work.
- Skill authoring uses the harness's skill-authoring skill, such as skill-creator, when one is installed, and the authoring playbook otherwise.
- p3-stack has no `/orchestrate` skill. Orchestrate is a `/p3-mode` playbook. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `/p3-mode`, not skills, so they have no slash command. Inside `/p3-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready with `watch_pull_request` and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

The Playbooks section of [`p3-mode`](../p3-mode/SKILL.md) lists every playbook and when it applies. [Opening a PR](../p3-mode/playbooks/opening-a-pr.md), [Babysit](../p3-mode/playbooks/babysit.md), and [Shipping](../p3-mode/playbooks/shipping.md) cover opening, babysitting, and landing a PR.

p3-stack has no planning skill. For work that spans phases or stacked PRs, asking `/p3-mode` for a plan runs the [Multi-phase plan playbook](../p3-mode/playbooks/multi-phase-plan.md), which writes the plan, checks it with `scripts/check-plan.mjs`, and doesn't implement it. For a design question, the Prototype playbook or `/architect` settles it in code first.

Principles are one-rule skills that `/p3-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/principle-<name>` still loads one on demand. The Principles section of [`p3-mode`](../p3-mode/SKILL.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | There is no mode to keep on. Start each new task with `/p3-mode`. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | The file from `/setup-p3` applies to new sessions. Start one. |
| A role's model was unavailable and the run stopped that step | `/p3-mode` never swaps a configured model on its own. Rerun `/setup-p3` to remap the role, or name a replacement. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Only `/setup-p3` loads from the user's words. The others load when the user types them or when `/p3-mode` runs them, and it doesn't run every skill. |
| Parallel agents overwrote each other | Give each delegate its own checkout with `delegate_task` and `isolation: "worktree"`, one writer per branch. |
| An overnight run moved but finished nothing | It needs a check that can pass or fail, not a duration. See the Autonomous run playbook. |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers, and [`references/recipes.md`](references/recipes.md) has the recipes worth copying.

## Make p3-stack my own

- [`/automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `/p3-mode`.
- [`/reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `/p3-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Edit skills in the astack checkout, then rerun `./install.sh` so every harness picks them up.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
