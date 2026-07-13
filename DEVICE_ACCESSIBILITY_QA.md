# Device and accessibility QA matrix

Use the deployed preview URL. Record browser/OS versions and attach screenshots for failures and fixes. Test at least the homepage, About, Events, News, Resources, Leadership, Contact and Bargaining pages.

## Device matrix

| Device/browser | Width/orientation | Menu | Ticker/scroll regions | Calendar month/agenda | Accordions | Forms/links | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| iPhone Safari | Portrait and landscape |  |  |  |  |  |  |
| Android Chrome | Portrait and landscape |  |  |  |  |  |  |
| iPad/tablet Safari | Portrait and landscape |  |  |  |  |  |  |
| Desktop Safari | 1280px and wider |  |  |  |  |  |  |
| Desktop Chrome | 1280px and wider |  |  |  |  |  |  |
| Desktop Firefox | 1280px and wider |  |  |  |  |  |  |

Verify there is no page-level horizontal overflow. Deliberately scroll the job ticker, Latest stories panel, calendar and any card rails. Confirm nested scrolling is discoverable and does not trap touch or keyboard input.

## Keyboard-only sequence

1. Start at the address bar and press Tab through the page without using a pointer.
2. Activate the skip link and verify focus lands at main content.
3. Open and close the mobile menu with Enter and Space; confirm Escape closes it and focus returns to the menu button.
4. Operate calendar controls, topic/view toggles, search, accordions and privacy controls.
5. Confirm focus is always visible and follows visual order.
6. Confirm no keyboard trap exists in a horizontal or nested scrolling region.

## VoiceOver

With Safari and macOS/iOS VoiceOver:

- Navigate by landmarks and headings; confirm the page outline is meaningful.
- Navigate links, buttons, form fields and accordions; confirm names and expanded states.
- Confirm decorative marks and duplicate card links do not add noise.
- Confirm image alternatives identify the action or event without naming the child in rally photographs.
- Confirm status changes, errors and result counts are announced where relevant.

## Zoom and reflow

At 200%, 300% and 400% browser zoom, verify content reflows without two-dimensional page scrolling at a 1280px desktop viewport. Text must not overlap, clip or become inaccessible. Pay particular attention to navigation, event calendar controls, news filters, leadership cards and long bargaining headings.

## User preferences

- Enable Reduce Motion and confirm tickers stop or become manually scrollable, smooth scrolling is removed and content remains available.
- Enable increased contrast/forced colors and confirm focus, controls, links and selected states remain distinguishable without relying on background color alone.
- Disable JavaScript and confirm the no-script navigation and server-rendered content remain usable.
- Throttle to a slow connection and block analytics/font domains; confirm the site stays readable and interactive.

## Acceptance

No critical task may depend on hover, color alone, precise touch movement, motion, JavaScript-loaded text or a third-party request. Record defects with page, device, exact reproduction steps, severity, owner and retest result.
