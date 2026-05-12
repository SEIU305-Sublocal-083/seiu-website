## 2024-04-30 - [Missing Lazy Loading] Learning: [Many images are missing `loading="lazy"` attribute, which causes all images to load synchronously and impacts page load time] Action: [Add `loading="lazy"` to `<img>` tags, except for those in the above-the-fold or hero section]

## 2024-05-18 - [Date Parsing in Render Loops]
**Learning:** [Calling `new Date()` and `toLocaleDateString()` inside mapping loops (e.g., `events.map`, `articles.forEach`) causes significant performance overhead and redundant calculations, especially on components that render frequently like the search-filtered news grid.]
**Action:** [Pre-parse date objects (e.g. `event.parsedDate`) and pre-format localized date strings (e.g. `article.formattedUpdatedAt`) immediately after JSON fetch, then reuse these cached values during DOM updates.]

## 2024-05-18 - [Missing Debounce on Render]
**Learning:** [Discovered a pattern where search input analytics were debounced, but the actual heavy DOM rendering and array filtering/sorting (`renderArticles`) was left synchronous on every keystroke, causing unnecessary main thread blocking.]
**Action:** [Always ensure that expensive rendering logic is included within the debounce timeout along with analytics when handling frequent input events.]

## 2024-05-18 - [DOM Layout Thrashing]
**Learning:** [Repeatedly appending to the DOM within loops (like `appendChild` in a `forEach` loop for news articles or tags) causes unnecessary layout recalculations and repaints, severely degrading rendering performance on large lists.]
**Action:** [Batch DOM updates using `innerHTML = array.map().join('')` for list rendering, or use a `DocumentFragment` to build complex nested elements in memory before appending to the live DOM once.]
