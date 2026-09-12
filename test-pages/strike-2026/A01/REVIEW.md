# A01: President and trustees personalized letter starter

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /strike/write-your-letter/ (proposed member action page; no letters sent).
- English source: `copy/en/`. 1 alternative(s), each with its own preview.
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

# A01 — Personalized letter starter to President Murthy and OSU trustees

## Internal editorial notes — do not distribute or send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding. **Release status: HOLD** for campaign approval, current recipient checks and each writer's own personalization and review.

Drafted Sept. 12, 2026. Audience: members who voluntarily choose to write university leadership; keep separate from essential ballot instructions. Primary action: draft and personally review a letter. Sources: emails.md ER3, ER7; guides.md H03. The ask below is proposed campaign copy requiring local/statewide approval and a fresh bargaining check before member distribution. No letter has been sent and no form may be submitted in this task.

Verified routing in ER7: President Jayathi Y. Murthy's official contact page leads to the Contact President's Office form. No president email is verified. The Board contact page provides its shared correspondence route; all trustees receive letters sent there. The linked public-comment PDF names trustees@oregonstate.edu, but use the current contact page and recheck before actual sending. This is general correspondence, not formal meeting public comment. Do not invent meeting deadlines. Seven-university bargaining means the ask is for OSU leadership's support and influence, not a claim OSU can settle alone.

The member-facing instructions below are separate from the letter text. No bracket placeholders, invented personal story or prefilled signature appear in the letter. The personal paragraph and signature must be added by the actual writer before any send. Do not send an unchanged mass letter. Human bilingual review remains outstanding.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
