# SEIU Local 503 @ OSU Website

This repository contains the source code for the SEIU Local 503 at Oregon State University website. The site is built with HTML, Tailwind CSS, and a small amount of JavaScript to dynamically load events and news from JSON files.

## How it Works

The website uses a simple, flat-file structure. There is no complex build process or static site generator. Content is managed by editing HTML files and JSON data.

### Key Directories

*   `/events`: Contains individual HTML pages for each event and the `events.json` data file.
*   `/news`: Contains individual HTML pages for each news story and the `news.json` data file.
*   `/resources`: Holds important documents like the collective bargaining agreement and bylaws.
*   `/images`: Stores all images used on the site.

## Adding and Updating Content

### Events

To add a new event, you need to do two things:

1.  **Create an HTML file for the event** in the `/events` directory.
2.  **Add an entry to `events/events.json`**.

The `index.html` and `events.html` pages will automatically display upcoming events based on the data in `events.json`.

#### Event Naming Convention

Event files should be named using the following format:

`YYYY-MM-DD-short-title.html`

For example: `2025-10-31-halloween-party.html`

#### `events.json` Structure

Each event in `events.json` is an object with the following properties:

```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM AM/PM",
  "title": "Event Title",
  "description": "A brief description of the event.",
  "type": "Event Type (e.g., Meeting, Social)",
  "url": "/events/YYYY-MM-DD-short-title.html",
  "featured": false,
  "location_detail": "Location of the event"
}
```

*   `date`: The date of the event in `YYYY-MM-DD` format.
*   `time`: The time of the event.
*   `title`: The title of the event.
*   `description`: A short description.
*   `type`: The type of event (e.g., "Zoom Meeting", "Social Event").
*   `url`: The path to the event's HTML file.
*   `featured`: Set to `true` to highlight the event.
*   `location_detail`: A more specific location (e.g., "MU Ballroom").

### News

Adding a news story follows the same pattern as adding an event.

1.  **Create an HTML file for the news story** in the `/news` directory.
2.  **Add an entry to `news/news.json`**.

#### News Naming Convention

News files should be named using the following format:

`YYYY-MM-DD-short-title.html`

For example: `2025-09-30-bargaining-update.html`

#### `news.json` Structure

Each news item in `news.json` is an object with the following properties:

```json
{
  "date": "YYYY-MM-DD",
  "title": "News Story Title",
  "description": "A brief summary of the news.",
  "url": "/news/YYYY-MM-DD-short-title.html",
  "image": "/images/your-image.webp"
}
```

*   `date`: The publication date in `YYYY-MM-DD` format.
*   `title`: The headline of the news story.
*   `description`: A short summary.
*   `url`: The path to the news story's HTML file.
*   `image`: The path to an accompanying image.