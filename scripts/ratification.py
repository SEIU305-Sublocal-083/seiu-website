"""Render meeting links from the same verified records as the public calendar."""
from datetime import datetime
from html import escape


def render_meetings(events, ratified=False):
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
        link_label = "Past meeting details" if ratified else "Details, RSVP &amp; Zoom"
        cards.append(f'''<article class="ratification-card">
        <p class="ratification-kicker"><time datetime="{escape(event['schema_start_date'])}">{date_label}<br>{time}</time></p>
        <h3>{escape(campus)}</h3><p>{escape(event['location_detail'])}</p>
        <a class="ratification-button" href="{escape(event['url'])}">{link_label}<span class="sr-only">: {escape(campus)}</span></a>
        </article>''')
    heading = "Past ratification meetings" if ratified else "Ratification meetings"
    intro = "These informational meetings took place before ratification. Voting has concluded." if ratified else "Join in person or on Zoom for a presentation and Q&amp;A. Members and nonmembers are welcome. All times are Pacific."
    note = "For questions about our ratified contract, " if ratified else "These are informational meetings; voting happens online using your personal ballot. For accessibility or language support, "
    return f'''<div class="ratification-wrap"><h2>{heading}</h2>
    <p>{intro}</p>
    <div class="ratification-cards">{''.join(cards)}</div>
    <p style="margin-top:20px">{note}<a href="mailto:sharpes@seiu503.org?cc=083execteam%40seiu503.org">contact our organizer</a>.</p></div>'''
