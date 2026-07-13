import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_rss as rss  # noqa: E402


class RssDeterminismTests(unittest.TestCase):
    def test_scheduled_story_is_not_public_even_when_date_is_due(self):
        article = {"status": "scheduled", "publishedAt": "2020-01-01"}
        self.assertFalse(rss.is_public_news_article(article, datetime(2030, 1, 1, tzinfo=timezone.utc)))

    def test_last_build_date_comes_from_content(self):
        date = datetime(2026, 7, 10, tzinfo=timezone.utc)
        feed = rss.build_feed(
            title="Test",
            description="Test feed",
            self_path="/feed.xml",
            items=[{
                "title": "Story",
                "link": "https://www.local083.org/story",
                "description": "Description",
                "pub_date": date,
                "guid": "story",
                "guid_is_permalink": False,
            }],
        )
        channel = feed.find("channel")
        self.assertIsNotNone(channel)
        self.assertEqual(channel.findtext("lastBuildDate"), rss.to_rfc2822(date))

    def test_event_entries_uses_versioned_events_payload(self):
        events = [{"title": "Meeting"}]
        self.assertIs(rss.event_entries({"asOf": "2026-07-12", "events": events}), events)
        with self.assertRaises(ValueError):
            rss.event_entries(events)


if __name__ == "__main__":
    unittest.main()
