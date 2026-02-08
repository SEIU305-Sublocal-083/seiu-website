#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import List, Optional
import xml.etree.ElementTree as ET
from xml.dom import minidom


BASE_URL = "https://www.local083.org"
ROOT = Path(__file__).resolve().parent.parent
NEWS_JSON_PATH = ROOT / "news" / "news.json"
EVENTS_JSON_PATH = ROOT / "events" / "events.json"
NEWS_RSS_PATH = ROOT / "news" / "rss.xml"
EVENTS_RSS_PATH = ROOT / "events" / "rss.xml"
COMBINED_RSS_PATH = ROOT / "feed.xml"

ATOM_NS = "http://www.w3.org/2005/Atom"
ET.register_namespace("atom", ATOM_NS)


def absolute_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{BASE_URL}{path}"


def parse_date(value: Optional[str]) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    value = value.strip()
    if len(value) == 10:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def to_rfc2822(value: datetime) -> str:
    return format_datetime(value.astimezone(timezone.utc), usegmt=True)


def prettify_xml(element: ET.Element) -> str:
    raw = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(raw)
    return parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def add_item(
    channel: ET.Element,
    title: str,
    link: str,
    description: str,
    pub_date: datetime,
    guid: str,
    guid_is_permalink: bool,
    categories: Optional[List[str]] = None,
) -> None:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    guid_el = ET.SubElement(item, "guid")
    guid_el.set("isPermaLink", "true" if guid_is_permalink else "false")
    guid_el.text = guid
    ET.SubElement(item, "description").text = description
    ET.SubElement(item, "pubDate").text = to_rfc2822(pub_date)
    for category in categories or []:
        ET.SubElement(item, "category").text = category


def build_feed(
    *,
    title: str,
    description: str,
    self_path: str,
    items: List[dict],
) -> ET.Element:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = BASE_URL
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = to_rfc2822(datetime.now(timezone.utc))

    atom_link = ET.SubElement(channel, f"{{{ATOM_NS}}}link")
    atom_link.set("href", absolute_url(self_path))
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    for item in items:
        add_item(channel=channel, **item)

    return rss


def build_news_items(news_data: List[dict]) -> List[dict]:
    sorted_news = sorted(
        news_data,
        key=lambda n: parse_date(n.get("publishedAt") or n.get("createdAt")),
        reverse=True,
    )

    items: List[dict] = []
    for article in sorted_news:
        link = absolute_url(article.get("url", ""))
        description = article.get("description", "")
        items.append(
            {
                "title": article.get("title", "Untitled News"),
                "link": link,
                "description": description,
                "pub_date": parse_date(article.get("publishedAt") or article.get("createdAt")),
                "guid": link,
                "guid_is_permalink": True,
                "categories": article.get("tags", []),
            }
        )
    return items


def build_event_items(events_data: List[dict]) -> List[dict]:
    sorted_events = sorted(events_data, key=lambda e: parse_date(e.get("date")))
    items: List[dict] = []
    for event in sorted_events:
        link = absolute_url(event.get("url", ""))
        event_date = event.get("date", "")
        time_text = event.get("time", "").strip()
        location = event.get("location_detail", "").strip()
        description_parts = [event.get("description", "").strip()]
        if event_date:
            description_parts.append(f"Date: {event_date}")
        if time_text:
            description_parts.append(f"Time: {time_text}")
        if location:
            description_parts.append(f"Location: {location}")
        description = " | ".join([part for part in description_parts if part])
        event_guid = f"event:{event_date}:{event.get('title', 'Untitled Event')}"
        items.append(
            {
                "title": event.get("title", "Untitled Event"),
                "link": link,
                "description": description,
                "pub_date": parse_date(event.get("date")),
                "guid": event_guid,
                "guid_is_permalink": False,
                "categories": [event.get("type", "Event")] if event.get("type") else ["Event"],
            }
        )
    return items


def build_combined_items(news_items: List[dict], event_items: List[dict]) -> List[dict]:
    combined: List[dict] = []
    for item in news_items:
        combined.append(
            {
                **item,
                "title": f"[News] {item['title']}",
                "guid": f"{item['link']}#news",
                "guid_is_permalink": False,
            }
        )
    for item in event_items:
        combined.append(
            {
                **item,
                "title": f"[Event] {item['title']}",
                "guid": f"{item['guid']}:combined",
                "guid_is_permalink": False,
            }
        )
    return sorted(combined, key=lambda i: i["pub_date"], reverse=True)


def write_xml(path: Path, xml_root: ET.Element) -> None:
    content = prettify_xml(xml_root)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    news_data = json.loads(NEWS_JSON_PATH.read_text(encoding="utf-8"))
    events_data = json.loads(EVENTS_JSON_PATH.read_text(encoding="utf-8"))

    news_items = build_news_items(news_data)
    event_items = build_event_items(events_data)
    combined_items = build_combined_items(news_items, event_items)

    news_feed = build_feed(
        title="SEIU Local 503 at OSU - News",
        description="News and updates from SEIU Local 503 at Oregon State University.",
        self_path="/news/rss.xml",
        items=news_items,
    )
    events_feed = build_feed(
        title="SEIU Local 503 at OSU - Events",
        description="Upcoming events from SEIU Local 503 at Oregon State University.",
        self_path="/events/rss.xml",
        items=event_items,
    )
    combined_feed = build_feed(
        title="SEIU Local 503 at OSU - News and Events",
        description="Combined news and event updates from SEIU Local 503 at Oregon State University.",
        self_path="/feed.xml",
        items=combined_items,
    )

    write_xml(NEWS_RSS_PATH, news_feed)
    write_xml(EVENTS_RSS_PATH, events_feed)
    write_xml(COMBINED_RSS_PATH, combined_feed)

    print(f"Wrote {NEWS_RSS_PATH}")
    print(f"Wrote {EVENTS_RSS_PATH}")
    print(f"Wrote {COMBINED_RSS_PATH}")


if __name__ == "__main__":
    main()
