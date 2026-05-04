# Palette Journal

Critical UX/accessibility learnings only.

## 2024-05-18 - [Add `inputmode="decimal"` to currency inputs]
**Learning:** `type="number"` inputs for currency or decimals (using `step="0.01"`) on mobile devices might show a standard number pad without a decimal point on some OS versions if `inputmode="decimal"` isn't specified.
**Action:** Always add `inputmode="decimal"` to `<input type="number" step="0.01">` when expecting currency or float values to ensure the correct numeric keypad with a decimal point is displayed for mobile users.
## 2024-05-18 - [Use type="search" for search inputs]\n**Learning:** Using `<input type="search">` instead of `<input type="text">` for search fields provides a better mobile experience by triggering the specialized native search keyboard and often adding a native clear button (x) in supported browsers, improving accessibility and usability without additional code.\n**Action:** Always prefer `type="search"` over `type="text"` for dedicated search input fields.
