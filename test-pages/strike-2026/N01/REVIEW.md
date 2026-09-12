# N01: Strike hub launch news

**Draft PR only. No publication, email send or schedule.**

This is item 2 of 6 in the Website and news stack. Its base is `codex/strike-w01-open-strike-information-hub` (PR #280); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: /news/2026-09-13-strike-information-hub.html (proposed; launch-dependent).
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

# N01 — Hub launch news and usable fallback

## Editorial controls — not public copy

Prepared Sept. 12, 2026. Variant A is held for a future verified bilingual hub launch at the proposed `/strike` address. Confirm its actual destination, content, links, current status and accepted maintenance/cadence owners before release. As written, A is a pre-vote launch announcement: use before the Sept. 14 daytime vote, or rewrite its voting action and Sept. 17 meeting reference for the actual launch date and verified status. This file does not claim the hub is live. Variant B is complete pre-vote copy for use if the hub is not ready; use only before the Sept. 14 daytime vote and after fresh status review. It does not depend on launching anything. Both variants need a real publication date in the news metadata. Never publish both together. Source/date: Sept. 12 research web R01–R08 and email ER1–ER5. Human review remains outstanding.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
