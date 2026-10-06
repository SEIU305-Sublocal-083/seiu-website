"""Render meeting links from the same verified records as the public calendar."""
from datetime import datetime
from html import escape


def render_meetings(events):
    meetings = sorted(
        (event for event in events if "Ratification-Presentation" in event["url"]),
        key=lambda event: event["date"],
    )
    cards = []
    for event in meetings:
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        date_label = f"{date:%A}, {date:%B} {date.day}, {date.year}"
        campus = event["title"].split(" — ")[-1]
        time = event["time"].split(" · ")[0]
        cards.append(f'''<article class="ratification-card">
        <p class="ratification-kicker"><time datetime="{escape(event['schema_start_date'])}">{date_label}<br>{time}</time></p>
        <h3>{escape(campus)}</h3><p>{escape(event['location_detail'])}</p>
        <a class="ratification-button" href="{escape(event['url'])}">Details, RSVP &amp; Zoom<span class="sr-only">: {escape(campus)}</span></a>
        </article>''')
    return f'''<div class="ratification-wrap"><h2>Ratification meetings</h2>
    <p>Join in person or on Zoom for a presentation and Q&amp;A. Members and nonmembers are welcome. All times are Pacific.</p>
    <div class="ratification-cards">{''.join(cards)}</div>
    <p style="margin-top:20px">These are informational meetings; voting happens online using your personal ballot. For accessibility or language support, <a href="mailto:sharpes@seiu503.org">contact Sylvia Sharpe</a>.</p></div>'''
