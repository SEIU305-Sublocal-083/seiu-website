# E05: Wednesday certified-result or pending email variants

**Draft PR only. No publication, email send or schedule.**

This is item 5 of 8 in the Emails stack. Its base is `codex/strike-e04-tuesday-cascades-and-absentee-targeted-reminder` (PR #258); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: E05 email campaign draft; no send or schedule.
- English source: `copy/en/`. 3 alternative(s), each with its own preview.
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

# E05 — Wednesday result or pending update

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for Wednesday, Sept. 16, 2026. Audience: Local 083 members. Primary action in each branch: attend the confirmed Sept. 17 membership meeting. Sources: emails.md ER3–ER6; guides.md G03/H02; SOURCE-LEDGER.md S04. All three branches are conditional editor templates, not statements of a current outcome or assembled sendable messages. Select one only after a fresh authorized status check.

- **A / passed:** Written certification, its authority/timestamp/scope and an approved outcome statement are required. This version also requires confirmation that no separate official strike call has superseded its preparation language. Do not infer an overwhelming margin or add totals without an approved denominator.
- **B / not passed:** Same certification requirements; confirm the actual next-step statement. A no result does not accept management's proposal or promise another vote.
- **C / no certified result to share:** Use only if no certified result is available for public release at send time and an authorized editor chooses a pending update. It makes no certification deadline promise.

**ASSEMBLY HOLD:** For A or B, insert the actual official result block in each language after its opening paragraph: issuing/certifying authority, certification date/time/time zone, electorate/scope, approved outcome wording and actual next-step/work instructions. Include counts or percentages only if the official source supplies the relevant denominator; never infer a threshold. Link or attach the full official statement as additional evidence, using a verified public destination or an approved accessible bilingual attachment. The result block is absent from this draft. For C, add the actual as-of date/time/time zone and approved pending-status explanation; do not turn an unverified result into an assertion that certification has not happened. Verify every claim against that status. Confirm the Thursday meeting remains scheduled. No live hub, automatic strike date, personal obligation or procedural threshold assumed. Human institutional and bilingual approval remain required.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
