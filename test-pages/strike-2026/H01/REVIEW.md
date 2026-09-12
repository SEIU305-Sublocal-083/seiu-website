# H01: How and where to vote and absentee ballots

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /strike/voting/ (proposed new guide).
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

# H01 — Voting guide

## Internal editorial notes — exclude from member copy

Round 4 brand/copy review completed Sept. 12, 2026, using the Round 3 checked draft. Source dates and publication conditions remain in force. Complete local draft only: agent bilingual review is not human bilingual, legal, institutional or publication approval. No fresh source verification is claimed in this round.

Source-stage record: Round 2 complete bilingual draft, prepared Sept. 12, 2026. Review only; no publication authorized. Sources: research G01–G03/G09 and emails ER1–ER3. Refresh every date-sensitive block before release and retire voting directions after Sept. 15. The confirmed daytime block can be released separately after review.

Release holds: evening venue/address/entrance conflicts among the organizer invitation, office directory and statewide table; do not publish any candidate address or map. Cascades table lists Sept. 15, Obsidian 205, 11 a.m.–5 p.m., with no time zone, but other table rows conflict; obtain event-owner confirmation before adding room/hours. Absentee time zone, return method/nonreceipt process and safe general link remain unverified. The member copy accurately attributes the two deadlines without adding a time zone. Confirm accessibility help and staffing without promising a response time. No personal absentee URL, private-mail evidence link or proposed /strike URL is included.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
