#!/usr/bin/env python3
"""Rebuild JSON-driven HTML fallbacks and structured data.

The browser still enhances these pages from JSON, but the committed HTML is a
useful, crawlable and failure-safe snapshot generated from the same source.
"""

from __future__ import annotations

import argparse
import calendar
import html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.local083.org"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def date_value(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def long_date(value: str) -> str:
    date = date_value(value)
    return f"{date.strftime('%B')} {date.day}, {date.year}"


def short_date(value: str) -> str:
    date = date_value(value)
    return f"{date.strftime('%b')} {date.day}, {date.year}"


def public_news(items: list[dict]) -> list[dict]:
    """Return only committed public stories; scheduling changes status first."""
    published = [item for item in items if item.get("status", "published") == "published"]
    return sorted(published, key=lambda item: item.get("publishedAt", ""), reverse=True)


def renderable_events(items: list[dict]) -> list[dict]:
    valid = [item for item in items if item.get("date") and item.get("title") and item.get("url")]
    if not valid:
        raise ValueError("events/events.json contains no renderable events")
    return valid


def event_payload(data: object) -> tuple[datetime, list[dict]]:
    """Return the explicit editorial date and events from events.json.

    The committed fallback cannot use the build machine's clock without daily
    CI drift. Requiring `asOf` keeps builds repeatable while letting an editor
    advance the calendar snapshot in the same JSON edit that adds new events.
    """

    if not isinstance(data, dict):
        raise ValueError("events/events.json must contain an object with `asOf` and `events`")
    as_of = data.get("asOf")
    events = data.get("events")
    if not isinstance(as_of, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of):
        raise ValueError("events/events.json `asOf` must use YYYY-MM-DD")
    if not isinstance(events, list):
        raise ValueError("events/events.json `events` must be an array")
    return date_value(as_of), events


def snapshot_event_month(items: list[dict], as_of: datetime) -> tuple[int, int, list[dict]]:
    valid = renderable_events(items)
    future = [item for item in valid if date_value(item["date"]) >= as_of]
    candidate_months = {
        (date_value(item["date"]).year, date_value(item["date"]).month)
        for item in (future or valid)
    }
    year, month = min(candidate_months) if future else max(candidate_months)
    selected = sorted(
        [item for item in valid if (date_value(item["date"]).year, date_value(item["date"]).month) == (year, month)],
        key=lambda item: (item["date"], item.get("time", ""), item["title"]),
    )
    return year, month, selected


def homepage_events(items: list[dict], as_of: datetime, limit: int = 2) -> list[dict]:
    future = sorted(
        (item for item in renderable_events(items) if date_value(item["date"]) >= as_of),
        key=lambda item: (item["date"], item.get("time", ""), item["title"]),
    )
    return future[:limit]


def event_class(event_type: str = "") -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", event_type.lower()).strip("-")
    return normalized if normalized in {"membership-meeting", "zoom-meeting", "cat-meeting", "rally", "social-event"} else "default-event"


def event_icon(event_type: str = "") -> str:
    return {
        "membership-meeting": "◎",
        "zoom-meeting": "▣",
        "cat-meeting": "⚡",
        "rally": "✊",
        "social-event": "♥",
        "default-event": "•",
    }[event_class(event_type)]


def agenda_meta(event: dict) -> str:
    raw = event.get("time", "")
    location = event.get("location_detail") or "Details coming soon"
    if raw == "12:00 PM - 1:00 PM":
        time = "Noon–1 p.m."
    elif raw.lower().startswith("evening"):
        time = "Evening"
    else:
        time = raw.replace(" PT", "")
    if time == "Evening" and "details coming soon" in location.lower():
        return "Evening · Details coming soon"
    return f"{time} · {location}" if time else location


def replace_element_inner(source: str, element_id: str, inner: str) -> str:
    start = re.search(
        rf'<(?P<tag>[a-zA-Z][\w:-]*)\b[^>]*\bid=["\']{re.escape(element_id)}["\'][^>]*>',
        source,
    )
    if not start:
        raise ValueError(f"Required generated element is missing: #{element_id}")
    tag = start.group("tag")
    token_re = re.compile(rf'</?{re.escape(tag)}\b[^>]*>', re.IGNORECASE)
    depth = 1
    for token in token_re.finditer(source, start.end()):
        if token.group(0).startswith("</"):
            depth -= 1
        elif not token.group(0).rstrip().endswith("/>"):
            depth += 1
        if depth == 0:
            return source[: start.end()] + "\n" + inner.rstrip() + "\n" + source[token.start() :]
    raise ValueError(f"Generated element is not closed: #{element_id}")


