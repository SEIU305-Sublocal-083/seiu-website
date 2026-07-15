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
## 2026-06-11 - [Add empty state for initial search screen]
**Learning:** Initial search screens often present users with a blank slate that can feel uninviting or confusing. A plain text prompt like "Type to search" lacks visual hierarchy and polish.
**Action:** Replace plain text search prompts with a visually distinct empty state component. This should include a relevant icon (like a magnifying glass or search symbol), a clear, bold heading ("Search the site"), and supportive descriptive text guiding the user on what they can search for. This reduces cognitive load and makes the search interface feel more approachable and professional.
## 2026-05-18 - [Add required indicators to critical inputs]
**Learning:** Users and screen readers need clear indicators for mandatory fields, even outside of traditional <form> submissions (e.g., calculator inputs). Relying on implicit requirement degrades UX and accessibility.
**Action:** Always add `required` and `aria-required="true"` attributes to essential <input> elements, and pair them with a visual indicator (like a red * with `aria-hidden="true"`) in the associated <label>.
## 2026-07-14 - [Add clear button to empty states]
**Learning:** When dynamically generating empty UI states for lists/searches (like the resource library), providing an actionable button (e.g., "Clear Search & Filters") directly inside the empty state allows users to quickly reset their context without needing to hunt for the original controls. Coupling this with `role="status"` ensures screen readers announce the empty result.
**Action:** Always include a reset button and `role="status"` on dynamically rendered empty states for filtered lists to improve recovery and accessibility.
## 2026-07-15 - [Visually distinctive empty states]
**Learning:** Using generic plain text for empty UI states (like zero search results or empty lists) is poor UX. Replacing them with a visually distinct component comprising an SVG icon, descriptive text, and a clear call-to-action button, while also adding the ARIA `role="status"`, improves both user recovery and screen reader accessibility.
**Action:** Always prefer rich, accessible empty state components with clear actions over plain text.
