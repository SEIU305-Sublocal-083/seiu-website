import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import site_quality_check as sq  # noqa: E402
import public_pages as pp  # noqa: E402


class PathExistsTests(unittest.TestCase):
    def test_directory_only_path_is_not_treated_as_valid_page(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "events").mkdir()

            self.assertFalse(sq.path_exists(base / "events"))

    def test_html_file_without_extension_is_resolved(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "about.html").write_text("<html></html>", encoding="utf-8")

            self.assertTrue(sq.path_exists(base / "about"))


class HtmlLinkTests(unittest.TestCase):
    def test_flags_active_hash_only_links_but_not_commented_markup(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "example.html"
            page.write_text(
                '<a href="#">Broken</a><!-- <a href="#">Ignored</a> -->',
                encoding="utf-8",
            )
            original_root = sq.ROOT
            try:
                sq.ROOT = root
                issues = sq.check_html_links([page])
            finally:
                sq.ROOT = original_root

            self.assertEqual(len(issues), 1)
            self.assertIn("placeholder link", issues[0].message)


class PublicPageDiscoveryTests(unittest.TestCase):
    def test_discovers_nested_public_sections_and_excludes_drafts(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text('<link rel="canonical" href="https://www.local083.org/">', encoding="utf-8")
            (root / "action").mkdir()
            (root / "action" / "index.html").write_text("<html></html>", encoding="utf-8")
            (root / "test-pages").mkdir()
            (root / "test-pages" / "draft.html").write_text("<html></html>", encoding="utf-8")
            (root / "scheduled.html").write_text('<meta name="robots" content="noindex">', encoding="utf-8")

            pages = pp.discover_public_pages(root)
            rels = {page.path.relative_to(root).as_posix() for page in pages}

            self.assertEqual(rels, {"action/index.html", "index.html", "scheduled.html"})
            self.assertEqual(pp.sitemap_urls(root), [
                "https://www.local083.org/",
                "https://www.local083.org/action/",
            ])

    def test_404_is_audited_but_not_sitemapped(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "404.html").write_text("<html></html>", encoding="utf-8")

            self.assertEqual(pp.public_html_paths(root), [root / "404.html"])
            self.assertEqual(pp.sitemap_urls(root), [])


if __name__ == "__main__":
    unittest.main()