def replace_js_array(source: str, variable: str, items: list[dict]) -> str:
    rendered = json.dumps(items, ensure_ascii=False, indent=2).replace("</", "<\\/")
    pattern = re.compile(rf"(?P<indent>[ \t]*)const\s+{re.escape(variable)}\s*=\s*\[.*?\];", re.DOTALL)
    match = pattern.search(source)
    if not match:
        raise ValueError(f"Required JavaScript fallback is missing: {variable}")
    indent = match.group("indent")
    indented = rendered.replace("\n", "\n" + indent)
    return source[: match.start()] + f"{indent}const {variable} = {indented};" + source[match.end() :]


def update_json_ld(source: str, update: Callable[[list[dict]], None]) -> str:
    pattern = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>\s*)(\{.*?\})(\s*</script>)', re.DOTALL)
    changed = False

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        data = json.loads(match.group(2))
        graph = data.get("@graph")
        if not isinstance(graph, list):
            return match.group(0)
        update(graph)
        changed = True
        return match.group(1) + json.dumps(data, ensure_ascii=False, indent=2) + match.group(3)

    rendered = pattern.sub(replace, source, count=1)
    if not changed:
        raise ValueError("Required @graph JSON-LD block was not found")
    return rendered


def lead_image(article: dict) -> tuple[str, str, int, int]:
    original = article.get("image") or "/images/card.webp"
    if original == "/images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd.webp":
        return (
            "/images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd-960w.webp",
            "/images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd-480w.webp 480w, /images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd-960w.webp 960w, /images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd-1440w.webp 1440w",
            1800,
            1084,
        )
    return original, "", 1200, 675


def thumbnail_url(image: str) -> str:
    return {
        "/images/card.webp": "/images/card-192.webp",
        "/images/2026-bargaining-zoom-backgrounds.webp": "/images/2026-bargaining-zoom-backgrounds-192.webp",
        "/images/3cd44f56-3666-4fa5-82ac-4bf3b8b00c0d-june-30-rally-speaker-with-camera.webp": "/images/3cd44f56-3666-4fa5-82ac-4bf3b8b00c0d-june-30-rally-speaker-with-camera-192.webp",
        "/images/83a4a1c4-4d9a-482a-8ad9-a3e73c338df3-wngr-barg-update.webp": "/images/83a4a1c4-4d9a-482a-8ad9-a3e73c338df3-wngr-barg-update-192.webp",
        "/images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd.webp": "/images/2cef7759-042d-4a05-9496-7eefff439a5e-june-30-rally-speaker-and-crowd-192.webp",
    }.get(image, image or "/images/card.webp")


def primary_topic(article: dict) -> str:
    return (article.get("tags") or ["Update"])[0]


def news_theme(article: dict) -> str:
    tags = set(article.get("tags") or [])
    if tags & {"Events", "Membership Meetings"}:
        return "theme-events"
    if tags & {"Action", "Rally"}:
        return "theme-action"
    if "Leadership" in tags:
        return "theme-leadership"
    if "Update" in tags:
        return "theme-update"
    return ""


def news_icon(article: dict) -> tuple[str, str]:
    tags = set(article.get("tags") or [])
    if tags & {"Events", "Membership Meetings"}:
        return "◫", "latest-icon-events"
    if tags & {"Action", "Rally"}:
        return "✦", "latest-icon-action"
    if "Leadership" in tags:
        return "★", "latest-icon-leadership"
    if tags & {"Contract", "Benefits", "Economics", "Bargaining"}:
        return "⇄", "latest-icon-contract"
    if "Update" in tags:
        return "!", "latest-icon-update"
    return "•", ""


def choose_lead(news: list[dict]) -> dict:
    return next((item for item in news if item.get("featured")), None) or next(
        (item for item in news if item.get("image") and not item["image"].endswith("/card.webp")),
        news[0],
    )


