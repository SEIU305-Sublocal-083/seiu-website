## 2024-04-30 - [Missing Lazy Loading] Learning: [Many images are missing `loading="lazy"` attribute, which causes all images to load synchronously and impacts page load time] Action: [Add `loading="lazy"` to `<img>` tags, except for those in the above-the-fold or hero section]

## 2024-05-18 - [Date Parsing in Render Loops]
**Learning:** [Calling `new Date()` and `toLocaleDateString()` inside mapping loops (e.g., `events.map`, `articles.forEach`) causes significant performance overhead and redundant calculations, especially on components that render frequently like the search-filtered news grid.]
**Action:** [Pre-parse date objects (e.g. `event.parsedDate`) and pre-format localized date strings (e.g. `article.formattedUpdatedAt`) immediately after JSON fetch, then reuse these cached values during DOM updates.]

## 2024-05-18 - [Missing Debounce on Render]
**Learning:** [Discovered a pattern where search input analytics were debounced, but the actual heavy DOM rendering and array filtering/sorting (`renderArticles`) was left synchronous on every keystroke, causing unnecessary main thread blocking.]
**Action:** [Always ensure that expensive rendering logic is included within the debounce timeout along with analytics when handling frequent input events.]

## 2024-05-18 - [Incorrect Cross-Boundary Search Optimization]
**Learning:** [Attempting to optimize search performance by pre-calculating a single, concatenated string of multiple fields (e.g., \`${title} ${description}\`) introduces a bug where searches can incorrectly match across the boundary of the joined fields (e.g., matching the end of the title and the beginning of the description).]
**Action:** [When optimizing search filters, pre-calculate the lowercase string for each field individually (e.g., \`searchTitle\`, \`searchDescription\`) to maintain the exact semantic boundaries and behavior of the original unoptimized code.]

## 2026-05-16 - [DOM Layout Thrashing]
**Learning:** [Appending DOM elements individually within a loop (e.g., using `appendChild`) causes layout thrashing because the browser has to recalculate styles and layout for every element. This significantly impacts rendering performance.]
**Action:** [Batch DOM updates using `innerHTML` with a mapped array joined into a single string (e.g. `element.innerHTML = items.map().join('')`) or use a `DocumentFragment` when creating elements dynamically.]
