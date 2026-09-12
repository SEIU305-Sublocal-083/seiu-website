# N02: Certified vote result news variants

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: Dated /news/ article after the actual certified result or approved pending update.
- English source: `copy/en/`. 3 alternative(s), each with its own preview.
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

# N02 — Certified result and pending-result news

## Editorial controls — not public copy

Prepared Sept. 12, 2026. No certified result was verified in the sources checked. Three complete conditional templates follow, each with its own HOLD fact panel. None is a prediction or a release-ready result announcement. Use only the variant authenticated at release. Wednesday, Sept. 16, is a proposed publication opportunity, not a promised certification date. Source basis: research web N02, email ER3/ER5, guides G03/H02. Do not infer outcomes from pledges, attendance, email opens or conversations.

### Required factual panel, completed by the editor before release

Place this verified panel after the headline, before the prose, in both languages. These are editorial fields, not public placeholders: publication date/time/time zone; official certifying authority and written source link; certified outcome and bargaining-unit scope; certification date; any approved counts with their exact denominator; current official work instruction; next confirmed event or accepted update commitment. For the pending variant, replace certification fields with the election authority's verified status and the time of that check. Do not claim the authority issued a statement if the status is merely the editor's documented confirmation that none is available. Omit unsupported optional counts. A count without the governing threshold/denominator must not be interpreted. Verify a public official source or obtain an approved publishable statement; private Gmail is not a public citation.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