def render_news_flash(article: dict) -> str:
    label = "Meeting update" if "Events" in (article.get("tags") or []) else "Latest update"
    return f'''                <span class="flash-label">{esc(label)}</span>
                <a href="{esc(article['url'])}">
                    <span class="flash-copy"><strong>{esc(article['title'])}</strong> {esc(article.get('description'))}</span>
                    <time class="flash-date" datetime="{esc(article['publishedAt'])}">{esc(short_date(article['publishedAt']))}</time>
                </a>'''


def render_news_lead(article: dict) -> str:
    src, srcset, width, height = lead_image(article)
    responsive = f' srcset="{esc(srcset)}" sizes="(max-width: 767px) calc(100vw - 2rem), 55vw"' if srcset else ""
    credit = '\n                        <span class="photo-credit">Photo by Sylv Sharp, SEIU 503</span>' if "mcnary-field-rally-recap" in article["url"] else ""
    return f'''                    <a class="lead-image-wrap" href="{esc(article['url'])}">
                        <img src="{esc(src)}"{responsive} alt="{esc(article.get('alt') or article['title'])}" width="{width}" height="{height}" fetchpriority="high">{credit}
                    </a>
                    <div class="lead-copy">
                        <div class="story-kicker"><span>Lead story · {esc(primary_topic(article))}</span><time datetime="{esc(article['publishedAt'])}">{esc(long_date(article['publishedAt']))}</time></div>
                        <h2>{esc(article['title'])}</h2>
                        <p>{esc(article.get('description'))}</p>
                        <a class="story-link" href="{esc(article['url'])}">Read the story <span aria-hidden="true">→</span></a>
                    </div>'''


def render_latest(news: list[dict]) -> str:
    rows = []
    for article in news[:8]:
        symbol, class_name = news_icon(article)
        rows.append(f'''                        <a class="latest-item" href="{esc(article['url'])}">
                            <span class="latest-thumb"><img src="{esc(thumbnail_url(article.get('image', '')))}" alt="" width="96" height="96" loading="lazy"><span class="latest-icon {class_name}" aria-hidden="true">{symbol}</span></span>
                            <span class="latest-copy"><time class="latest-date" datetime="{esc(article['publishedAt'])}">{esc(short_date(article['publishedAt']))}</time><span class="latest-title">{esc(article['title'])}</span></span>
                            <span class="latest-arrow" aria-hidden="true">→</span>
                        </a>''')
    return "\n".join(rows)


def render_story_card(article: dict, *, wide: bool = False) -> str:
    src, srcset, width, height = lead_image(article)
    responsive = f' srcset="{esc(srcset)}" sizes="(max-width: 767px) calc(100vw - 2rem), 50vw"' if srcset else ""
    author = (article.get("author") or {}).get("name") or "SEIU Local 503, Local 083"
    classes = " ".join(value for value in ("story-card", news_theme(article), "is-wide" if wide else "") if value)
    return f'''                <article class="{classes}">
                    <a class="story-image-link" href="{esc(article['url'])}"><img class="story-image" src="{esc(src)}"{responsive} alt="{esc(article.get('alt') or article['title'])}" width="{width}" height="{height}" loading="lazy"></a>
                    <div class="story-body">
                        <div class="story-meta"><span class="story-topic">{esc(primary_topic(article))}</span><time datetime="{esc(article['publishedAt'])}">{esc(long_date(article['publishedAt']))}</time></div>
                        <h3><a href="{esc(article['url'])}">{esc(article['title'])}</a></h3>
                        <p class="story-description">{esc(article.get('description'))}</p>
                        <div class="story-footer"><span class="story-author">{esc(author)}</span><a class="story-read" href="{esc(article['url'])}" aria-label="Read {esc(article['title'])}">Read the story →</a></div>
                    </div>
                </article>'''


