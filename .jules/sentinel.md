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

## 2025-05-12 - [DOM-based XSS in News Grid via JS]
**Vulnerability:** User-controlled data (specifically `article.url`, `article.image`, and `article.formattedUpdatedAt`) was injected into the DOM via `articleCard.innerHTML` without escaping in `js/news.js`.
**Learning:** Even though `js/news.js` was using `escapeHtml` for strings and `escapeAttr` for other attributes (like title for the tooltip), `article.url` and `article.image` attributes inside `img` and `a` tags were missed. XSS can occur when attributes are injected unescaped just as easily as inner text.
**Prevention:** Ensured the `escapeAttr` helper was applied to `article.url` and `article.image` and `escapeHtml` was applied to `article.formattedUpdatedAt` in the string template interpolation in `displayArticles` in `js/news.js`. Continue to be rigorous about using `escapeAttr` for any variables within HTML attributes, especially `href` and `src`.
## 2025-05-14 - [DOM-based XSS in News Articles Grid]
**Vulnerability:** User-controlled data for news articles (`article.url`, `article.image`, `article.formattedUpdatedAt`) was injected into the DOM via `innerHTML` without escaping in the main `displayArticles` function of `js/news.js`.
**Learning:** Even if primary text properties (`title`, `description`) are escaped, unescaped attributes (like `href` or `src`) are extremely dangerous, especially if the data can contain `javascript:` URIs or break out of attribute quotes. The main rendering loops need the same scrutiny as one-off components.
**Prevention:** Always apply `escapeAttr()` to URLs and image paths, and `escapeHtml()` to any text before injecting it into HTML strings via `.innerHTML`. Ensure consistent escaping across all properties within a templated string.

## 2025-05-16 - [DOM-based XSS in Event Passcode Copy]
**Vulnerability:** In multiple event pages (like `events/2025-08-21-Membership-Meeting.html`) and the event template (`templates/events/template.html`), the copy passcode script saved the original text using `const originalPasscodeText = passcodeTextElement.innerHTML;` and later restored it with `passcodeTextElement.innerHTML = originalPasscodeText;`.
**Learning:** Using `.innerHTML` to save and restore strictly text values is a bad practice. Even if the content appears static at the time of authoring, any future modifications that introduce dynamic or unescaped user data into that element would instantly create a DOM-based XSS vulnerability when the content is restored.
**Prevention:** Always use `.textContent` or `.innerText` when reading or writing purely text values to the DOM. I replaced `.innerHTML` with `.textContent` across all event files and the template to ensure the text restoration process remains immune to XSS.

## 2025-05-18 - [DOM-based XSS via javascript: URIs]
**Vulnerability:** User-controlled URLs (like `article.url` or `article.image`) were escaped for HTML entities using `escapeAttr`, but were not sanitized against executing JavaScript (e.g. `javascript:alert(1)`) or injecting malicious data (`data:text/html,...`) when injected into `href` or `src` attributes.
**Learning:** `escapeHTML` and `escapeAttr` protect against breaking out of the attribute context (e.g. `"><script>`), but they do not protect against the protocol-level execution of JavaScript when a user clicks the link or the browser loads the source.
**Prevention:** Always validate and sanitize URLs before rendering them into `href` or `src` attributes using `.innerHTML`. Created `window.Sentinel.sanitizeUrl()` in `js/utils.js` (and localized it in `js/news.js`) to explicitly reject any URL starting with `javascript:` or `data:`.
## 2025-05-20 - [DOM-based XSS via javascript: URIs in Multiple HTML files]
**Vulnerability:** User-controlled URLs (like `event.url`, `event.calendar_link`, `item.url`, `article.url`) were escaped for HTML entities using `escapeHTML` or `escapeAttr`, but were not sanitized against executing JavaScript (e.g. `javascript:alert(1)`) or injecting malicious data (`data:text/html,...`) when injected into `href` attributes in `events.html`, `test-pages/search.html`, and `test-pages/2026-bargaining-redesign.html`.
**Learning:** `escapeHTML` and `escapeAttr` protect against breaking out of the attribute context (e.g. `"><script>`), but they do not protect against the protocol-level execution of JavaScript when a user clicks the link. Even after the creation of `window.Sentinel.sanitizeUrl()`, it wasn't being used consistently across all inline rendering scripts.
**Prevention:** Always use `sanitizeUrl()` for dynamic `href` attribute injections. Be careful NOT to use it on `src` attributes for images, as it will explicitly block legitimate base64-encoded `data:` URIs, breaking those images. Make sure to apply it universally across all client-rendered views.

