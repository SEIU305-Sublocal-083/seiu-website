# E07: Friday material-change email variants

**Draft PR only. No publication, email send or schedule.**

This is item 7 of 8 in the Emails stack. Its base is `codex/strike-e06-thursday-membership-meeting-reminder` (PR #260); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: E07 email campaign draft; no send or schedule.
- English source: `copy/en/`. 4 alternative(s), each with its own preview.
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

# E07 — Friday material-change email variants

## Internal editorial notes — do not send

Round 4 brand/copy review completed Sept. 12, 2026. This is a finished local copy draft, not release approval. All fact-check holds and future assembly requirements remain in force. Human Spanish fluency review is still outstanding.

Drafted Sept. 12 for a material development on Friday, Sept. 18, 2026, or an urgent actual development requiring the same format. Audience: affected Local 083 members, as authorized by the actual notice. No development means no E07 email. Sources: emails.md ER5–ER6/E07; guides.md H02/H06/H07; web_organizing.md N04. Future information cannot be verified on Sept. 12. Every branch is held until its specific event happens and union approval is recorded.

These are conditional editor templates with drafted introductions and actions; they are not assembled sendable messages. **ASSEMBLY HOLD: For release, each must be paired with an actual official, accessible bilingual information block in the email body, after the matching language's action paragraph and before its sign-off.** This necessary future block is not present or invented here. A linked document alone must not carry urgent start/return facts. An editor may replace the document-reference wording with a verified public destination only when the essential operational information remains in the body. Do not send a prose shell without the block. Check that every “below” / “abajo” reference points to the assembled block in the same language. No proposed /strike link is used.

| Branch | Required actual information before assembly/release |
| --- | --- |
| A — Notice only | Issuer, issue date/time, actual notice and its scope; precise distinction between advance notice and any member start instruction; confirmation no actual start order accompanies this message. |
| B — Official strike call | Written authorized start instruction; covered workers, exact date/time/time zone, reporting/call-in and work instructions, verified picket/preparation step, private access/support route, next confirmed briefing if any. Reproduce each accurately in both languages. |
| C — Tentative agreement | Actual signed/authorized TA status and text/summary; ratification process and eligibility/deadline if announced; explicit current effect on every strike notice/call and work/return instruction. Never infer suspension, cancellation or ratification. |
| D — Changed timeline | Exact previous instruction and issue date, replacement instruction with scope/date/time/time zone, who approved it, effect on work/picket/return plans, and route to resolve conflicts. |

Subject/preheader and complete prose for each branch follow. Choose one, insert its verified official block, remove all unused branches and editorial material, then obtain human factual, language and release approval. No assumed Sept. 18 notice, Sept. 28 start, lawfulness finding, funding availability or response-time promise.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
