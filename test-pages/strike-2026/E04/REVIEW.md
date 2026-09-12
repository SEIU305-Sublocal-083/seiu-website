# E04: Tuesday Cascades and absentee targeted reminder

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: E04 email campaign draft; no send or schedule.
- English source: `copy/en/`. 2 alternative(s), each with its own preview.
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

# E04 — Tuesday targeted voting reminders

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for Tuesday, Sept. 15, 2026. Two separate targeted messages; do not combine into an all-member repeat. Sources: emails.md ER3 and E04; guides.md G02/H01. Do not build audience lists from ballot choices. Monday's request cutoff is past; no invitation to submit a new request or invented extension.

**Cascades branch:** The official indexed table's Obsidian 205, 11 a.m.–5 p.m. is a published-source candidate with no time zone and other conflicted rows. It requires organizer refresh. The complete interim email below offers confirmed day and a direct contact; it does not resolve venue/hour access planning. Hold a full travel instruction until date, venue, room, hours, time zone and access route are confirmed. Then replace the first two paragraphs with the confirmed details in both languages before human release review.

**Absentee branch:** Confirm the deadline time zone, accepted return method and missing-ballot escalation. Until then use the exact attributed deadline and the member's own ballot instructions below; do not add a time zone or share a personalized link. The member should contact the organizer promptly about nonreceipt; no second ballot assumed. Remove either branch when selecting the audience. No send is authorized.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
