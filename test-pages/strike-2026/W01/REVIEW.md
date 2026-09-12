# W01: Open strike information hub

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /strike/ (proposed hub; not live).
- English source: `copy/en/`. 9 alternative(s), each with its own preview.
- Spanish handoff: `copy/es/`, `sources/es.md` and `title_es` in `item.json`. Human translation has not been supplied or approved.
- Full preview: `index.html`; alternatives: `a.en.html`, etc.
- Screenshots: `screenshots/`. These are captures of the rendered HTML.
- Visible citations: `sources/en.md` renders beneath the body in each preview. Inline supporting links stay in the copy.

## Translator and reviewer steps

1. Translate the English alternative(s) that the editor intends to use; retain the other conditional drafts as alternatives.
2. Translate subject lines, preheaders, headings, tables, actions, captions/transcripts and source notes. Do not invent missing facts or remove qualifications.
3. Mark the variant `ready_for_review`. A bilingual reviewer records `approved`, their name and the SHA-256 of its current English file only after review. Fill `title_es` and the source-note reviewer.
4. An editor selects exactly one variant, resolves the release conditions, and records current fact-check and approval fields. Selection never sends or publishes anything.
5. Run the preview builder, review both languages on desktop/mobile and refresh screenshots. `--release-check` intentionally fails until approvals and facts are complete.

## Item-specific editorial record

# W01 — Open strike information hub

## Editorial controls — not public copy

Draft prepared Sept. 12, 2026. Proposed destination: `https://www.local083.org/strike`; no page launch or route verification is claimed. Local review only. English and Spanish below are the complete initial page copy. Use actual publication/review timestamps at release, with the status owner and next review time recorded internally. Existing guides are reuse candidates requiring reconciliation; do not imply their July claims are newly approved. The initial copy below answers priority questions directly and uses verified event/contact/official-agency fallbacks. When H01–H07/Q01 have approved live destinations in both languages, attach their descriptive links to the matching sections. No invented paths.

Sources: SOURCE-LEDGER S01–S07 and the Sept. 12 verified membership-route addition; research web R01–R08; email ER1–ER4; guides G03–G09, checked Sept. 12. Round 3 independently reopened the membership application and confirmed the signature/submission instruction; this does not establish election eligibility. Preserve evening destination conflict, Cascades candidate and missing absentee time zone. The evening information is organizer-announced time only, with direct destination confirmation before travel. Hold maps and exact evening venue until reconciled. Human approval and language review remain required.

**Round 4 status:** Complete bilingual draft for human review. Initial launch and unresolved logistics remain held; all future status options remain HOLD until their actual fact panel is assembled. Copy review is not institutional, legal or human Spanish approval.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
