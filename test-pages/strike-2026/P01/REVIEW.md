# P01: Voting poster copy

**Draft PR only. No publication, email send or schedule.**

This is item 4 of 6 in the Organizing materials stack. Its base is `codex/strike-a01-president-and-trustees-personalized-letter-starter` (PR #254); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: Print voting poster; no automatic distribution.
- English source: `copy/en/`. 1 alternative(s), each with its own preview.
- Spanish handoff: `copy/es/` and `title_es` in `item.json`; include `sources/es.md` only when citations are displayed. Human translation has not been supplied or approved.
- Full preview: `index.html`; alternatives: `a.en.html`, etc.
- Screenshots: `screenshots/`. These are captures of the rendered HTML.
- Citations: no citation section appears in this page. `sources/en.md` is retained for editorial reference; contact and action links remain in the body.

## Translator and reviewer steps

1. Translate the English alternative(s) that the editor intends to use; retain the other conditional drafts as alternatives.
2. Translate subject lines, preheaders, headings, tables, actions and captions/transcripts. Translate source notes only when `citations` is `collapsed`. Do not invent missing facts or remove qualifications.
3. Mark the variant `ready_for_review`. A bilingual reviewer records `approved`, their name and the SHA-256 of its current English file only after review. Fill `title_es`; record the source-note reviewer only when citations are displayed.
4. An editor selects exactly one variant, resolves the release conditions, and records current fact-check and approval fields. Selection never sends or publishes anything.
5. Run the preview builder, review both languages on desktop/mobile and refresh screenshots. `--release-check` intentionally fails until approvals and facts are complete.

## Item-specific editorial record

# P01 — Voting poster copy

## Editorial controls — not part of poster

Prepared Sept. 12, 2026. Complete bilingual **Corvallis daytime** poster text below; review/printing/posting not authorized by this file. Sources S01, ER1, G01/G03 and SOURCE-LEDGER's Sept. 12 verified membership-route addition. Round 3 independently reopened the application; the link does not establish election eligibility. Verify event/contact/membership links immediately before print. The readable non-QR route is the existing public `www.local083.org/events.html`, whose calendar links to the exact vote event. No unverified short URL. If a QR is later added, encode the verified daytime event URL and print the readable route beside it; never encode an absentee link. Supply this text with any artwork.

Design: two equally prominent language blocks, high contrast, large dates/times and venue; Inter body/Lora headline using established Local 083 assets. Do not shrink Spanish to fit. Print two posters if needed for readable type. Remove/replace this daytime poster after 5 p.m. Pacific Sept. 14. No poster artwork or rendered readability check has been completed. Check posting permission with the distributor.

Evening panel and Cascades poster remain held: exact evening destination conflicts, and Cascades table's room/hours are only a published candidate. Do not print either as travel instructions or silently substitute an address. The confirmed daytime poster can move to human review independently.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
