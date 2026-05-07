## 2024-04-30 - [Missing Lazy Loading] Learning: [Many images are missing `loading="lazy"` attribute, which causes all images to load synchronously and impacts page load time] Action: [Add `loading="lazy"` to `<img>` tags, except for those in the above-the-fold or hero section]

## 2024-05-18 - [Date Parsing in Render Loops]
**Learning:** [Calling `new Date()` and `toLocaleDateString()` inside mapping loops (e.g., `events.map`, `articles.forEach`) causes significant performance overhead and redundant calculations, especially on components that render frequently like the search-filtered news grid.]
**Action:** [Pre-parse date objects (e.g. `event.parsedDate`) and pre-format localized date strings (e.g. `article.formattedUpdatedAt`) immediately after JSON fetch, then reuse these cached values during DOM updates.]
