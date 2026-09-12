# H02: What the ballot means and membership eligibility

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /strike/authorization-and-membership/ (proposed new guide).
- English source: `copy/en/`. 1 alternative(s), each with its own preview.
- Spanish handoff: `copy/es/` and `title_es` in `item.json`; include `sources/es.md` only when citations are displayed. Human translation has not been supplied or approved.
- Full preview: `index.html`; alternatives: `a.en.html`, etc.
- Screenshots: `screenshots/`. These are captures of the rendered HTML.
- Citations: a closed-by-default “Sources and references” section renders `sources/en.md`. Keep consequential qualifications and practical help links in the body.

## Translator and reviewer steps

1. Translate the English alternative(s) that the editor intends to use; retain the other conditional drafts as alternatives.
2. Translate subject lines, preheaders, headings, tables, actions and captions/transcripts. Translate source notes only when `citations` is `collapsed`. Do not invent missing facts or remove qualifications.
3. Mark the variant `ready_for_review`. A bilingual reviewer records `approved`, their name and the SHA-256 of its current English file only after review. Fill `title_es`; record the source-note reviewer only when citations are displayed.
4. An editor selects exactly one variant, resolves the release conditions, and records current fact-check and approval fields. Selection never sends or publishes anything.
5. Run the preview builder, review both languages on desktop/mobile and refresh screenshots. `--release-check` intentionally fails until approvals and facts are complete.

## Item-specific editorial record

# H02 — Ballot meaning and eligibility

## Internal editorial notes — exclude from member copy

Round 4 brand/copy review completed Sept. 12, 2026, using the Round 3 checked draft. Source dates and publication conditions remain in force. Complete local draft only: agent bilingual review is not human bilingual, legal, institutional or publication approval. No fresh source verification is claimed in this round.

Source-stage record: Round 2 complete bilingual draft, Sept. 12, 2026. Review only. Sources: G03/G05/G06, original meeting as recorded in the research brief, ER2/ER3. Release holds on exact ballot, electorate and membership cutoff/verification, threshold and denominator, certifier, duration/end authority, personal participation consequences and any later-vote requirement. Do not equate an oral statement that people can join and vote with an instant-processing guarantee. No vote results are known in this draft. Operational duties require union review, not just this general explainer.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
