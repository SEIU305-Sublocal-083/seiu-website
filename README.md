# SEIU Local 503 @ OSU Website

This repository contains the source code for the SEIU Local 503 at Oregon State University website. It is a static HTML site with Tailwind CSS and small, progressively enhanced JavaScript features. News and event data live in JSON; a lightweight build command writes crawlable HTML fallbacks, RSS feeds, structured data, the shared public-page shell, the sitemap, and compiled CSS.

## How it Works

The website uses a simple, flat-file structure. There is no application server or framework. Content is managed by editing HTML files and JSON data, then running one deterministic build command:

```bash
python3 scripts/build_site.py
```

The generated files are committed to the repository so the deployed site stays fully static and works even when JavaScript is unavailable. The same command also synchronizes the canonical header and footer across every public page. GitHub Actions reruns the build and fails if committed output has drifted from its sources.

### Key Directories

*   `/events`: Contains individual HTML pages for each event and the `events.json` data file.
*   `/news`: Contains individual HTML pages for each news story and the `news.json` data file.
*   `/resources`: Holds important documents like the collective bargaining agreement and bylaws.
*   `/images`: Stores all images used on the site.

## Adding and Updating Content

### Email Campaigns

Email HTML and campaign briefs live in `/marketing/email`.

Use these docs when planning Mailchimp sends:

*   `/marketing/email/mailchimp-segment-strategy.md`: Defines how to treat the broad list, `Engaged subscribers`, and `Disengaged subscribers`.
*   `/marketing/email/mailchimp-campaign-brief-template.md`: Reusable template for writing segment-aware campaign briefs with distinct subject lines, CTAs, and metrics.

### Events

To add a new event, you need to do three things:

1.  **Create an HTML file for the event** in the `/events` directory. Use `/templates/events/template.html` as a starting point (copy it into `test-pages/` first).
2.  **Create an iCalendar (`.ics`) file** in the `/events/ical` directory. This allows users to add the event to their calendar.
3.  **Add an entry to `events/events.json`**.

The build updates the event listings on `index.html` and `events.html`, their static fallbacks and structured data from `events.json`. Browser JavaScript can then enhance those committed fallbacks.

#### 1. Event Naming Convention

Event files should be named using the following format:

`YYYY-MM-DD-short-title.html`

For example: `2025-10-31-halloween-party.html`

#### 2. Creating the iCalendar (`.ics`) File

To make an "Add to Calendar" link for your event, follow these steps:

1.  **Copy the template:** Duplicate the file `/events/ical/template.ics`.
2.  **Rename the file:** Name it to match your event, e.g., `2025-10-31-halloween-party.ics`.
3.  **Edit the contents:** Open the new `.ics` file and replace the `{{PLACEHOLDERS}}` with the event's details.
    *   `SUMMARY`: The title of the event.
    *   `UID`: A unique identifier for the event. The format `YYYYMMDD-event-name` is recommended.
    *   `DTSTAMP`: The time the event was created, in UTC. Format: `YYYYMMDDTHHMMSSZ`. (e.g., `20251021T153500Z`)
    *   `DTSTART`: The start time of the event. Format: `YYYYMMDDTHHMMSSZ`.
    *   `DTEND`: The end time of the event. Format: `YYYYMMDDTHHMMSSZ`.
    *   `DESCRIPTION`: A short description of the event.
    *   `LOCATION`: The location of the event.
    *   `URL`: The full URL to the event page on the website.

#### 3. `events.json` Structure

`events.json` has an explicit editorial snapshot date and an array of event objects:

```json
{
  "asOf": "YYYY-MM-DD",
  "events": [
    {
      "date": "YYYY-MM-DD",
      "time": "HH:MM AM/PM",
      "title": "Event Title",
      "description": "A brief description of the event.",
      "type": "Event Type (e.g., Meeting, Social)",
      "url": "/events/YYYY-MM-DD-short-title.html",
      "featured": false,
      "location_detail": "Location of the event",
      "calendar_link": "/events/ical/YYYY-MM-DD-short-title.ics"
    }
  ]
}
```

*   `asOf`: The date the committed calendar snapshot should consider current. Advance it when publishing calendar changes so the static homepage and events page surface the nearest relevant announced events. Keeping this value in the data file makes builds repeatable on every machine.
*   `events`: The complete array of event records.
*   `date`: The date of the event in `YYYY-MM-DD` format.
*   `time`: The time of the event.
*   `title`: The title of the event.
*   `description`: A short description.
*   `type`: The type of event (e.g., "Zoom Meeting", "Social Event").
*   `url`: The path to the event's HTML file.
*   `featured`: Set to `true` to highlight the event.
*   `location_detail`: A more specific location (e.g., "MU Ballroom").
*   `calendar_link`: (Optional) The path to the corresponding `.ics` file.

### News

Adding a news story follows the same pattern as adding an event.

