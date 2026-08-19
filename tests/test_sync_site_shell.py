import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_site_shell as shell  # noqa: E402


PAGE = '''<!doctype html><html><head><style>body { color: black; }</style></head><body>
<a href="#main-content">Skip</a>
<header class="old"><nav>Old</nav></header>
<main id="main-content"><article><header><h1>Article title</h1></header><p>Body copy</p></article></main>
<footer class="old">Old footer</footer>
<script>const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');
mobileMenuButton.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));</script>
</body></html>'''


class SyncSiteShellTests(unittest.TestCase):
    def test_top_level_section_pages_select_their_navigation_category(self):
        for path, expected in (
            ("events.html", "events"),
            ("news.html", "news"),
            ("resources.html", "resources"),
        ):
            with self.subTest(path=path):
                self.assertEqual(shell.active_section(path), expected)

    def test_shell_styles_define_canonical_tokens_and_ui_font(self):
        styles = (ROOT / "styles" / "site-shell.css").read_text(encoding="utf-8")
        self.assertIn("[data-site-shell-header]", styles)
        self.assertIn("[data-site-shell-footer]", styles)
        self.assertIn("--brand-purple: #7c3aed", styles)
        self.assertIn("--text-secondary: #374151", styles)
        self.assertIn("font-family: 'Inter'", styles)
        self.assertIn(
            '[data-site-shell-header] > nav[aria-label="Primary navigation"]',
            styles,
        )
        self.assertIn("max-width: 80rem", styles)

    def test_replaces_shell_but_preserves_article_header_and_body(self):
        updated = shell.sync_source(PAGE, "news/story.html")
        self.assertIn('<link rel="stylesheet" href="/styles/tailwind.css">', updated)
        self.assertIn('<link rel="stylesheet" href="/styles/site-shell.css">', updated)
        self.assertIn('<a href="/news.html" class="text-brand-purple font-bold" aria-current="page">News</a>', updated)
        self.assertIn(
            '<a href="/news.html" class="block text-center py-3 px-6 text-lg text-brand-purple bg-brand-purple-light font-bold" aria-current="page">News</a>',
            updated,
        )
        self.assertIn("<article><header><h1>Article title</h1></header><p>Body copy</p></article>", updated)
        self.assertIn('href="/privacy.html#analytics-controls">Tracking settings</a>', updated)
        self.assertIn("data-site-shell-menu-state-script", updated)
        self.assertIn("event.stopImmediatePropagation()", updated)
        self.assertIn("{ capture: true }", updated)
        self.assertIn("data-site-shell-menu-owner", updated)
        self.assertNotIn("Old footer", updated)
        self.assertNotIn('onclick="siteShellToggleMenu(this)"', updated)

    def test_adds_canonical_shell_and_handler_to_redirect_stub(self):
        page = '<!doctype html><html><head></head><body class="flex"><main id="main-content">Redirect</main></body></html>'
        updated = shell.sync_source(page, "eps/index.html")
        self.assertIn("data-site-shell-added", updated)
        self.assertIn("data-site-shell-menu-state-script", updated)
        self.assertIn("data-site-shell-menu-owner", updated)
        self.assertIn("button.addEventListener('click'", updated)
        self.assertIn("Redirect</main>", updated)

    def test_wordmark_uses_scoped_canonical_brand_color(self):
        updated = shell.sync_source(PAGE, "about.html")
        self.assertIn(
            '<span class="site-wordmark text-2xl font-bold text-brand-purple-dark">SEIU 503</span>',
            updated,
        )
        styles = (ROOT / "styles" / "site-shell.css").read_text(encoding="utf-8")
        self.assertIn("[data-site-shell-header] .site-wordmark", styles)
        self.assertIn("color: var(--brand-purple-dark) !important", styles)

    def test_is_idempotent(self):
        once = shell.sync_source(PAGE, "about.html")
        twice = shell.sync_source(once, "about.html")
        self.assertEqual(once, twice)

    def test_cleans_indentation_only_line_before_inserted_shell(self):
        page = '<!doctype html><html><head></head><body>\n    \n<main>Redirect</main></body></html>'
        updated = shell.sync_source(page, "rally/index.html")
        self.assertNotIn("\n    \n    <!-- SITE SHELL", updated)


if __name__ == "__main__":
    unittest.main()
