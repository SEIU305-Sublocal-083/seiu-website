import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScheduledNewsWorkflowTests(unittest.TestCase):
    def test_commit_step_does_not_stage_ignored_quality_report(self):
        workflow = (ROOT / ".github" / "workflows" / "publish-scheduled-news.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn("git add -A --", workflow)
        self.assertNotIn("site-quality-report.md", workflow)


if __name__ == "__main__":
    unittest.main()
