import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import site_quality_check as sq  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
