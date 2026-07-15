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
        self.assertIn("new MutationObserver(window.siteShellSyncMenuState)", updated)
        self.assertNotIn("Old footer", updated)
        self.assertNotIn('onclick="siteShellToggleMenu(this)"', updated)

    def test_adds_compatible_shell_and_handler_to_redirect_stub(self):
        page = '<!doctype html><html><head></head><body class="flex"><main id="main-content">Redirect</main></body></html>'
        updated = shell.sync_source(page, "eps/index.html")
        self.assertIn("data-site-shell-added", updated)
        self.assertIn("data-site-shell-menu-state-script", updated)
        self.assertIn('onclick="siteShellToggleMenu(this)"', updated)
        self.assertIn("function siteShellToggleMenu(button)", updated)
        self.assertIn("Redirect</main>", updated)

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
