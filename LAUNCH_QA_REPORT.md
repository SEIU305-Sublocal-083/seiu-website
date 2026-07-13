# Launch QA report

Reviewed July 12, 2026 on branch `codex/dynamic-homepage-concept`.

## Automated checks passed

- Public-page quality audit: titles, descriptions, canonical metadata, scheduled-content rules and placeholder checks pass.
- Accessibility structure audit: 96 pages, 0 errors and 0 warnings. The audit covers language, viewport, page landmarks, one H1, skip links, IDs and ARIA references, image alternatives and dimensions, form labels, button names and external-link safety.
- Local runtime crawl: 103 sitemap URLs and core assets returned a successful or intentional redirect response.
- Link/action audit: 108 public pages and 3,763 references passed. This includes internal files and fragments, PDF signatures, calendar-file structure, mail recipients and safe external new-window links.
- Official replacement links were verified for Corvallis City Council, Oregon BOLI discrimination and retaliation guidance, and Oregon's legislator lookup.
- CSS is compiled locally and reproducible in CI. Public pages no longer load the Tailwind browser compiler or Google Fonts.
- RSS and sitemap generation exclude the July 13 rally story until its Oregon-time publication date.
- Analytics respects opt-out state, Do Not Track and Global Privacy Control; session recording and autocapture are disabled.
- JavaScript syntax, XML parsing and repository whitespace checks pass.

## Accessibility and resilience implemented

- Reduced-motion, increased-contrast and forced-colors support is included globally.
- Primary pages include a no-JavaScript navigation fallback.
- Homepage events and news retain server-rendered fallback content if JSON loading fails.
- Images include alternatives and intrinsic dimensions; major imagery uses responsive sources.
- Privacy controls and a plain-language privacy notice are available in the footer.

## Must be completed by a person or in hosting

1. Test keyboard-only navigation, visible focus, 200% and 400% zoom, VoiceOver, reduced motion and forced colors in a rendered browser.
2. Test current iPhone/Android and desktop Safari, Chrome and Firefox layouts.
3. Run Lighthouse or WebPageTest on deployed HTTPS and record LCP, CLS and INP.
4. Validate Article/Event structured data with Google's Rich Results Test and inspect social cards in the intended publishing tools.
5. Apply and verify the response headers in `SECURITY_HEADERS.md`, including CSP report-only monitoring before enforcement.
6. On July 13 after midnight Pacific time, run or confirm the scheduled-news workflow and verify the rally story appears in News, RSS and the sitemap exactly once.
7. Obtain leadership signoff on officer titles. Current source material conflicts on the vice president and membership coordinator roles.
8. Confirm July 16 Zoom details and July 20 time, location, remote-access details and calendar file, or explicitly approve publication as “details coming soon.”
9. Archive the source file supporting the 1,454 workers / 36 counties figures.
10. Conduct the role-based tasks in `STAKEHOLDER_WALKTHROUGH.md` and record all four signoffs.

The unresolved factual items and responsible roles are listed in `CONTENT_SIGNOFF.md`.

## Release recommendation

The repository is ready for stakeholder and rendered-browser review, but it should not be called fully launch-approved until the human confirmations, production headers, browser/device checks and July 13 publication verification above are complete.
