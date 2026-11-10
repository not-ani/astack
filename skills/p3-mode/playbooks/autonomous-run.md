### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Pick the wake mechanism by what you wait on. An event to watch (CI, a merge, a ref advancing) arms `watch_pull_request` and ends the turn. T3 wakes the thread when checks finish, a comment lands, or the branch conflicts. A delegate's result arrives through its `next`. A background command you started is awaited with `t3_background_wait`. External state T3 cannot report (a deploy, a remote queue) gets a `schedule_task` heartbeat (`{"type":"interval","everyMs":...}`) sized to when the result is worth re-checking, and so does a run with no event at all. Never use a scheduled task, a sleep, or polling to wait for a delegate or a PR. Pick each delegate's reasoning level and fast or standard speed for the job, per the Subagents section.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the **sequence-verifiable-units** principle skill, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries that support the goal are yours. Address broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself via p3-mode. Put out-of-band fixes in their own PR. Do not park reversible work for the human or ask a question you can settle yourself. Surface only irreversible actions, genuine product or preference calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration via the **show-me-your-work** skill, a row for what changed and whether the predicate moved.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory. Delete any heartbeat you scheduled with `delete_scheduled_task`, and unwatch every PR you watch.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