def render_home_news(news: list[dict]) -> str:
    lead = choose_lead(news)
    side = [item for item in news if item["url"] != lead["url"]][:2]
    src, srcset, width, height = lead_image(lead)
    responsive = f' srcset="{esc(srcset)}" sizes="(max-width: 767px) calc(100vw - 2rem), 55vw"' if srcset else ""
    main = f'''                <article class="news-card bg-white rounded-2xl border border-border-color overflow-hidden group">
                    <a href="{esc(lead['url'])}" class="block news-card-media aspect-[16/9]" aria-label="Read {esc(lead['title'])}"><img src="{esc(src)}"{responsive} alt="{esc(lead.get('alt') or lead['title'])}" loading="lazy" decoding="async" width="{width}" height="{height}"></a>
                    <div class="p-6 md:p-8">
                        <div class="flex items-center gap-3 text-sm mb-4"><span class="bg-brand-purple-light text-brand-purple-dark font-bold rounded-full px-3 py-1">{esc(primary_topic(lead))}</span><span class="text-text-secondary">{esc(long_date(lead['publishedAt']))}</span></div>
                        <h3 class="font-bold text-3xl md:text-4xl leading-tight mb-4">{esc(lead['title'])}</h3>
                        <p class="text-text-secondary leading-relaxed">{esc(lead.get('description'))}</p>
                        <a href="{esc(lead['url'])}" class="text-brand-purple font-bold mt-5 inline-block group-hover:underline">Read the story →</a>
                    </div>
                </article>'''
    side_rows = []
    for article in side:
        side_src, side_srcset, side_width, side_height = lead_image(article)
        side_responsive = f' srcset="{esc(side_srcset)}" sizes="(max-width: 767px) calc(100vw - 2rem), 40vw"' if side_srcset else ""
        side_rows.append(f'''                    <article class="news-card bg-white rounded-2xl border border-border-color overflow-hidden group">
                        <a href="{esc(article['url'])}" class="block news-card-media aspect-[16/7]" aria-label="Read {esc(article['title'])}"><img src="{esc(side_src)}"{side_responsive} alt="{esc(article.get('alt') or article['title'])}" loading="lazy" decoding="async" width="{side_width}" height="{side_height}"></a>
                        <div class="p-5 md:p-6"><div class="flex items-center gap-3 text-xs mb-3"><span class="font-bold uppercase tracking-wide text-brand-purple">{esc(primary_topic(article))}</span><span class="text-text-secondary">{esc(long_date(article['publishedAt']))}</span></div><h3 class="font-bold text-xl md:text-2xl leading-tight mb-3">{esc(article['title'])}</h3><p class="text-text-secondary text-sm leading-relaxed">{esc(article.get('description'))}</p><a href="{esc(article['url'])}" class="text-brand-purple font-bold mt-4 inline-block group-hover:underline">Read the story →</a></div>
                    </article>''')
    return main + '\n                <div class="space-y-6">\n' + "\n".join(side_rows) + "\n                </div>"


def render_home_event(event: dict) -> str:
    date = date_value(event["date"])
    featured = bool(event.get("featured"))
    border = "border-2 border-brand-purple shadow-xl" if featured else "border border-border-color"
    badge = "bg-brand-purple text-white" if featured else "bg-brand-purple-light text-brand-purple-dark"
    footer = "bg-brand-purple-light" if featured else "bg-gray-50"
    raw_time = event.get("time", "")
    time = "Noon" if raw_time.startswith("12:00 PM") else "Evening" if raw_time.lower().startswith("evening") else raw_time.split(" - ")[0].replace(" PT", "")
    return f'''                <article class="event-card bg-white rounded-2xl {border} overflow-hidden flex flex-col">
                    <div class="p-6 md:p-7 flex-grow"><div class="flex items-start justify-between gap-4 mb-6"><div class="event-date" aria-label="{esc(date.strftime('%A'))}, {esc(long_date(event['date']))}"><span class="event-date-month">{esc(date.strftime('%b'))}</span><span class="event-date-day">{date.day}</span></div><div class="text-right"><div class="{badge} inline-flex font-bold rounded-full px-3 py-1 text-xs uppercase tracking-wide">{esc(event.get('type') or 'Event')}</div><div class="mt-3 text-sm font-semibold text-text-secondary"><span aria-hidden="true">●</span> {esc(time)}</div></div></div>
                        <h3 class="font-bold text-2xl md:text-3xl mb-3">{esc(event['title'])}</h3><p class="text-text-secondary leading-relaxed">{esc(event.get('description'))}</p><p class="mt-3 text-sm text-text-secondary"><strong>Where:</strong> {esc(event.get('location_detail') or 'Details coming soon')}</p>
                    </div>
                    <div class="{footer} border-t border-border-color p-4 flex items-center justify-between gap-3"><span class="text-sm font-bold text-text-primary">{esc(date.strftime('%a'))}, {esc(short_date(event['date']))}</span><a href="{esc(event['url'])}" class="font-bold text-brand-purple hover:underline" aria-label="View {esc(event['title'])} details">View event details →</a></div>
                </article>'''


