import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "strike-readiness.html",
    "strike-rights-oregon.html",
    "strike-pay-benefits.html",
    "strike-support.html",
    "why-workers-strike.html",
    "strike-history.html",
    "strike-sourcing-policy.html",
)


class StrikeReadinessClusterTests(unittest.TestCase):
    def test_pages_have_unique_h1_and_self_canonical(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertEqual(len(re.findall(r"<h1\b", source, flags=re.I)), 1)
                self.assertIn(
                    f'<link rel="canonical" href="https://www.local083.org/resources/{filename}">',
                    source,
                )

    def test_every_page_cross_links_to_cluster(self):
        expected = [f"/resources/{filename}" for filename in PAGES]
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                for path in expected:
                    self.assertIn(path, source)

    def test_every_page_connects_readiness_to_current_pledge(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn('href="/pledge"', source)
                self.assertIn("not a strike-authorization vote", source)

    def test_high_stakes_pages_show_review_date_and_sources(self):
        for filename in ("strike-rights-oregon.html", "strike-pay-benefits.html", "strike-support.html"):
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn("July 20, 2026", source)
                self.assertIn('class="source-list"', source)

    def test_rights_guide_accounts_for_current_contract_extension(self):
        source = (ROOT / "resources" / "strike-rights-oregon.html").read_text(encoding="utf-8")
        self.assertIn("extended the current agreement through Aug. 31, 2026", source)
        self.assertIn("Treat the no-strike clause as continuing during the reported extension", source)
        self.assertIn("https://seiu503.org/get-involved/bargaining/higher-ed-bargaining-2026/", source)

        layoff = (ROOT / "resources" / "layoff-workflow.html").read_text(encoding="utf-8")
        self.assertIn("extended through August 31, 2026", layoff)
        self.assertNotIn("agreement expired June 30, 2026", layoff)
        self.assertIn("https://seiu503.org/get-involved/bargaining/higher-ed-bargaining-2026/", layoff)

    def test_unemployment_copy_distinguishes_two_unpaid_requirements(self):
        hub = (ROOT / "resources" / "strike-readiness.html").read_text(encoding="utf-8")
        benefits = (ROOT / "resources" / "strike-pay-benefits.html").read_text(encoding="utf-8")
        self.assertIn("the strike-specific unpaid week, a possible waiting week on a new claim", hub)
        self.assertIn("still working for the employer involved in the strike", benefits)

    def test_guides_show_editorial_review_and_prefilled_corrections_link(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn("Reviewed by Local 083", source)
                self.assertIn("083execteam@seiu503.org?subject=Correction%20to%20Local%20083", source)
                self.assertIn("What%20needs%20correction%3A", source)
                self.assertIn(">Send a correction<", source)

    def test_pages_follow_brand_metadata_requirements(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                title = re.search(r"<title>(.*?)</title>", source, flags=re.S | re.I)
                description = re.search(
                    r'<meta name="description" content="([^"]+)">', source, flags=re.I
                )
                self.assertIsNotNone(title)
                self.assertTrue(title.group(1).endswith(" - SEIU Local 503, OSU"))
                self.assertIsNotNone(description)
                self.assertGreaterEqual(len(description.group(1)), 130)
                self.assertLessEqual(len(description.group(1)), 165)
                for field in (
                    "og:type",
                    "og:url",
                    "og:title",
                    "og:description",
                    "og:image",
                    "og:site_name",
                    "twitter:card",
                    "twitter:url",
                    "twitter:title",
                    "twitter:description",
                    "twitter:image",
                ):
                    self.assertIn(f'content=', source[source.find(field):source.find(field) + 300])

    def test_pages_publish_organization_website_and_webpage_schema(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                match = re.search(
                    r'<script type="application/ld\+json">(.*?)</script>',
                    source,
                    flags=re.S | re.I,
                )
                self.assertIsNotNone(match)
                data = json.loads(match.group(1))
                graph_types = {item.get("@type") for item in data.get("@graph", [])}
                self.assertTrue({"Organization", "WebSite", "WebPage"}.issubset(graph_types))

    def test_member_copy_uses_our_union_voice(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            main = re.search(r"<main\b.*?</main>", source, flags=re.S | re.I).group(0)
            visible = re.sub(r"<[^>]+>", " ", main)
            with self.subTest(filename=filename):
                self.assertNotRegex(visible.lower(), r"\bthe union(?:'s|’s)?\b")

        hub = (ROOT / "resources" / "strike-readiness.html").read_text(encoding="utf-8")
        self.assertIn("Start the readiness checklist", hub)
        self.assertIn("View our bargaining updates", hub)
        self.assertIn("Email our stewards", hub)

    def test_strike_pages_use_canonical_site_typography_and_palette(self):
        stylesheet = (ROOT / "styles" / "strike-readiness.css").read_text(encoding="utf-8")
        self.assertIn('font-family: "Inter", sans-serif', stylesheet)
        self.assertIn('font-family: "Lora", serif', stylesheet)
        self.assertIn("--brand-purple-dark: #4c1d95", stylesheet)
        self.assertNotIn("#2e1065", stylesheet)

    def test_strike_layout_matches_modern_resource_page_conventions(self):
        stylesheet = (ROOT / "styles" / "strike-readiness.css").read_text(encoding="utf-8")
        self.assertIn("max-width: 74rem", stylesheet)
        self.assertIn("3.75rem", stylesheet)
        self.assertIn("border-bottom-color: var(--brand-purple)", stylesheet)
        self.assertNotIn('border-radius: 999px; color: #4b5563', stylesheet)
        self.assertNotIn("border-top: 4px solid #c4b5fd", stylesheet)
        self.assertIn("border-left: 4px solid var(--brand-purple)", stylesheet)

    def test_county_lookup_contains_all_36_oregon_counties(self):
        script = (ROOT / "js" / "strike-county-lookup.js").read_text(encoding="utf-8")
        match = re.search(r"const counties = \[(.*?)\];", script, flags=re.S)
        self.assertIsNotNone(match)
        self.assertEqual(len(re.findall(r"'[A-Za-z ]+'", match.group(1))), 36)

    def test_resource_library_lists_cluster(self):
        source = (ROOT / "resources.html").read_text(encoding="utf-8")
        for filename in PAGES:
            with self.subTest(filename=filename):
                self.assertIn(f"/resources/{filename}", source)
        self.assertIn('data-category="strike"', source)


if __name__ == "__main__":
    unittest.main()
