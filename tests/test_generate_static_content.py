import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_static_content as static  # noqa: E402


def graph() -> str:
    return '<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"ItemList"}]}</script>'


class StaticContentTests(unittest.TestCase):
    def test_element_replacement_handles_nested_same_name_tags(self):
        source = '<div id="target"><div>old</div></div><div>after</div>'
        self.assertEqual(
            static.replace_element_inner(source, "target", "  <p>new</p>"),
            '<div id="target">\n  <p>new</p>\n</div><div>after</div>',
        )

    def test_build_is_repeatable_and_excludes_scheduled_news(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "news").mkdir()
            (root / "events").mkdir()
            news = [
                {
                    "status": "scheduled", "title": "Tomorrow", "description": "Not public", "url": "/news/tomorrow.html",
                    "image": "/images/card.webp", "alt": "Card", "tags": ["Update"], "publishedAt": "2026-07-13", "featured": True,
                },
                {
                    "title": "Published story", "description": "Public", "url": "/news/published.html", "image": "/images/feature.webp",
                    "alt": "Feature", "tags": ["Bargaining"], "author": {"name": "Local 083"}, "publishedAt": "2026-07-12", "featured": False,
                },
                {
                    "title": "Meeting update", "description": "Room confirmed", "url": "/news/meeting.html", "image": "/images/card.webp",
                    "alt": "Card", "tags": ["Events", "Update"], "author": {"name": "Local 083"}, "publishedAt": "2026-07-11", "featured": False,
                },
            ]
            events = [
                {"date": "2026-06-01", "time": "Noon", "title": "Older", "description": "Older event", "type": "Meeting", "url": "/events/older.html", "location_detail": "Online"},
                {"date": "2026-07-20", "time": "Evening", "title": "CAT Meeting", "description": "Organize", "type": "CAT Meeting", "url": "/events/cat.html", "location_detail": "Online"},
                {"date": "2027-01-05", "time": "Noon", "title": "Far Future", "description": "Later", "type": "Meeting", "url": "/events/future.html", "location_detail": "Online"},
            ]
            (root / "news" / "news.json").write_text(json.dumps(news), encoding="utf-8")
            (root / "events" / "events.json").write_text(
                json.dumps({"asOf": "2026-07-12", "events": events}), encoding="utf-8"
            )
            (root / "news.html").write_text(
                graph()
                + '<div id="news-flash">old</div><article id="lead-story">old</article><div id="latest-list">old</div>'
                + '<span id="latest-count">old</span><p id="results-status">old</p><div id="stories-grid">old</div>'
                + '<script>const fallbackNews = [{"old": true}];</script>',
                encoding="utf-8",
            )
            (root / "events.html").write_text(
                graph()
                + '<strong id="intro-count-number">0</strong><span id="intro-count-label">old</span><div id="intro-date-list">old</div>'
                + '<h2 id="month-label">old</h2><div id="agenda-list">old</div>'
                + '<script>const fallbackEvents = [{"old": true}];</script>',
                encoding="utf-8",
            )
            (root / "index.html").write_text(
                graph() + '<div id="upcoming-events-container">old</div><div id="news-grid-container">old</div>',
                encoding="utf-8",
            )

            static.build(root)
            first = {name: (root / name).read_text(encoding="utf-8") for name in ("index.html", "news.html", "events.html")}
            static.build(root)
            second = {name: (root / name).read_text(encoding="utf-8") for name in first}

            self.assertEqual(first, second)
            self.assertIn("Published story", first["news.html"])
            self.assertNotIn("Tomorrow", first["news.html"])
            self.assertIn("CAT Meeting", first["events.html"])
            self.assertIn("July 2026", first["events.html"])

            events.append({
                "date": "2026-08-06", "time": "Noon", "title": "August Meeting", "description": "Newly announced",
                "type": "Membership Meeting", "url": "/events/august.html", "location_detail": "Online",
            })
            (root / "events" / "events.json").write_text(
                json.dumps({"asOf": "2026-08-01", "events": events}), encoding="utf-8"
            )
            static.build(root)
            updated_events = (root / "events.html").read_text(encoding="utf-8")
            updated_home = (root / "index.html").read_text(encoding="utf-8")
            self.assertIn("August 2026", updated_events)
            self.assertIn("August Meeting", updated_home)

            (root / "events" / "events.json").write_text(
                json.dumps({"asOf": "2028-01-01", "events": events}), encoding="utf-8"
            )
            static.build(root)
            no_upcoming_home = (root / "index.html").read_text(encoding="utf-8")
            self.assertIn("No upcoming events", no_upcoming_home)
            self.assertIn('/events.html#past-events', no_upcoming_home)


if __name__ == "__main__":
    unittest.main()
