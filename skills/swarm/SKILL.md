---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Pick the worker model from the `swarm workers` line in `p3-models.md`, resolved against `orchestrator_capabilities`. If the file or that line is missing, run `setup-p3`, or use a fast code model that `orchestrator_capabilities` lists and say so. For `auto` or `inherit-parent`, omit `model` so the workers run on the parent model. If a configured provider or model is unavailable or rejected, report the affected workers unavailable. Use a replacement only when the caller or configuration explicitly authorizes it. Do not substitute the parent model or another provider silently. For a model race, name each arm's model up front. Pick each subagent's reasoning effort, and speed where `orchestrator_capabilities` offers one, for the job, per the Subagents section of the **p3-mode** skill.
4. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one turn, one `delegate_task` each with `mode: "async"`, `isolation: "worktree"`, and the step 3 model, left unset for `auto` or `inherit-parent`. Use `isolation: "shared"` only when the worker needs the parent checkout itself, such as its uncommitted edits or a process running there. Follow each delegate's `next` until all are terminal. Don't poll.

When a worker needs a non-default pushed branch, name the desired starting revision as an input. T3 creates the checkout first through `isolation: "worktree"`; the worker may select that revision only inside its prepared checkout. Never ask the worker to create a checkout.

Every brief stands alone, because a child gets only its brief. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with a result table, issue one-liners, gaps or dropouts, and the race rule when used.
