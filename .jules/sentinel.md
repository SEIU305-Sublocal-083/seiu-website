## 2025-05-06 - [DOM-based XSS and Regex Injection]
**Vulnerability:** User input (`query`) and search results were injected into the DOM via `innerHTML` without escaping in `test-pages/search.html`. Additionally, user input was directly passed to `new RegExp()` causing Regex Injection risks.
**Learning:** The application uses client-side rendering with `.innerHTML` across multiple scripts (`js/news.js`, `index.html`, `test-pages/search.html`). This pattern is highly susceptible to DOM-based XSS when handling any dynamic data, especially user-provided search queries.
**Prevention:** Always escape data before inserting it into the DOM. For this codebase, I created `js/utils.js` providing `window.Sentinel.escapeHTML`. Any script dynamically rendering HTML should include `<script src="/js/utils.js"></script>` and apply `escapeHTML()` to all interpolated variables. Additionally, escape regular expression control characters using `.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')` when constructing regex from user input.

## 2025-05-09 - [DOM-based XSS in Homepage]
**Vulnerability:** JSON response data for Events and News in `index.html` were injected into the DOM via `innerHTML` without escaping, exposing the site to DOM-based Cross-Site Scripting (XSS).
**Learning:** Even though the JSON payload comes from a trusted internal source (`/events/events.json` and `/news/news.json`), client-side XSS vulnerabilities manifest if data is directly interpolated into HTML strings. The missing shared `escapeHTML` helper highlighted that scripts embedded directly in HTML files (like the one in `index.html`) can be easily overlooked.
**Prevention:** Ensured the `escapeHTML` helper was defined locally in `index.html` (falling back to `window.Sentinel.escapeHTML` if available) and wrapped all dynamic interpolations (`event.title`, `event.time`, `story.description`, etc.) before rendering. Continue to systematically audit any remaining instances of `innerHTML` across other views (like `events.html`).

## 2025-05-10 - [DOM-based XSS in Events Page]
**Vulnerability:** Similar to the homepage, `events.html` retrieved JSON data (`events.json`) and injected properties directly into the DOM using `innerHTML` without sanitization, posing a risk for DOM-based XSS if the data source was ever compromised or altered maliciously.
**Learning:** The application extensively utilizes string interpolation into `innerHTML` for client-side templating across multiple pages. When refactoring or replicating templates (like moving from `index.html` to `events.html`), developers must be vigilant to include and apply escaping logic universally.
**Prevention:** Injected the `escapeHTML` helper function into the inline script of `events.html` and consistently wrapped all variable interpolations (`event.title`, `event.url`, `event.description`, etc.) with `escapeHTML()`. Continued diligence is required for any new client-rendered views.

## 2025-05-11 - [DOM-based XSS in Featured News Article and Survey Tracker]
**Vulnerability:** User-controlled data for the featured news article (`article.url`, `article.title`, `article.description`, `article.image`) was injected into the DOM via `innerHTML` without escaping in `js/news.js`. A similar vulnerability existed in `2026-bargaining/survey-tracker.html` where department names were directly interpolated.
**Learning:** Even when the main rendering loops (like `displayArticles` in `js/news.js`) implement proper sanitization, secondary rendering paths (like the featured article banner or one-off campaign trackers) are often overlooked. This inconsistency creates critical blind spots for DOM-based XSS.
**Prevention:** Apply `escapeHTML` (and `escapeAttr` for attributes) universally to *all* properties injected into HTML strings, regardless of where they appear on the page or whether the component is a "one-off". Consistent use of a shared library (`utils.js`) helps maintain this standard across both external scripts and inline script tags.

## 2025-05-12 - [DOM-based XSS in News Articles Grid]
**Vulnerability:** User-controlled data for the news articles grid (`article.url`, `article.image`, `article.formattedUpdatedAt` and tag URLs) was injected into the DOM via `innerHTML` without escaping in `js/news.js`.
**Learning:** Even though `renderFeaturedArticle` correctly escaped attributes, `displayArticles` (the main render loop) missed them for `url` and `image`. This highlights the need for consistency across all rendering paths, not just secondary ones.
**Prevention:** Apply `escapeHTML` (and `escapeAttr` for attributes) universally to *all* properties injected into HTML strings across *all* rendering loops. Consistent use of shared helper functions prevents these oversights.
