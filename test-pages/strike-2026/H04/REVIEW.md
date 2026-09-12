# H04: Strike pay hardship unemployment and back pay

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /resources/strike-pay-benefits.html (update existing guide after review).
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

# H04 — Money and household planning

## Internal editorial notes — exclude from member copy

Round 4 brand/copy review completed Sept. 12, 2026, using the Round 3 checked draft. Source dates and publication conditions remain in force. Complete local draft only: agent bilingual review is not human bilingual, legal, institutional or publication approval. No fresh source verification is claimed in this round.

Source-stage record: Round 2 complete bilingual draft, Sept. 12, 2026. Review only. Sources: G04/G09 and H04 research. Writer refreshed OED's English strike guidance Sept. 12; same rules as research. No new strike-pay/hardship operating documents verified. Release holds for program amounts, eligibility, participation/accommodations, approved administrator, application/security, payment timing and staffed urgent escalation. The safe planning guide below does not advertise an operating assistance program. Obtain OED-specific reporting advice for union payments; do not infer exclusion from earnings. Refresh weekly OED work-search requirements before later reuse. Do not label paycheck wages, retroactive rates and strike-lost-wage compensation with one undifferentiated “back pay” label. Agent checking is not financial-program approval or individual claim determination.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. No AI-generated artwork or unreviewed machine Spanish is included in this PR.