## 2026-05-23 - [DOM-based XSS via javascript: URIs in Email Editor]
**Vulnerability:** In `marketing/email-editor/index.html`, user-provided URLs in 'button' and 'links' blocks were injected into the `href` attributes of `<a>` tags. While the code used `escapeAttr()` (which escapes HTML entities), it did not sanitize the URL scheme, allowing `javascript:` or `data:` URIs to execute if the preview or exported HTML was interacted with.
**Learning:** Even internal or admin-facing tools (like an email editor) are susceptible to DOM-based XSS if user input is rendered into critical attributes like `href`. Simple HTML escaping (`escapeHtml` / `escapeAttr`) is insufficient for URLs.
**Prevention:** Ensure that a `sanitizeUrl` function (which explicitly blocks `javascript:` and `data:` schemes) is defined and applied to all user-controlled URLs before they are passed into `escapeAttr()` for insertion into HTML templates.

## 2026-05-25 - [Removed sanitizeUrl on img src]
**Vulnerability:** The application incorrectly used `sanitizeUrl` on `img src` attributes in `js/news.js`. While intended to prevent injection, `sanitizeUrl` explicitly strips `data:` URIs, which breaks legitimate base64-encoded images.
**Learning:** Security functions must be applied only to their intended context. `sanitizeUrl` is designed to prevent `javascript:` and malicious `data:` scheme execution in contexts where they can execute (like `href` or `form action`). Browsers do not execute `javascript:` URIs in `<img> src` attributes, and blocking `data:` URIs unnecessarily breaks image rendering.
**Prevention:** Removed `sanitizeUrl` from `<img src="...">` interpolations in `js/news.js`. Always verify the security context before applying a sanitization function to avoid breaking intended functionality.

## 2026-06-01 - Fix Selector Injection
**Vulnerability:** User-controlled URL parameter `targetId` was used directly in `document.querySelector()` without being escaped in `test-pages/annotated-page.html`.
**Learning:** Constructing CSS selectors using unescaped user input can lead to Selector Injection. Attackers can inject arbitrary selectors or execute Client-Side Denial of Service (DoS) by providing excessively complex or malformed inputs, which could break the JavaScript execution.
**Prevention:** Always sanitize and escape user-controlled data using `CSS.escape()` before interpolating it into a CSS selector string.

## 2026-06-05 - [Fix Reverse Tabnabbing Vulnerability]
**Vulnerability:** Instances of  were found missing the  attribute, leaving the application susceptible to reverse tabnabbing attacks.
**Learning:** Using  without proper  attributes can allow newly opened tabs to hijack the original tab's  object.
**Prevention:** Ensured  is added to all user-facing  anchor tags dynamically interpolated in client-side HTML.

## 2026-06-05 - [Fix Reverse Tabnabbing Vulnerability]
**Vulnerability:** Instances of target="_blank" were found missing the rel="noopener noreferrer" attribute, leaving the application susceptible to reverse tabnabbing attacks.
**Learning:** Using target="_blank" without proper rel attributes can allow newly opened tabs to hijack the original tab's window.opener object.
**Prevention:** Ensured rel="noopener noreferrer" is added to all user-facing target="_blank" anchor tags dynamically interpolated in client-side HTML.

## 2026-06-08 - Fix Selector Injection in events.html
**Vulnerability:** User-controlled data (the `dateStr` derived from user clicks on calendar elements, stored in `dataset.date`) was interpolated directly into CSS selectors within `document.querySelector` calls in `events.html`'s `highlightEvent` function.
**Learning:** Constructing CSS selectors using unescaped user input can lead to Selector Injection. This allows attackers to potentially inject arbitrary selectors or trigger Client-Side Denial of Service (DoS) by crafting complex inputs.
**Prevention:** Always sanitize and escape user-controlled data using `CSS.escape()` before interpolating it into a CSS selector string.

## 2026-07-09 - [DOM-based XSS via javascript: URIs in current-action.js]
**Vulnerability:** User-controlled URLs (like `cta.href`) were interpolated into the `href` attribute of CTA buttons in `js/current-action.js` via `element.setAttribute('href', safeText(cta.href || '#'))`. This does not sanitize the URL scheme, allowing `javascript:` or `data:` URIs to execute if the data source contains malicious links.
**Learning:** We continue to see the pattern where strings injected into critical attributes like `href` or `src` via JavaScript DOM manipulation (`setAttribute` or `.innerHTML`) are susceptible to XSS if not explicitly sanitized. Simply ensuring it's a string via `safeText` is insufficient.
**Prevention:** Always ensure a `sanitizeUrl` function is defined and applied to all user-controlled URLs before they are passed into `setAttribute('href', ...)` or interpolated into HTML string templates. I added the sanitization directly into `setCta` in `current-action.js`.
