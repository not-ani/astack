# p3 model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` as a value: the role runs on the parent thread's model (omit the delegate_task model). Entries in a panel list still count toward its fan-out.
# Kita override: when the project's main checkout is under ~/kita/ (for a worktree, `git rev-parse --path-format=absolute --git-common-dir` resolves under ~/kita/), use providerInstanceId `codex_kita` everywhere a line below says `codex`. Same model and effort.
# Opus thinks and writes; Sol gathers evidence and checks. Fable only on hardest tasks.
# budget: medium (high)
feature, refactoring: claudeAgent/claude-opus-5-5 (high)
bug-fix: claudeAgent/claude-opus-5-5 (high)
perf-issue: claudeAgent/claude-opus-5-5 (high)
hillclimb: claudeAgent/claude-opus-5-5 (high)
judgment and prose: claudeAgent/claude-opus-5-5 (high)
hardest tasks: claudeAgent/claude-fable-5-1 (high)
how explorer: codex/gpt-6.1-sol (high)
how explainer: claudeAgent/claude-opus-5-5 (high)
why investigators: codex/gpt-6.1-sol (high)
why synthesizer: claudeAgent/claude-opus-5-5 (high)
reflect tooling: codex/gpt-6.1-sol (high)
reflect judgment, divergent, synthesizer: claudeAgent/claude-opus-5-5 (high)
arena runners: claudeAgent/claude-opus-5-5 (high), claudeAgent/claude-opus-5-5 (high)
arena cross-judge pool: codex/gpt-6.1-sol (high)
swarm workers: codex/gpt-6.1-sol (high)
architect runners: claudeAgent/claude-opus-5-5 (high), claudeAgent/claude-opus-5-5 (high)
interrogate reviewers: codex/gpt-6.1-sol (high), claudeAgent/claude-opus-5-5 (high)
