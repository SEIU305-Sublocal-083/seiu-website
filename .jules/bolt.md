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

## 2024-05-18 - [Intl.DateTimeFormat Instantiation Overhead]
**Learning:** [While pre-computing date strings (`toLocaleDateString()`) outside of rendering loops is good, calling `toLocaleString()` repeatedly is still surprisingly slow because it implicitly instantiates a new `Intl.DateTimeFormat` object each time under the hood. Local benchmarking showed caching the formatter makes formatting ~400x faster.]
**Action:** [When formatting many dates, always instantiate `new Intl.DateTimeFormat(...)` once and cache it, then call `formatter.format(date)` instead of relying on `date.toLocaleDateString(...)` or `date.toLocaleString(...)`.]

## 2026-05-18 - [Premature Date Formatting]
**Learning:** [Applying expensive operations like `Intl.DateTimeFormat` across an entire dataset (e.g. hundreds of items) before filtering and slicing it down to the handful of items that will actually be rendered is a significant performance anti-pattern. This wastes CPU and memory on data that the user will never see.]
**Action:** [Always perform filtering, sorting, and slicing first, and only apply expensive formatting or data transformations to the minimal subset of data that will be rendered.]

## 2024-05-18 - [Premature Date Parsing for Filtering]
**Learning:** [Instantiating `new Date()` for every item in a large dataset (e.g., hundreds of JSON events) just to filter by "upcoming" or "past" dates is an extremely slow performance anti-pattern. Because ISO-8601 dates (YYYY-MM-DD) are lexicographically sortable, direct string comparison (e.g. `event.date >= todayString`) achieves the same result ~50x faster.]
**Action:** [Filter date strings directly using string comparison first, and defer instantiating `new Date()` only for the remaining slice of items that actually need advanced manipulation or formatting for display.]

## 2024-05-18 - [Redundant Array Sorting]
**Learning:** [Calling `.sort()` on an array that is already sorted, or can be trivially reversed, is a waste of O(n log n) operations. JavaScript's `.filter()` method preserves the original array order. If the source data is pre-sorted, the filtered result remains sorted in that same order.]
**Action:** [Skip sorting entirely if the data is already in the desired order (e.g., "newest first"). If the opposite order is needed (e.g., "oldest first"), use the O(n) `.reverse()` method instead of re-evaluating the sort criteria.]

## 2024-05-18 - [RegExp Instantiation in Loops]
**Learning:** [Instantiating `new RegExp()` inside rendering loops (like `Array.prototype.map()`) when the pattern is constant causes redundant pattern compilation and object creation on every iteration, harming performance. Furthermore, it's safe to hoist global RegExp instances (e.g., with the 'g' or 'gi' flag) outside of rendering loops and reuse them with `String.prototype.replace()`, because `replace()` automatically ignores and resets the regex's `lastIndex` property, preventing state leakage across loop iterations.]
**Action:** [Always hoist `new RegExp()` instantiations outside the loop when the pattern (such as a search query) remains constant.]
## 2024-05-18 - [Optimizing Date Grouping with Substrings]
**Learning:** [Instantiating `new Date()` and applying `Intl.DateTimeFormat` across an entire dataset just to group items by month/year is an O(N) performance bottleneck. Because ISO-8601 dates (YYYY-MM-DD) contain the grouping information inherently, extracting the group key via a substring (e.g., `date.substring(0, 7)`) avoids parsing dates altogether.]
**Action:** [To optimize date grouping loops, extract grouping keys via substring. Then format the key once per group (O(1)) and extract specific date components (like the day) directly using substrings (e.g., `parseInt(date.substring(8, 10), 10)`) to avoid the overhead of `Date` instantiation and formatting within inner loops.]
