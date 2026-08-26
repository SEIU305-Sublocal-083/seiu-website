import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESOURCE_PATH = ROOT / "resources" / "code-of-conduct.html"
ALIASES = ("COC", "Conduct", "Code-of-Conduct")


class CodeOfConductTests(unittest.TestCase):
    def test_resource_page_contains_complete_policy_structure_and_source(self):
        source = RESOURCE_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "Code of Conduct for SEIU 503 Events/Meetings/Communications",
            source.replace("<wbr>", ""),
        )
        self.assertIn(
            "There is a prohibition against harassment and other exclusionary behavior. "
            "This includes, but is not limited to:",
            source,
        )
        self.assertEqual(source.count('class="flex gap-4"'), 10)
        policy_items = (
            "Violent threats or language, signs, symbols, or images directed against another person",
            "Discriminatory jokes and language, signs, symbols, or images",
            "Ableist jokes and language, signs, symbols, or images",
            "Sexually explicit or violent behavior and language, signs, symbols, or images",
            "Offensive comments, signs, symbols, or images related to gender, gender identity and expression, "
            "sexual orientation, disability, mental illness, neurotype, physical appearance, body, age, race, "
            "ethnicity, nationality, language, family status, economic status, immigration status, or religion",
            "Unwelcome sexual attention",
            "Advocating for or encouraging any of the above behavior",
            "Repeated harassment of others",
            "Deliberate intimidation",
            "Deliberate misgendering or use rejected names to describe groups of people",
        )
        for item in policy_items:
            with self.subTest(item=item):
                self.assertIn(item, source)
        self.assertIn("originally adopted by the Board of Directors on 3/9/2019", source)
        self.assertIn("amended on 9/2/2020", source)
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
