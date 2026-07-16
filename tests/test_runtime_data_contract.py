import json
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

    def test_current_email_action_copies_osu_trustees(self):
        payload = json.loads(self.source("data/current-action.json"))
        email_action = payload["emailActions"]["osu-president"]

        self.assertEqual(email_action["recipient"], "pres.office@oregonstate.edu")
        self.assertEqual(email_action["cc"], "trustees@oregonstate.edu")
        self.assertIn("Members of the OSU Board of Trustees", email_action["body"])
        self.assertIn("cc=${encodeURIComponent(cc)}", self.source("js/current-action.js"))

        fallback_pages = (
            "index.html",
            "action/index.html",
            "2026-bargaining/index.html",
            "news/2026-07-09-latest-bargaining-update.html",
            "news/2026-07-09-tell-universities-hell-no.html",
        )
        fallback_href = "mailto:pres.office@oregonstate.edu?cc=trustees@oregonstate.edu"
        for page in fallback_pages:
            with self.subTest(page=page):
                self.assertIn(fallback_href, self.source(page))


if __name__ == "__main__":
    unittest.main()
