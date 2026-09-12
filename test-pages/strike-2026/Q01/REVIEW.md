# Q01: Common and complex questions index

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /strike/questions/ (proposed Q&A page).
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

# Q01 — Member questions index

## Internal editorial notes — exclude from member copy

Round 4 brand/copy review completed Sept. 12, 2026, using the Round 3 checked draft. Source dates and publication conditions remain in force. Complete local draft only: agent bilingual review is not human bilingual, legal, institutional or publication approval. No fresh source verification is claimed in this round.

Source-stage record: Round 2 complete bilingual short-answer index, Sept. 12, 2026. Review only. Detail owners: voting logistics H01; ballot/eligibility H02; proposals H03; six money categories H04; coverage/leave H05; work duties H06; strike sequence/participation H07. Every answer below inherits the Sept. 12 checked date; group source and help links apply to its entries. Proposed guide paths are not live. Until separately authorized publication and link verification, the member copy uses official source/contact and event URLs, not guessed article URLs. After approved publication, add the actual canonical H01–H07 link to each matching group and update it together with the summary in both languages.

Retain all H01–H07 holds. In particular, no evening address/map; Cascades Obsidian 205/11 a.m.–5 p.m. remains an internal published candidate needing event-owner refresh; absentee time zone and personalized-link limits remain. This is a navigation layer, not an alternate place to improvise legal/benefit rules. Assign actual editor/backup before promising maintenance or urgent response. Agent language review does not constitute human bilingual approval. No private cases, documents or ballot choices belong on this public index.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
