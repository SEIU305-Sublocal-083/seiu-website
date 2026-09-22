# Marketing and copy review revisions — September 22, 2026

Status: revised public review drafts, awaiting final brand/content signoff. These changes do not promote the pages into live homepage or strike navigation.

## Applied to the review pages

- Community support: changed the primary action to “Email our team to offer help”; identified SEIU Local 503 internal field organizer Sylv Sharpe and disclosed that Sylv is copied on the executive-team email. Role source: September 18 strike-notice report, source note. Shortened fundraising copy and kept the current actions first. Introduced the leadership inquiry section with the union's stated aim of a fair agreement. Email variants remain factual inquiries.
- Picket preparation: changed the headline and metadata to “Prepare for OSU picketing.” Added an immediate status notice distinguishing this preparation resource from assigned shifts. Made “Email for picket instructions” the primary action, with a complete editable request to the executive team and Sylv. Consolidated assignment instructions and retained the map, access/transport planning, outdoor checklist and arrival guidance. Moved the secondary leadership email action into a keyboard-operable disclosure.
- Both card previews: replaced “Join us outside Kerr” with “Prepare to picket,” and replaced organizer shorthand with concrete ways to share updates and offer practical help.
- Strike preview: added the preparation/map link to the picketing FAQ while retaining the email route for individual instructions. Changed the household-assistance link to “Find food and housing assistance.” Spelled out “97 percent” in FAQ prose; retained compact timeline formatting.
- Titles: used the resource-page suffix “- SEIU Local 503, OSU.” Updated descriptions, social titles/descriptions and WebPage structured data to match. Kept noindex, review canonicals and test-pages links.

## Visual and interaction verification

Chromium checks at 390, 768 and 1440 pixels: one main heading, no horizontal overflow, Lora heading/Inter body fonts on the two resource pages, primary-action contrast at least 4.5:1, visible focus outline, mobile menu open/Escape close, keyboard disclosure operation, correct executive-team/Sylv recipients, updated titles and review metadata. Inspected refreshed screenshots with map and footer logo loaded.

Leadership mailto checks: both office recipients, complete editable content, all 30 variants across the two pages, blocked storage and failed-data fallbacks. Browser tests intercept mailto navigation; no message was sent and no installed external mail client was exercised.

Countdown checked in a JavaScript-enabled browser at September 22, 2026: timer renders nonzero time and changes after one second. After the intended start, the timer hides and directs readers to current status without asserting that a strike began. The all-zero static retrieval is not evidence of a running countdown defect.

Build drift check, Node email tests and public quality, accessibility, link and shell audits passed. Public audits exclude test-pages; the browser and focused content checks cover the four changed drafts. This is a scoped browser QA pass, not a complete assistive-technology or visual-accessibility certification.

## Separate inherited homepage follow-up

The reviewers explicitly separated these issues from approval of the new cards. No live-homepage change was made in this revision.

1. Replace “Read about it” with “Read our strike notice” in the active strike-notice action in data/current-action.json, then regenerate the static homepage. Changing only HTML would be overwritten by the runtime action data.
2. Expand cost-of-living adjustment (COLA) on first use and Contract Action Team (CAT) before abbreviating in current homepage content; inspect generated and runtime paths together.
3. Refresh the static upcoming-event fallback. The review HTML still contains September 14 and September 16 listings. In a JavaScript-enabled September 22 browser, the same preview correctly replaces these with the October 6 Code of Conduct 101 event. This narrows the reported problem to stale initial/fallback content, not the successfully loaded feed. Verify the no-JavaScript and failed-fetch cases when repairing the generator/fallback.

On final publication, replace test-pages links with final destinations and verify canonical/social/schema URLs and the sitemap. Current review routes remain unchanged for the reviewers.
