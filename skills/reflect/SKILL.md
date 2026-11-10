---
name: reflect
description: Spawn three parallel review subagents over the active thread, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

The transcript is this T3 thread. Read it with `t3_thread_read`, and use `t3_thread_search` only to find this thread or pull exact passages from it. Don't read other threads. That crosses project boundaries and reads private chats from unrelated work.

Reviewers get only their brief, never this thread's context. Pass this thread's id and tell them to read it with `t3_thread_read`. If you don't have the id, or a reviewer can't call T3 tools, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One turn, three `delegate_task` calls with `mode: "async"`. Follow each delegate's `next` instead of polling. Reviewers keep their MCP tools to look up the tickets, chat threads, and observability traces the transcript references.

Each reviewer and the synthesizer name a role line in `p3-models.md` and a fallback. Resolve the line against `orchestrator_capabilities` and pass its provider and model. Use the fallback if the file or the line is missing, and say so. Leave `model` unset when the value is `auto` or `inherit-parent`. If a configured provider or model is unavailable or rejected, report the role unavailable. Use a fallback only when the caller or configuration explicitly authorizes it. Do not substitute another provider or model silently. Pick each subagent's reasoning effort, and speed where `orchestrator_capabilities` offers one, for the job, per the Subagents section of the **p3-mode** skill.

| Lens | Role line | Fallback | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | the `judgment and prose` line | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | a fast code model from another family than the judgment reviewer | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | the `judgment and prose` line | `references/divergent-reviewer.md` |

Pass each template verbatim as the brief, substituting the thread id or digest where marked. Reviewers return findings in their task result.

## 3. Synthesize

One `delegate_task` call, model from the `reflect judgment, divergent, synthesizer` line (fallback the `judgment and prose` line). It spot-verifies citations through MCP, so it keeps its tools. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting, when the user has authorized writes to that tracker. Otherwise list the items for the user to file. Only the Accepted list waits for approval.

Never edit a skill inside a plugin cache (such as `~/.claude/plugins/cache/`). Before approval, show its destination. An installed skill linked from a source checkout is edited at its source. A plugin skill goes to `.agents/skills/<skill>/` or `~/.agents/skills/<skill>/`. After approval, copy a plugin skill there and edit the copy. Never open a PR or push.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): follow the **p3-mode** skill's `authoring-a-skill` playbook and run a draft / test / iterate loop, with the `skill-creator` skill when the session lists it.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): follow the `authoring-a-skill` playbook and run a description-optimization loop, with `skill-creator` when the session lists it.
- `new skill via authoring-a-skill: <kebab-name>`: hand creation to the `authoring-a-skill` playbook. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
