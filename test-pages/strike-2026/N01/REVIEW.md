# N01: Strike hub launch news

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /news/2026-09-13-strike-information-hub.html (proposed; launch-dependent).
- English source: `copy/en/`. 2 alternative(s), each with its own preview.
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

# N01 — Hub launch news and usable fallback

## Editorial controls — not public copy

Prepared Sept. 12, 2026. Variant A is held for a future verified bilingual hub launch at the proposed `/strike` address. Confirm its actual destination, content, links, current status and accepted maintenance/cadence owners before release. As written, A is a pre-vote launch announcement: use before the Sept. 14 daytime vote, or rewrite its voting action and Sept. 17 meeting reference for the actual launch date and verified status. This file does not claim the hub is live. Variant B is complete pre-vote copy for use if the hub is not ready; use only before the Sept. 14 daytime vote and after fresh status review. It does not depend on launching anything. Both variants need a real publication date in the news metadata. Never publish both together. Source/date: Sept. 12 research web R01–R08 and email ER1–ER5. Human review remains outstanding.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. No AI-generated artwork or unreviewed machine Spanish is included in this PR.
