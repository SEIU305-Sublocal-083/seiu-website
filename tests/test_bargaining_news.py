import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "higher-ed-bargaining-updates.json"
UUID_PREFIX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}-"
)
ALLOWED_TAGS = {
    "Bargaining",
    "Update",
    "Contract",
    "Action",
    "Mediation",
    "Economics",
    "Rally",
    "Events",
    "2026 Bargaining",
}


class BargainingNewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.news = json.loads((ROOT / "news" / "news.json").read_text(encoding="utf-8"))

    def test_manifest_has_seventeen_complete_bilingual_updates(self):
        self.assertEqual(len(self.payload["updates"]), 17)
        for update in self.payload["updates"]:
            self.assertEqual(update["tags"][0], "Bargaining")
            self.assertIn("Update", update["tags"])
            self.assertIn("2026 Bargaining", update["tags"])
            self.assertTrue(set(update["tags"]).issubset(ALLOWED_TAGS))
            self.assertEqual(set(update["languages"]), {"en", "es"})
            for language, article in update["languages"].items():
                self.assertEqual(article["displayDate"], update["date"])
                self.assertTrue(article["title"])
                self.assertTrue(article["description"])
                self.assertTrue(article["bodyHtml"])
                self.assertTrue(article["url"].startswith("/news/es/" if language == "es" else "/news/"))

    def test_imported_images_are_local_uuid_prefixed_files(self):
        for update in self.payload["updates"]:
            for article in update["languages"].values():
                image_urls = [article["heroImage"], *re.findall(r'src="([^"]+)"', article["bodyHtml"])]
                for image_url in image_urls:
                    self.assertTrue(image_url.startswith("/images/"), image_url)
                    image_name = Path(image_url).name
                    self.assertRegex(image_name, UUID_PREFIX)
                    image_path = ROOT / image_url.lstrip("/")
                    self.assertTrue(image_path.is_file(), image_path)
                    thumbnail = image_path.with_name(f"{image_path.stem}-192{image_path.suffix}")
                    self.assertTrue(thumbnail.is_file(), thumbnail)

    def test_all_generated_pages_use_requested_byline_and_language_links(self):
        author = self.payload["author"]["name"]
        self.assertEqual(author, "SEIU 503 Higher Ed Bargaining Team")
        for update in self.payload["updates"]:
            for language, article in update["languages"].items():
                page = (ROOT / article["url"].lstrip("/")).read_text(encoding="utf-8")
                self.assertIn(f'<html lang="{language}"', page)
                self.assertIn(author, page)
                self.assertIn('hreflang="en"', page)
                self.assertIn('hreflang="es"', page)
                self.assertIn('hreflang="x-default"', page)
                self.assertIn("font-family: 'Inter', sans-serif", page)
                self.assertIn("font-family: 'Lora', serif", page)
                self.assertIn("color: var(--brand-purple-dark)", page)
                self.assertIn('<meta property="article:section" content="Bargaining">', page)
                for tag in update["tags"]:
                    self.assertIn(f'<meta property="article:tag" content="{tag}">', page)
                if language == "es":
                    self.assertIn('<meta property="article:tag" content="Español">', page)

    def test_all_thirty_four_pages_are_in_news_index(self):
        indexed = {item["url"]: item for item in self.news}
        imported_urls = []
        for update in self.payload["updates"]:
            for article in update["languages"].values():
                imported_urls.append(article["url"])
                self.assertIn(article["url"], indexed)
                self.assertEqual(indexed[article["url"]]["author"]["name"], self.payload["author"]["name"])
                expected_tags = update["tags"] + (["Español"] if article["url"].startswith("/news/es/") else [])
                self.assertEqual(indexed[article["url"]]["tags"], expected_tags)
        self.assertEqual(len(imported_urls), 34)
        self.assertEqual(len(set(imported_urls)), 34)

    def test_news_page_exposes_spanish_filter(self):
        news_page = (ROOT / "news.html").read_text(encoding="utf-8")
        self.assertIn('data-topic="Español"', news_page)


if __name__ == "__main__":
    unittest.main()