def render_home_events(events: list[dict]) -> str:
    if events:
        return "\n".join(render_home_event(item) for item in events)
    return '''                <div class="col-span-full flex flex-col items-center justify-center py-12 px-6 bg-white rounded-xl border border-border-color border-dashed">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <h3 class="text-xl font-bold text-brand-purple-dark mb-2">No upcoming events</h3>
                    <p class="text-text-secondary mb-6 text-center max-w-md">No upcoming events are currently announced. Browse past events or check back for new dates.</p>
                    <a href="/events.html#past-events" class="btn btn-outline">View past events</a>
                </div>'''


def render_agenda(events: list[dict]) -> str:
    rows = []
    for event in events:
        date = date_value(event["date"])
        rows.append(f'''                        <article class="agenda-card {event_class(event.get('type', ''))}">
                            <div class="agenda-date"><span>{esc(date.strftime('%a'))}</span><strong>{date.day}</strong></div>
                            <div class="agenda-copy"><span class="agenda-type"><span class="event-icon" aria-hidden="true">{event_icon(event.get('type', ''))}</span>{esc(event.get('type') or 'Local 083 event')}</span><h3>{esc(event['title'])}</h3><p>{esc(agenda_meta(event))}</p></div>
                            <a class="agenda-link" href="{esc(event['url'])}" aria-label="View {esc(event['title'])} details">View event details →</a>
                        </article>''')
    return "\n".join(rows)


def render_glance(events: list[dict], month: int) -> str:
    rows = []
    for event in events[:2]:
        date = date_value(event["date"])
        rows.append(f'''                        <div class="glance-date {event_class(event.get('type', ''))}">
                            <strong>{date.day}</strong><div class="glance-date-copy"><small>{esc(date.strftime('%a'))} · {esc(calendar.month_name[month])}</small><span>{event_icon(event.get('type', ''))} {esc(event.get('type') or event['title'])}</span></div>
                        </div>''')
    if len(events) > 2:
        rows.append(f'                        <span class="glance-more">+{len(events) - 2} more in the calendar</span>')
    return "\n".join(rows)


def update_news_graph(graph: list[dict], news: list[dict]) -> None:
    item_list = next((item for item in graph if item.get("@type") == "ItemList"), None)
    if item_list is None:
        item_list = {"@type": "ItemList", "@id": f"{BASE_URL}/news.html#news-list"}
        graph.append(item_list)
    entries = news[:8]
    item_list["numberOfItems"] = len(entries)
    item_list["itemListElement"] = [
        {"@type": "ListItem", "position": position, "url": f"{BASE_URL}{item['url']}", "name": item["title"]}
        for position, item in enumerate(entries, 1)
    ]


def event_schema(event: dict) -> dict:
    url = f"{BASE_URL}{event['url']}"
    schema = {
        "@type": "Event",
        "@id": f"{url}#event",
        "name": event["title"],
        "description": event.get("description", ""),
        "startDate": event["date"],
        "eventStatus": "https://schema.org/EventScheduled",
        "url": url,
        "organizer": {"@id": f"{BASE_URL}#organization"},
    }
    location = event.get("location_detail", "")
    if location and "details coming soon" not in location.lower():
        schema["location"] = {"@type": "Place", "name": location}
    return schema


def update_events_graph(graph: list[dict], events: list[dict]) -> None:
    graph[:] = [item for item in graph if item.get("@type") != "Event"]
    item_list = next((item for item in graph if item.get("@type") == "ItemList"), None)
    if item_list is None:
        item_list = {"@type": "ItemList", "@id": f"{BASE_URL}/events.html#event-list"}
        graph.append(item_list)
    item_list["numberOfItems"] = len(events)
    item_list["itemListElement"] = [
        {"@type": "ListItem", "position": position, "item": {"@id": f"{BASE_URL}{item['url']}#event"}}
        for position, item in enumerate(events, 1)
    ]
    graph.extend(event_schema(event) for event in events)


