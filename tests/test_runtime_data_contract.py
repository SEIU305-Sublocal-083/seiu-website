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
            "news/2026-07-09-latest-bargaining-update.html",
            "news/2026-07-09-tell-universities-hell-no.html",
        )
        fallback_href = "mailto:pres.office@oregonstate.edu?cc=trustees@oregonstate.edu"
        for page in fallback_pages:
            with self.subTest(page=page):
                self.assertIn(fallback_href, self.source(page))

    def test_current_action_announces_victory_and_retires_mobilization(self):
        payload = json.loads(self.source("data/current-action.json"))
        action = payload["actions"][payload["defaultAction"]]
        self.assertTrue(all(slug == action["slug"] for slug in payload["slots"].values()))
        self.assertEqual(action["ctas"][0]["href"], "/news/2026-09-28-we-won.html")
        self.assertIn("Report to work as scheduled", action["actionPage"]["nextStep"])
        self.assertEqual(payload["actions"]["strike-september-28"]["strikeClock"]["status"], "cancelled")
        for slug, old_action in payload["actions"].items():
            if slug != action["slug"]:
                self.assertIn("until", old_action["visibility"])
        for page in ("index.html", "action/index.html", "strike/index.html"):
            source = self.source(page)
            self.assertIn("3% and 3%", source)
            self.assertIn("The strike is off.", source)
            self.assertNotIn("data-strike-countdown", source)
            self.assertNotIn("WE’RE GOING ON STRIKE.", source)
            self.assertNotIn("data-home-strike-clock", source)

    def test_homepage_victory_keeps_a_static_fallback(self):
        payload = json.loads(self.source("data/current-action.json"))
        action = payload["actions"][payload["slots"]["homepageHero"]]
        self.assertEqual(action["type"], "contract_victory")
        self.assertIn(action["headline"], self.source("index.html"))
        self.assertIn(action["summary"], self.source("index.html"))
        self.assertNotIn('role="timer"', self.source("index.html"))


if __name__ == "__main__":
    unittest.main()
