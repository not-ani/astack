import tempfile
import unittest
from pathlib import Path

from check_skills import check


class SkillValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills" / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("---\nname: example\ndescription: Example skill.\n---\n\n# Example\n")

    def append(self, text):
        self.skill.write_text(self.skill.read_text() + text)

    def test_valid_skill(self):
        self.assertEqual(check(self.root), [])

    def test_missing_bundled_reference_fails(self):
        self.append("Read [the guide](references/guide.md).\n")
        self.assertTrue(any("missing link references/guide.md" in error for error in check(self.root)))
        guide = self.skill.parent / "references" / "guide.md"
        guide.parent.mkdir()
        guide.write_text("# Guide\n")
        self.assertEqual(check(self.root), [])

    def test_old_completion_polling_fails(self):
        self.append("Drain with `task_status`.\n")
        self.assertTrue(any("follow the delegate's next instruction" in error for error in check(self.root)))

    def test_cursor_agent_arguments_fail(self):
        self.append('Spawn with `subagent_type: "poteto-agent"`.\n')
        self.assertTrue(any("use native delegation or delegate_task" in error for error in check(self.root)))

    def test_frontmatter_name_must_match_directory(self):
        self.skill.write_text("---\nname: wrong\ndescription: Example skill.\n---\n")
        self.assertTrue(any("name must match its directory" in error for error in check(self.root)))

    def test_cursor_replacement_cannot_remove_t3_router_wiring(self):
        router = self.root / "skills" / "p3-mode" / "SKILL.md"
        router.parent.mkdir()
        router.write_text("---\nname: p3-mode\ndescription: Agent workflow.\n---\nSpawn a Task worker.\n")
        self.assertTrue(any("preserve the T3 mechanism delegate_task" in error for error in check(self.root)))
        router.write_text(router.read_text() + "Use delegate_task, orchestrator_capabilities, and p3-models.md.\n")
        self.assertEqual(check(self.root), [])

    def test_unrelated_negation_does_not_hide_forbidden_calls(self):
        self.append("Poll `task_status` until the child is not running.\n")
        self.append("Launch workers with t3_thread_launch and workspaceStrategy.\n")
        self.append("Use `gh pr checks --watch` instead of waiting.\n")
        errors = check(self.root)
        self.assertTrue(any("follow the delegate's next instruction" in error for error in errors))
        self.assertTrue(any("top-level thread" in error for error in errors))
        self.assertTrue(any("use watch_pull_request" in error for error in errors))

    def test_prohibition_does_not_hide_a_later_positive_instruction(self):
        self.append("Never poll `task_status`. Use `task_status` until done.\n")
        self.assertTrue(any("follow the delegate's next instruction" in error for error in check(self.root)))

    def test_direct_prohibitions_and_requested_top_level_threads_are_allowed(self):
        self.append("Never poll with `task_status` or `gh pr checks --watch`.\n")
        self.append("`t3_thread_launch` creates top-level threads. Use it only when the user asks for a new thread.\n")
        self.assertEqual(check(self.root), [])


if __name__ == "__main__":
    unittest.main()
