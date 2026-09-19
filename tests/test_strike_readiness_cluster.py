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

    def test_every_page_connects_to_current_strike_status(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertRegex(source, r'href="/strike/?(?:#[^"]*)?"')
                self.assertNotIn("Sign the Higher Ed strike pledge.", source)

    def test_every_guide_has_sources_without_claiming_leadership_approval(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn('class="source-list"', source)
                self.assertNotRegex(source.lower(), r"leadership (?:review|approval).*?pending")
                self.assertNotIn("Reviewed by Local 083", source)

    def test_rights_guide_uses_notice_without_certifying_individual_rights(self):
        source = (ROOT / "resources" / "strike-rights-oregon.html").read_text(encoding="utf-8")
        self.assertIn("/news/2026-09-18-osu-strike-notice-delivered.html", source)
        self.assertIn("ORS 243.726", source)
        self.assertIn("ORS 243.672(3)", source)
        self.assertNotIn("Mediation — current stage", source)

    def test_unemployment_copy_distinguishes_two_unpaid_requirements(self):
        hub = (ROOT / "resources" / "strike-readiness.html").read_text(encoding="utf-8")
        benefits = (ROOT / "resources" / "strike-pay-benefits.html").read_text(encoding="utf-8")
        self.assertIn("the strike-specific unpaid week, a possible waiting week on a new claim", hub)
        self.assertIn("still working for the employer involved in the strike", benefits)

    def test_guides_show_editorial_review_and_prefilled_corrections_link(self):
        for filename in PAGES:
            source = (ROOT / "resources" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertNotIn("Reviewed by Local 083", source)
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
        self.assertIn("overflow-x: auto", stylesheet)
        self.assertIn("justify-content: space-between", stylesheet)
        self.assertIn("top: 4.0625rem", stylesheet)
        self.assertNotIn("top: 4.5rem", stylesheet)

    def test_county_lookup_maps_all_36_oregon_counties_to_local_providers(self):
        script = (ROOT / "js" / "strike-county-lookup.js").read_text(encoding="utf-8")
        agency_match = re.search(r"const agencies = \{(.*?)\n  \};", script, flags=re.S)
        county_match = re.search(r"const countyAgencies = \{(.*?)\n  \};", script, flags=re.S)
        self.assertIsNotNone(agency_match)
        self.assertIsNotNone(county_match)

        agency_keys = set(re.findall(r"^    ([A-Za-z]+): \{", agency_match.group(1), flags=re.M))
        county_entries = re.findall(
            r"^    (?:'([^']+)'|([A-Za-z]+)): '([A-Za-z]+)',",
            county_match.group(1),
            flags=re.M,
        )
        county_names = {quoted or bare for quoted, bare, _ in county_entries}
        assigned_agencies = {agency for _, _, agency in county_entries}
        self.assertEqual(len(county_names), 36)
        self.assertEqual(
            county_names,
            {
                "Baker", "Benton", "Clackamas", "Clatsop", "Columbia", "Coos",
                "Crook", "Curry", "Deschutes", "Douglas", "Gilliam", "Grant",
                "Harney", "Hood River", "Jackson", "Jefferson", "Josephine",
                "Klamath", "Lake", "Lane", "Lincoln", "Linn", "Malheur",
                "Marion", "Morrow", "Multnomah", "Polk", "Sherman", "Tillamook",
                "Umatilla", "Union", "Wallowa", "Wasco", "Washington", "Wheeler",
                "Yamhill",
            },
        )
        self.assertTrue(assigned_agencies.issubset(agency_keys))

        support = (ROOT / "resources" / "strike-support.html").read_text(encoding="utf-8")
        self.assertIn('id="county-agency-name"', support)
        self.assertIn('id="county-agency-phone"', support)
        self.assertIn('id="county-agency-link"', support)
        self.assertIn("https://www.caporegon.org/find-help", support)
        self.assertNotIn("https://www.caporegon.org/find-services/", support)

    def test_tax_correction_and_benefit_limits_are_easy_to_find(self):
        for relative in ["strike/index.html", "resources/strike-readiness.html",
                         "resources/strike-pay-benefits.html"]:
            source = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative):
                self.assertIn("Strike pay is taxable income", source)
                self.assertIn("$400", source)
                self.assertIn("https://www.irs.gov/publications/p525", source)
        benefits = (ROOT / "resources/strike-pay-benefits.html").read_text(encoding="utf-8")
        self.assertIn("not an automatic payment", benefits)
        self.assertIn("A payable week is not a promised deposit date", benefits)

    def test_sources_have_resolving_unique_fragment_targets(self):
        paths = [ROOT / "resources" / name for name in PAGES]
        paths += [ROOT / "strike/index.html"]
        for path in paths:
            source = path.read_text(encoding="utf-8")
            ids = re.findall(r'\bid="([^"]+)"', source)
            refs = re.findall(r'href="#([^"]+)"', source)
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual(len(ids), len(set(ids)), "Duplicate fragment targets")
                self.assertTrue(set(refs).issubset(ids), set(refs) - set(ids))

    def test_resource_library_lists_cluster(self):
        source = (ROOT / "resources.html").read_text(encoding="utf-8")
        for filename in PAGES:
            with self.subTest(filename=filename):
                self.assertIn(f"/resources/{filename}", source)
        self.assertIn('data-category="strike"', source)


if __name__ == "__main__":
    unittest.main()
