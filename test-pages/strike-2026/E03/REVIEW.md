# E03: Monday weekly update and voting email

**Draft PR only. No publication, email send or schedule.**

This is item 3 of 8 in the Emails stack. Its base is `codex/strike-e02-sunday-before-you-vote-email` (PR #256); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: E03 email campaign draft; no send or schedule.
- English source: `copy/en/`. 1 alternative(s), each with its own preview.
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

# E03 — Monday weekly update and voting email

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for Monday, Sept. 14, 2026, before 7:30 a.m. Pacific. Audience: Local 083 members. Primary action: cast a strike authorization ballot. Source base: emails.md ER1–ER4; guides.md H01–H03. Refresh before release; change the opening if sent after voting begins and do not reuse after polls close. This is Monday's weekly message; no separate all-member weekly email is needed that day.

Release holds: evening destination; absentee time zone/approved general link; personal eligibility and paid-time instructions. Supported daytime core is usable independently. If unresolved, retain the attributed absentee times and direct-help wording exactly; do not present the times as fully verified operational instructions. No universal late-request option, paid-time right, immediate strike, numerical threshold or proposed hub claim. Recheck help route without promising instant response. Both languages require human approval.

Membership addition checked Sept. 12: https://seiu503signup.org/ is the official application linked by Local 083. Starting, signing/submitting and processing an application do not establish this vote's cutoff or the applicant's eligibility. Preserve the organizer confirmation step in both languages.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
