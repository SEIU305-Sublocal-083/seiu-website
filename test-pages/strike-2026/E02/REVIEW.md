# E02: Sunday before-you-vote email

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: E02 email campaign draft; no send or schedule.
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

# E02 — Sunday before-you-vote email

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for Sunday, Sept. 13, 2026. Audience: Local 083 members and relevant coworkers receiving membership information. Trigger: approved preparation message before Monday voting. Primary action: choose a voting method and time.

Sources: emails.md ER1–ER5; guides.md H01–H03; web_organizing.md R07. Refresh proposals and logistics before release. The complete core below deliberately uses the published absentee times as an attributed quotation in substance, expressly identifying the missing time zone and urging action before the cutoff. Never add Pacific to those deadlines without verification. The request link stays in each reader's own Friday message. Evening address and Cascades venue/hours remain held. The confirmed MU block does not depend on resolving these holds. Ballot rules, joining cutoff, paid-time arrangements and individual benefit promises are not verified. No live-hub claim; current event link is the fallback. Human approval of content, both languages, audience and help coverage is still required.

Cadence and website sentences are the user-requested proposed communications promise; confirm an editor accepts the schedule and responsibility for reviewed website answers before release. The direct membership application was independently checked Sept. 12 at https://seiu503signup.org/ and is linked from Local 083's contact page; signing/submitting, processing and eligibility are separate matters. No voting cutoff or immediate eligibility is established by that form. Future link replacement: only after separately authorized launch and bilingual public readback, replace the daytime-event/contact destinations as appropriate with the verified local083.org/strike front door. Do not advertise the proposed hub beforehand.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
