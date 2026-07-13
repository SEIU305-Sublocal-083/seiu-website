import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import shell_consistency_audit as shell  # noqa: E402


CANONICAL_PAGE = '''<!doctype html><html><body>
<header><nav aria-label="Primary navigation"><a href="/">SEIU 503</a>
<a href="/about.html">About</a><a href="/events.html">Events</a><a href="/news.html">News</a>
<a href="/resources.html">Resources &amp; Rights</a><a href="/leadership.html">Leadership</a><a href="/contact.html">Contact</a>
</nav></header><main><h1>Page</h1></main>
<footer><p>SEIU Local 503 — Oregon State University</p>
<a href="/resources.html">Resources &amp; Rights</a><a href="/contact.html">Contact us</a>
<a href="mailto:083execteam@seiu503.org">Executive</a><a href="mailto:083stewards@seiu503.org">Stewards</a>
<a href="/privacy.html#analytics-controls">Tracking settings</a><a href="/privacy.html">Privacy notice</a></footer>
<script data-site-shell-menu-state-script></script>
</body></html>'''


class ShellAuditTests(unittest.TestCase):
    def test_accepts_canonical_shell(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "index.html"
            page.write_text(CANONICAL_PAGE, encoding="utf-8")
            self.assertEqual(shell.audit_page(page, root), [])

    def test_reports_nav_order_and_missing_footer_parts(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "index.html"
            page.write_text('<header><nav aria-label="Primary navigation"><a href="/news.html">News</a></nav></header><footer>SEIU Local 503</footer>', encoding="utf-8")
            messages = [finding.message for finding in shell.audit_page(page, root)]
            self.assertTrue(any("navigation differs" in message for message in messages))
            self.assertTrue(any("Privacy notice" in message for message in messages))
            self.assertTrue(any("Tracking settings" in message for message in messages))
            self.assertTrue(any("mobile-menu state script" in message for message in messages))

    def test_reports_duplicate_mobile_menu_state_script(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "index.html"
            page.write_text(
                CANONICAL_PAGE.replace(
                    "</body>",
                    "<script data-site-shell-menu-state-script></script></body>",
                ),
                encoding="utf-8",
            )
            messages = [finding.message for finding in shell.audit_page(page, root)]
            self.assertEqual(
                [message for message in messages if "mobile-menu state script" in message],
                ["Expected exactly one canonical mobile-menu state script; found 2"],
            )


if __name__ == "__main__":
    unittest.main()
