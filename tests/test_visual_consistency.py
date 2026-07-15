import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PRIMARY_HEADING_PAGES = (
    "contact.html",
    "leadership.html",
    "news.html",
    "resources.html",
)
REQUIRED_HEADING_CLASSES = {
    "text-4xl",
    "md:text-6xl",
    "font-bold",
    "leading-[1.04]",
    "tracking-tight",
}


class VisualConsistencyTests(unittest.TestCase):
    def test_legacy_primary_pages_use_canonical_heading_treatment(self):
        for relative_path in PRIMARY_HEADING_PAGES:
            with self.subTest(page=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                match = re.search(r'<h1\s+class="([^"]+)"', source)
                self.assertIsNotNone(match)
                classes = set(match.group(1).split())
                self.assertTrue(REQUIRED_HEADING_CLASSES <= classes)


if __name__ == "__main__":
    unittest.main()
