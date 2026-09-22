# Community support and picket logistics drafts

Prepared September 22, 2026. New drafts only; production navigation and sitemap unchanged. Both pages use noindex while under review.

Sources: user confirmed on September 22 that solidarity is the current ask while systems for a possible GoFundMe are being set up. User confirmed picketing outside Kerr Administration Building and requested a Google Maps embed. No fundraiser URL, launch date, shift times, exact outdoor gathering point or check-in procedure was supplied. OSU building listing confirms street address: https://events.oregonstate.edu/kerr_administration_bldg . Existing strike hub supplies executive-team/steward contacts and context.

Proposed content owner: executive team; reviewer: communications chair. Confirm shift times and check-in procedure before presenting this as a complete schedule. Review again before publication and whenever organizing instructions change.

Suggested production paths: /strike/community-support/ and /strike/picket-logistics/. On promotion update canonical/social/structured URLs and cross-links, remove draft banner and noindex, add useful links from /strike/, then run the complete publication checks from DRAFTING_WORKFLOW.md. Do not add Event markup without confirmed dates/times. No payments are collected.

Validation: Chromium desktop (1440px) and mobile (390px), one h1 per page, no horizontal overflow, internal page links resolve, draft robots metadata retained. Screenshots alongside this note. Google Maps uses a titled responsive iframe and a separate directions link.

Layout revision: added scoped styles/strike-companion.css for both drafts. Removed the unused desktop hero column, widened the card rows, reduced section spacing and heading sizes, added section dividers and filled primary buttons, and stacked actions on mobile. Rechecked 390px and 1440px layouts and internal links; no horizontal overflow. Refreshed screenshots.

Action revision: both pages now share one reading-column width and use the canonical header/footer renderer (exact region comparison passed). “I want to help” opens an editable mailto to 083execteam@seiu503.org, cc sharpes@seiu503.org, with prompts for name, affiliation, offer, availability and contact information. Sylv address source: marketing/email/2026-09-18-Strike-Declared-Draft.html and 2026-09-10-OSU-Strike-Authorization-Vote-Draft.html. No email sent.

Added personalized leadership-message draft and official President Murthy contact form: https://leadership.oregonstate.edu/webform/contact-presidents-office (verified September 22). A direct president email could not be confirmed; user asked for preferred address. Message expresses the sender's position and asks for action on a fair contract. Buttons return to /strike/. Chromium checks at 390, 768 and 1440 passed: email recipients/body, editable message, mobile menu open/Escape close, one h1 and no horizontal overflow.

## Leadership action revision, September 22

Replaced the visible message textarea with a single email action and a collapsed help section. Verified live mailto links through Chromium on OSU's published contact pages: pres.office@oregonstate.edu (President Murthy trustee biography) and trustees@oregonstate.edu (board contact page). Those two offices are the recipients; individual trustees are not added separately.

Three subagents drafted 10 messages each; all 30 were revised and reviewed as neutral factual inquiries. Each asks about one issue identified in the September 18 strike notice and a relevant OSU strategic objective, with two source links in the body. No personal affiliations, personal harms or fill-in prompts are asserted. The sender can edit the draft naturally in their email app. The advocacy/blame framing was not expanded into targeted persuasion messages.

Sources for subject matter:
- https://www.local083.org/news/2026-09-18-osu-strike-notice-delivered.html
- https://leadership.oregonstate.edu/strategic-plan/three-goals
- https://leadership.oregonstate.edu/strategic-plan/implementation

Drafts are stored in data/leadership-email-drafts.json; js/leadership-email.js selects from a shuffled queue on a user click. The queue contains draft IDs only, in browser local storage, shared across both pages. No personal content or email-send status is stored. All 30 drafts are used before the cycle resets, avoiding immediate repetition across the boundary. Separate browsers, cleared storage, simultaneous tabs and the static fallback can still repeat a draft; site-wide uniqueness is not claimed. If storage is blocked, rotation continues in memory for that page; if JavaScript/data is unavailable, the button retains one complete mailto draft.

Both pages retain the canonical header/footer, strike return links, the executive-team/Sylv help email, and draft noindex status. The help email now also uses complete prose without blanks. Review issue status after the next bargaining update before publication.

Verification: node tests/test_leadership_email.cjs covers 30 unique complete drafts, three rotation cycles, malformed saved-state recovery, both recipients and full text encoding. Browser checks cover both-page rotation, no visible textarea, no fill-in prompts, mobile menu and overflow, failed data fetch, and blocked local storage. No email was sent during testing.


## Public review release

Prepared on isolated branch codex/community-picket-review from origin/main 76ab663. Homepage and strike review copies were refreshed from that published revision. The four /test-pages/ URLs are publicly viewable review pages, with noindex metadata and exclusion from the sitemap. Live homepage and strike entry points are unchanged.

Marketing/copy follow-up: see [MARKETING-REVISIONS.md](MARKETING-REVISIONS.md) for the applied copy and hierarchy changes, browser QA, and separate inherited homepage follow-ups. The email action on the picket guide is now secondary and collapsed by default. Updated screenshots reflect this revision.
