import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESOURCE_PATH = ROOT / "resources" / "code-of-conduct.html"
ALIASES = ("COC", "Conduct", "Code-of-Conduct")


class CodeOfConductTests(unittest.TestCase):
    def test_resource_page_contains_complete_policy_structure_and_source(self):
        source = RESOURCE_PATH.read_text(encoding="utf-8")

        self.assertIn("Code of Conduct for Events, Meetings and Communications", source)
        self.assertIn("Prohibited conduct includes, but is not limited to:", source)
        self.assertEqual(source.count('class="flex gap-4"'), 10)
        self.assertIn("March 9, 2019", source)
        self.assertIn("September 2, 2020", source)
        self.assertIn(
            "https://seiu503.org/wp-content/uploads/2020/11/Code-of-Conduct-for-SEIU-503-Events_Meetings_Communications.pdf",
            source,
        )

    def test_resource_library_indexes_page(self):
        source = (ROOT / "resources.html").read_text(encoding="utf-8")

        self.assertIn('href="/resources/code-of-conduct.html"', source)
        self.assertIn("SEIU 503 Code of Conduct", source)
        self.assertIn("Showing 19 resources", source)

    def test_all_requested_short_urls_target_resource_page(self):
        entries = json.loads((ROOT / "data" / "short-urls.json").read_text(encoding="utf-8"))
        by_slug = {entry["slug"]: entry for entry in entries}

        for alias in ALIASES:
            with self.subTest(alias=alias):
                self.assertEqual(
                    by_slug[alias]["target"],
                    "/resources/code-of-conduct.html",
                )
                redirect = ROOT / alias / "index.html"
                self.assertTrue(redirect.is_file())
                self.assertIn(
                    'content="0; url=/resources/code-of-conduct.html"',
                    redirect.read_text(encoding="utf-8"),
                )

    def test_resource_page_is_in_sitemap_but_aliases_are_not(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")

        self.assertIn(
            "https://www.local083.org/resources/code-of-conduct.html",
            sitemap,
        )
        for alias in ALIASES:
            self.assertNotIn(f"https://www.local083.org/{alias}/", sitemap)


if __name__ == "__main__":
    unittest.main()
