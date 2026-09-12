# H06: Rights responsibilities and practical work questions

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /resources/strike-rights-oregon.html (update existing guide after review).
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

# H06 — Workplace questions and responsibilities

## Internal editorial notes — exclude from member copy

Round 4 brand/copy review completed Sept. 12, 2026, using the Round 3 checked draft. Source dates and publication conditions remain in force. Complete local draft only: agent bilingual review is not human bilingual, legal, institutional or publication approval. No fresh source verification is claimed in this round.

Source-stage record: Round 2 complete bilingual draft, Sept. 12, 2026. Review only. Sources: G05/G06/G09 and H06 research. General legal frame is Oregon public-sector law; do not substitute private-sector NLRA rules. This draft provides records/help steps, not a blanket legal opinion. Hold specific paid-time voting, overtime refusal, manager-response obligations, leave/time codes, payroll deadlines, call-in duties, property handling and start/return directions for union/legal and policy review. No workplace disruption authorized by this guide. Staffed confidential priority-case intake and response time remain unverified. No employee/student data export or public incident registry.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
