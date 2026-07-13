import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_site  # noqa: E402


class BuildSiteDriftTests(unittest.TestCase):
    def test_check_detects_drift_and_restores_original_file(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            generated = root / "index.html"
            generated.write_text("before", encoding="utf-8")

            def fake_run(command: list[str]) -> None:
                if command[-1] == "scripts/generate_static_content.py":
                    generated.write_text("after", encoding="utf-8")

            with (
                patch.object(build_site, "ROOT", root),
                patch.object(build_site, "GENERATED_PATHS", ["index.html"]),
                patch.object(build_site, "run", fake_run),
                patch.object(sys, "argv", ["build_site.py", "--check", "--skip-css"]),
            ):
                self.assertEqual(build_site.main(), 1)

            self.assertEqual(generated.read_text(encoding="utf-8"), "before")

    def test_check_succeeds_when_rebuild_is_stable(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text("stable", encoding="utf-8")
            with (
                patch.object(build_site, "ROOT", root),
                patch.object(build_site, "GENERATED_PATHS", ["index.html"]),
                patch.object(build_site, "run", lambda command: None),
                patch.object(sys, "argv", ["build_site.py", "--check", "--skip-css"]),
            ):
                self.assertEqual(build_site.main(), 0)


if __name__ == "__main__":
    unittest.main()
