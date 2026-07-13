import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class RuntimeDataContractTests(unittest.TestCase):
    def source(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_every_browser_news_feed_requires_published_status(self):
        index = self.source("index.html")
        newsroom = self.source("news.html")
        legacy_feed = self.source("js/news.js")

        self.assertIn("(item.status || 'published') === 'published'", index)
        self.assertIn("if (status !== 'published') return false;", newsroom)
        self.assertIn("if (status !== 'published') return false;", legacy_feed)

    def test_browser_event_feeds_accept_versioned_payload(self):
        index = self.source("index.html")
        calendar = self.source("events.html")

        self.assertIn("eventsPayload.events", index)
        self.assertIn("payload.events", calendar)
        self.assertIn("Array.isArray(events)", index)
        self.assertIn("Array.isArray(events)", calendar)


if __name__ == "__main__":
    unittest.main()
