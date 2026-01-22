# Sentinel's Journal

## 2025-10-22 - Stored XSS in News Page
**Vulnerability:** The news page (`news.html` and `js/news.js`) fetched `news.json` and injected its content (title, description, tags, author info) directly into the DOM using `innerHTML` without sanitization. This allowed stored XSS if the JSON file contained malicious scripts.
**Learning:** Even in static sites with local data files, "Defense in Depth" requires treating data sources as untrusted, especially when they drive HTML generation. The vulnerability was duplicated in an inline script and an external script, highlighting the risk of redundant code.
**Prevention:** Always sanitize data before injecting into HTML. Use `textContent` where possible, or a sanitizer/escape function when constructing HTML strings.
