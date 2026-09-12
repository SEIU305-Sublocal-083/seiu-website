# E01: Saturday targeted voting clarification

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: E01 email campaign draft; no send or schedule.
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

# E01 — Saturday targeted voting clarification

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12, 2026. Audience: members who missed Friday's information, were excluded from Zoom, or received the earlier pledge-restricted invitation. Trigger: a demonstrated clarification need on Saturday, Sept. 12; no automatic all-member send. Primary action: make a voting plan.

Sources: emails.md ER1–ER3, ER5; guides.md G01; SOURCE-LEDGER.md S01–S03. Confirmed daytime core is available for review now. Evening time is supported, but invitation, office directory and indexed statewide table disagree on destination. No address or map may be added without organizer confirmation. This draft uses direct confirmation before travel. A pledge is not required to receive the evening invitation; do not equate that with verified personal ballot eligibility. Help email is verified; response time/weekend staffing is not. All publication and sending remain held for human approval.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. No AI-generated artwork or unreviewed machine Spanish is included in this PR.
