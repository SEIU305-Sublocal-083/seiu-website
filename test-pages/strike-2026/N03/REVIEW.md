# N03: September17 membership meeting recap template

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: /news/2026-09-17-membership-meeting-recap.html (proposed; checked notes required).
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

# N03 — Sept. 17 meeting recap editor template

## Editorial controls — not public copy

Prepared Sept. 12, 2026. The Sept. 17 meeting is future. No attendance, discussion, answer, decision, recording or technical repair is asserted by this draft. The meeting currently listed is Thursday, Sept. 17, noon–1 p.m. Pacific, Memorial Union room 211 or Zoom; sources S04 and ER4. This is a complete assembly template with reusable public prose and explicit factual panels, not an already-written account of a future event. Do not release it as a recap until a responsible participant has checked the actual record and every panel below is complete in both languages.

## Editor's factual panels — complete outside public prose, then insert

| Position in final article | Required actual content and review | Spanish parity check |
|---|---|---|
| Below headline | Actual publication date/time; meeting date and whether it occurred as planned; named internal fact approver. Publicly identify the source as the verified meeting record, with an approved link if one exists. | Date and meeting status match. Do not translate scheduled as held. |
| Under “What members need to know” | Two to four short actual takeaways. Begin with any action-changing fact: official vote/bargaining status, exact applicable instruction, deadline. Identify source date and authority for any result or work instruction. Do not certify a vote from meeting recollection. | Same action, scope, dates, times and conditions. |
| Under “Decisions and next steps” | Each real decision: what was decided, by whom, whether adopted or proposed, who it affects, and the next action. If no decision requiring member action was recorded, say so only if the participant confirms that. Never turn questions or suggestions into decisions. | Match “proposed,” “approved,” “pending” and authority. |
| Under “Answers and open questions” | Each general question, the actual reviewed answer or “An answer has not been verified in the sources checked,” source/review date, and contact route. Include any accepted next-update commitment. Redact personal cases and names. | Preserve uncertainty; do not shorten away conditions. |
| Before closing help paragraph | One primary next member action with a verified working destination. Use the existing contact page if no new event or action has been confirmed. | Same action and usable destination; do not invent Spanish routes. |

For an optional recording: verify existence, sharing consent, privacy edits, captions, transcript and both-language written access. Add a descriptive recording link only after that check. Omit all recording references if unavailable; do not promise a replay. The written takeaway panels are required either way.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
