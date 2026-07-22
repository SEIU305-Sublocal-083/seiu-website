import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_short_redirects as redirects  # noqa: E402


class ShortRedirectTests(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads((ROOT / "data" / "short-urls.json").read_text(encoding="utf-8"))
        self.by_slug = {entry["slug"]: entry for entry in self.entries}

    def test_required_and_high_value_short_urls_are_declared(self):
        self.assertEqual(self.by_slug["actions"]["target"], "/action/")
        self.assertEqual(
            self.by_slug["pledge"]["target"],
            "https://canvasser-7217.my.site.com/survey/s/surveyvista?su=NaJMuv",
        )
        self.assertEqual(self.by_slug["strikeprep"]["target"], "/resources/strike-readiness.html")
        self.assertEqual(self.by_slug["strikepay"]["target"], "/resources/strike-pay-benefits.html")
        self.assertEqual(self.by_slug["strikehelp"]["target"], "/resources/strike-support.html")

    def test_generated_redirects_are_noindex_canonical_and_accessible(self):
        for entry in self.entries:
            with self.subTest(slug=entry["slug"]):
                source = redirects.render_redirect(entry)
                self.assertIn('<meta name="robots" content="noindex, follow">', source)
                self.assertIn(f'<meta http-equiv="refresh" content="0; url={entry["target"]}">', source)
                self.assertIn(f'href="{entry["target"]}"', source)
                self.assertIn("data-site-shell-header", source)
                self.assertIn("data-site-shell-footer", source)
                self.assertIn('class="text-2xl font-bold text-brand-purple-dark">SEIU 503</span>', source)

    def test_internal_redirect_targets_exist(self):
        for entry in self.entries:
            target = entry["target"]
            if not target.startswith("/"):
                continue
            with self.subTest(slug=entry["slug"]):
                path = ROOT / target.lstrip("/")
                if target.endswith("/"):
                    path /= "index.html"
                self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