1.  **Create an HTML file for the news story** in the `/news` directory. Start from `/templates/news/ba-template.html` or `/templates/news/spotlight-template.html` (copy into `test-pages/` first).
2.  **Add an entry to `news/news.json`**.

#### News Naming Convention

News files should be named using the following format:

`YYYY-MM-DD-short-title.html`

For example: `2025-09-30-bargaining-update.html`

#### `news.json` Structure

Each news item in `news.json` is an object with the following properties:

```json
{
  "title": "News Story Title",
  "description": "A brief summary of the news.",
  "url": "/news/YYYY-MM-DD-short-title.html",
  "image": "/images/your-image.webp",
  "tags": ["Events", "Membership Meetings"],
  "author": {
    "name": "Author Name",
    "title": "Author Title"
  },
  "publishedAt": "YYYY-MM-DD",
  "createdAt": "YYYY-MM-DD",
  "updatedAt": "YYYY-MM-DD",
  "featured": false
}
```

*   `title`: The headline of the news story.
*   `description`: A short summary.
*   `url`: The path to the news story's HTML file.
*   `image`: The path to an accompanying image.
*   `tags`: An array of strings to categorize the news story.
*   `author`: An object containing the name and title of the author.
*   `publishedAt`: The date the story was published in `YYYY-MM-DD` format.
*   `createdAt`: The date the story was created in `YYYY-MM-DD` format.
*   `updatedAt`: The date the story was last updated in `YYYY-MM-DD` format.
*   `featured`: Set to `true` to highlight the news story.

### Rebuild generated files

After changing `events/events.json`, `news/news.json`, a public page, or Tailwind classes, run:

```bash
python3 scripts/build_site.py
```

Commit the source change and generated output in the **same human commit**. Depending on the change, generated output can include:

* Public HTML pages when the shared header or footer changes
* `index.html`, `events.html`, and `news.html` when JSON-driven listings change
* `events/rss.xml`, `news/rss.xml`, and `feed.xml`
* `sitemap.xml` and `robots.txt`
* `styles/tailwind.css`

Before opening a pull request, verify there is no build drift:

```bash
python3 scripts/build_site.py --check
```

The check rebuilds the site and fails when rebuilding would change a generated file. CI starts from the committed version and runs the same check; it does not make a follow-up bot commit.

## Drafting and Publishing Workflow

Use the draft-first workflow documented in `/DRAFTING_WORKFLOW.md`.

Templates now live in `/templates/` (subfolders for events, news, minutes, marketing, misc). Copy from there into `test-pages/` to start drafts.

### Required flow

1. Create and review new pages in `/test-pages` first.
2. Promote to production path only after content and metadata are complete.
3. Update index/data files when applicable:
   *   Events: `events/events.json`
   *   News: `news/news.json`
4. Build the static site and run required publish checks:

```bash
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/site_quality_check.py --strict-placeholders
```

### Publish checklist summary

*   No placeholders, TODOs, or dummy links.
*   Canonical + OG + Twitter URLs aligned to final production URL.
*   JSON-LD includes `Organization`, `WebSite`, and `WebPage` (plus `Event` on event pages).
*   Internal links and asset paths resolve.
*   Voice uses \"our union\" framing (never othering language).

### Helper: promote script

Use the helper to move a finished draft out of `test-pages/` and get reminders:

```bash
scripts/promote_page.sh test-pages/my-draft.html events 2026-04-12-rally.html
```

## RSS Feeds

This site publishes RSS feeds for news and events:

*   `https://www.local083.org/news/rss.xml`
*   `https://www.local083.org/events/rss.xml`
*   `https://www.local083.org/feed.xml` (combined)

### How it is generated

1.  The script `scripts/generate_rss.py` reads:
    *   `news/news.json`
    *   `events/events.json`
2.  It writes:
    *   `news/rss.xml`
    *   `events/rss.xml`
    *   `feed.xml`

RSS is part of `python3 scripts/build_site.py`. Commit feed changes alongside the JSON that produced them. The site-quality workflow verifies that those generated files are current instead of creating a second bot-authored commit.

Scheduled news is the one automated publishing exception: `.github/workflows/publish-scheduled-news.yml` promotes due stories to `published`, removes `noindex`, runs the same full site build and quality check, and commits all resulting files together.

## Wayback Machine Archiving (Automated)

This site can be automatically submitted to Internet Archive's Save Page Now using:

*   Workflow: `.github/workflows/wayback-archive.yml`
*   Script: `scripts/archive_wayback.py`

### Trigger options

*   **Scheduled**: Runs weekly on Mondays.
*   **Manual**: Run from the Actions tab with optional inputs:
    *   `max_urls` (default `0` = archive every URL in `sitemap.xml`)
    *   `delay_seconds` (default `5`)
    *   `fail_on_error` (default `false`)

### Notes

*   URLs are read from `sitemap.xml`.
*   Requests are rate-limited using `delay_seconds` to reduce throttling risk.
