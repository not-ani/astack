---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use the `arena runners` line in `p3-models.md`, resolved against `orchestrator_capabilities`. If the file or that line is missing, run `setup-p3`, or default to one runner each on two different model families that `orchestrator_capabilities` lists, and say so. Families go by model maker (`claude-*`, `gpt-*`, and so on), whichever provider instance serves the model. An `auto` or `inherit-parent` entry in this line means the parent model, so omit `model` for it. If a configured provider or model is unavailable or rejected, report that seat unavailable. Use a replacement only when the caller or configuration explicitly authorizes it. Refill a dropped seat only with a model already allowed by the runner pool. Report any requested coverage that cannot run; do not silently substitute a provider, model, or native-tool fallback. Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive. Pick each subagent's reasoning effort, and speed where `orchestrator_capabilities` offers one, for the job, per the Subagents section of the **p3-mode** skill.
4. Give each candidate its own output location (its own worktree through `delegate_task` with `isolation: "worktree"` where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill. A new worktree starts from the parent commit without uncommitted edits, so point candidates at the grounding by absolute path.

## Phase B: Fan out

Spawn all N candidates in one turn, one `delegate_task` per runner with `mode: "async"`, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected. A child gets only its brief, never this thread, so every brief stands alone. Follow each delegate's `next` until all are terminal. Don't poll.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one model from the `arena cross-judge pool` line in `p3-models.md`. If the file or that line is missing, choose from the models `orchestrator_capabilities` lists. Spawn one judge with `delegate_task`, and say in its brief that it is read-only: inspect only, no writes. The judge is never from the parent's family, as Phase A step 3 defines families. Try only the entries from another family, in pool order. An `auto` or `inherit-parent` entry is the parent model, so it never judges. If a pool entry is unavailable or rejected, report it and move only to another explicitly allowed pool entry. Do not substitute an unlisted provider or model. If no allowed entry from another family runs, skip the judge, pick the base alone in Phase D, and report the missing independent judgment. If you do not know the parent's model, try the pool's entries in pool order and say that the family check did not run. The judge sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
