# P02: Before-you-vote handout

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: Print member handout; no automatic distribution.
- English source: `copy/en/`. 1 alternative(s), each with its own preview.
- Spanish handoff: `copy/es/`, `sources/es.md` and `title_es` in `item.json`. Human translation has not been supplied or approved.
- Full preview: `index.html`; alternatives: `a.en.html`, etc.
- Screenshots: `screenshots/`. These are captures of the rendered HTML, not generated illustrations.
- Visible citations: `sources/en.md` renders beneath the body in each preview. Inline supporting links stay in the copy.

## Translator and reviewer steps

1. Translate the English alternative(s) that the editor intends to use; retain the other conditional drafts as alternatives.
2. Translate subject lines, preheaders, headings, tables, actions, captions/transcripts and source notes. Do not invent missing facts or remove qualifications.
3. Mark the variant `ready_for_review`. A bilingual reviewer records `approved`, their name and the SHA-256 of its current English file only after review. Fill `title_es` and the source-note reviewer.
4. An editor selects exactly one variant, resolves the release conditions, and records current fact-check and approval fields. Selection never sends or publishes anything.
5. Run the preview builder, review both languages on desktop/mobile and refresh screenshots. `--release-check` intentionally fails until approvals and facts are complete.

## Item-specific editorial record

# P02 — Before-you-vote handout

## Editorial controls — not handout text

Prepared Sept. 12, 2026. Complete English and Spanish handout copy; suggested front/back, one language per side, or two large-print sheets. Do not force small type to meet a one-sheet limit. Both languages travel together. Sources: S01–S04, ER1–ER5, G03/G04 and web R07. Confirm immediately before later distribution. Exact ballot, membership cutoff, threshold, paid-time rule, evening destination, Cascades room/hours and absentee zone remain unverified; copy gives useful interim routes. No QR required. The “my plan” area stays with the member; do not collect it or ballot choices. Attach longer H01–H07/Q01 only when approved and available; this handout does not invent their URLs.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. No AI-generated artwork or unreviewed machine Spanish is included in this PR.