def update_home_graph(graph: list[dict], news: list[dict], events: list[dict]) -> None:
    graph[:] = [item for item in graph if item.get("@id") not in {f"{BASE_URL}/#home-news-list", f"{BASE_URL}/#home-event-list"}]
    graph.extend((
        {
            "@type": "ItemList",
            "@id": f"{BASE_URL}/#home-news-list",
            "name": "Latest Local 083 news",
            "numberOfItems": min(3, len(news)),
            "itemListElement": [
                {"@type": "ListItem", "position": position, "url": f"{BASE_URL}{item['url']}", "name": item["title"]}
                for position, item in enumerate(news[:3], 1)
            ],
        },
        {
            "@type": "ItemList",
            "@id": f"{BASE_URL}/#home-event-list",
            "name": "Latest announced Local 083 events",
            "numberOfItems": min(2, len(events)),
            "itemListElement": [
                {"@type": "ListItem", "position": position, "url": f"{BASE_URL}{item['url']}", "name": item["title"]}
                for position, item in enumerate(events[:2], 1)
            ],
        },
    ))


def build(root: Path = ROOT) -> list[Path]:
    news = public_news(json.loads((root / "news" / "news.json").read_text(encoding="utf-8")))
    as_of, events_all = event_payload(json.loads((root / "events" / "events.json").read_text(encoding="utf-8")))
    if not news:
        raise ValueError("news/news.json contains no published stories")
    year, month, events = snapshot_event_month(events_all, as_of)

    news_path = root / "news.html"
    source = news_path.read_text(encoding="utf-8")
    flash = next((item for item in news if {"Events", "Update"}.issubset(set(item.get("tags") or []))), news[0])
    lead = choose_lead(news)
    archive = [item for item in news if item["url"] != lead["url"]][:7]
    source = replace_element_inner(source, "news-flash", render_news_flash(flash))
    source = replace_element_inner(source, "lead-story", render_news_lead(lead))
    source = replace_element_inner(source, "latest-list", render_latest(news))
    source = replace_element_inner(source, "stories-grid", "\n".join(render_story_card(item, wide=index == 0) for index, item in enumerate(archive)))
    source = replace_element_inner(source, "latest-count", f"{min(8, len(news))} recent {'story' if len(news) == 1 else 'stories'}")
    source = replace_element_inner(source, "results-status", f"Showing {len(archive)} of {max(0, len(news) - 1)} stories")
    source = replace_js_array(source, "fallbackNews", news)
    source = update_json_ld(source, lambda graph: update_news_graph(graph, news))
    news_path.write_text(source, encoding="utf-8")

    events_path = root / "events.html"
    source = events_path.read_text(encoding="utf-8")
    source = replace_element_inner(source, "agenda-list", render_agenda(events))
    source = replace_element_inner(source, "intro-count-number", str(len(events)))
    source = replace_element_inner(source, "intro-count-label", f"{'event' if len(events) == 1 else 'events'} announced<br>in {calendar.month_name[month]}")
    source = replace_element_inner(source, "intro-date-list", render_glance(events, month))
    source = replace_element_inner(source, "month-label", f"{calendar.month_name[month]} {year}")
    source = replace_js_array(source, "fallbackEvents", events_all)
    source = update_json_ld(source, lambda graph: update_events_graph(graph, events))
    events_path.write_text(source, encoding="utf-8")

    home_path = root / "index.html"
    source = home_path.read_text(encoding="utf-8")
    home_events = homepage_events(events_all, as_of)
    source = replace_element_inner(source, "upcoming-events-container", render_home_events(home_events))
    source = replace_element_inner(source, "news-grid-container", render_home_news(news))
    source = update_json_ld(source, lambda graph: update_home_graph(graph, news, home_events))
    home_path.write_text(source, encoding="utf-8")

    return [home_path, news_path, events_path]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    for path in build(args.root.resolve()):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
