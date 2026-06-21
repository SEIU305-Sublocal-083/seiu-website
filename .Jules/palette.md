# Palette Journal

Critical UX/accessibility learnings only.

## 2024-05-18 - [Add `inputmode="decimal"` to currency inputs]
**Learning:** `type="number"` inputs for currency or decimals (using `step="0.01"`) on mobile devices might show a standard number pad without a decimal point on some OS versions if `inputmode="decimal"` isn't specified.
**Action:** Always add `inputmode="decimal"` to `<input type="number" step="0.01">` when expecting currency or float values to ensure the correct numeric keypad with a decimal point is displayed for mobile users.
## 2024-05-18 - [Use type="search" for search inputs]\n**Learning:** Using `<input type="search">` instead of `<input type="text">` for search fields provides a better mobile experience by triggering the specialized native search keyboard and often adding a native clear button (x) in supported browsers, improving accessibility and usability without additional code.\n**Action:** Always prefer `type="search"` over `type="text"` for dedicated search input fields.
## 2024-05-18 - [Add `aria-label` to icon-only buttons]
**Learning:** Icon-only buttons (like image carousel controls or share buttons) that rely solely on `title` attributes or surrounding context are inaccessible to screen readers, leaving users unaware of the button's function.
**Action:** Always add descriptive `aria-label` attributes to `<button>` or `<a>` elements that do not contain visible text.
## 2024-05-18 - [Add `aria-pressed` to toggle buttons]
**Learning:** When using buttons as visual toggles (like category filters that turn a distinct color when active), screen reader users are unaware of which filter is currently active if relying solely on CSS classes (e.g., `class="active"`). Using the `aria-pressed` attribute correctly translates the visual state into semantic state for assistive technologies.
**Action:** Always add `aria-pressed="true"` to active toggle buttons and `aria-pressed="false"` to inactive ones, ensuring JavaScript updates this attribute synchronously with any visual class toggles.
## 2026-05-18 - [Add helpful empty states for filtered lists]
**Learning:** When users apply search filters that return zero results, a generic "no results" message leaves them stuck. A well-designed empty state with an actionable "Clear Filters" button significantly improves recovery and usability.
**Action:** Always include a helpful empty state with a clear call-to-action (e.g., a button to reset filters) for any search or filtering mechanism that can return zero results.
## 2026-05-18 - [Add visual and semantic loading states]
**Learning:** Plain text loading indicators (like "Loading...") can feel unresponsive and lack proper semantic meaning for assistive technologies. Replacing them with an animated visual spinner and a `role="status"` wrapper ensures both sighted and screen-reader users understand the system is processing information.
**Action:** Always use a visual indicator (like a spinner) accompanied by semantic `role="status"` and visually hidden text for asynchronous loading states.
## 2026-05-18 - [Add required indicators to critical inputs]
**Learning:** Users and screen readers need clear indicators for mandatory fields, even outside of traditional <form> submissions (e.g., calculator inputs). Relying on implicit requirement degrades UX and accessibility.
**Action:** Always add `required` and `aria-required="true"` attributes to essential <input> elements, and pair them with a visual indicator (like a red * with `aria-hidden="true"`) in the associated <label>.
