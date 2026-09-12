# E08: Monday Sept21 weekly update variants

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: E08 email campaign draft; no send or schedule.
- English source: `copy/en/`. 5 alternative(s), each with its own preview.
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

# E08 — Monday, Sept. 21 weekly next steps

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for Monday, Sept. 21, 2026. Audience: Local 083 members; match any official instruction's scope. Select one conditional editor template after a fresh status check. These are not assembled sendable messages. Sources: emails.md E08/ER3–ER6; guides.md H04–H07; web_organizing.md R07/N04. No future meeting recap, repeated Thursday meeting, support operation or outcome is assumed. Keep Monday's message to one phase-specific action.

**ASSEMBLY HOLD:** Each branch refers to a dated briefing accompanying the email. That future information does not exist in this draft and must be supplied as a verified, accessible bilingual block in the email body, after the matching language's action paragraph and before its sign-off. Give the as-of date/time/time zone, what changed, the actual current instruction, and a verified next action or explicitly unresolved next step. Check that every “below” / “abajo” reference points to the assembled block in the same language. Link a current public source only after it is approved and tested; use the established contact routes in the copy while proposed /strike remains unverified. This draft does not claim a briefing or hub is already published.

| Branch | Event/release conditions and required accompanying block |
| --- | --- |
| A — Bargaining continues, no official call | Authorized confirmation of continued bargaining and absence of a call; current proposal/change summary and verified next bargaining/member action, or explicit absence of a new scheduled action. A Sept. 11 historical summary is not a Sept. 21 status check. |
| B — Official call, preparation | Current written call; exact start date/time/time zone, scope, work/call-in instructions, actual preparation task/picket access, support route and next briefing if confirmed. Urgent work facts must be in the email, not solely behind a link. |
| C — Tentative agreement | Confirmed current TA and text; actual ratification process, eligibility, deadline/time zone and access if announced; explicit effect on any strike notice/call/work instructions. |
| D — Changed timeline | Dated superseded instruction and new date/time/time zone/scope; explicit work/picket/return effect and approved immediate action. |
| E — Strike continues longer than expected | Contingency for an actual later active strike, not a prediction about Sept. 21. Retitle/redate for actual use. Verify active status, what expectation changed, whether an end/return date is confirmed, continuing work/picket/return instructions and next briefing; refresh aid operations/amounts/eligibility, coverage cases and OED guidance. Use the no-confirmed-end-date sentence only if that remains true. No promise of end date or funding duration. |

For every branch, the current help status should distinguish confirmed support from unresolved program rules. H04/H05/H06/H07 are the canonical draft answer owners; do not summarize old live pages as newly reviewed guidance. Insert their later verified URLs only after separately authorized publication/readback, or include their reviewed relevant text in the briefing. No source consultation or personal case discussion authorizes a legal or financial guarantee. Human factual, institutional and bilingual approval is still required.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
