# N04: Official strike notice tentative agreement or changed timeline news

**Draft PR only. No publication, email send or schedule.**

This is item 5 of 6 in the Website and news stack. Its base is `codex/strike-n03-september17-membership-meeting-recap-template` (PR #272); its diff adds only this item's directory. Edit this item on its own branch and carry parent updates forward. See [stack workflow](../STACK.md). Keep this PR draft during translation review.

- Intended destination: Dated /news/ article after an actual authorized announcement.
- English source: `copy/en/`. 5 alternative(s), each with its own preview.
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

# N04 — Official change news: notice, call, agreement, changed timetable or extended strike

## Editorial controls — not public copy

Prepared Sept. 12, 2026. All five variants are future-event drafts. None of these events is verified as having happened. Do not automatically publish Sept. 18 or use Sept. 28 as a countdown. Sources: S03/S07, web N04, guides G03/G05/H07. Written authorization, applicable process review and current official instructions are required. A notice is not interchangeable with an immediate instruction to stop work; an agreement is not automatically ratified or a return order. The text below needs the appropriate factual panel assembled before release; it is not operationally complete without that panel.

### Mandatory factual panel — editor completes from the actual written source

Place directly below the headline in English and Spanish. Supply the official source/issuer, announcement and publication dates/times/time zones, affected bargaining unit/members, exact current instruction and when it takes effect, what prior instruction it replaces, verified help route and next confirmed briefing or accepted update time. Link the approved public announcement; never link a private email or private source file. If the source is not public, obtain an approved publishable factual statement. Require the subject owner to approve each instruction and both language versions. No placeholder, editorial field name or unused variant may appear in released text.

Additional fields by trigger:

- **Notice:** kind of notice, recipient, date served and verified effect; distinguish notice from a later call. Do not imply legal sufficiency from the fact that a notice exists.
- **Actual call:** precise start date/time/time zone, covered workers/sites/shifts, call-in/reporting guidance, work that stops or any approved exceptions, instructions for overnight/remote shifts, picket/accessibility contact, property/timesheet direction or explicit individual help route. An unresolved essential stop-work instruction blocks this notice.
- **Tentative agreement:** verified terms/summary, required approval process, ratification eligibility/deadline/method if announced, and explicit authorized effect on strike plans or any action already underway.
- **Changed timetable:** exact old instruction being superseded, replacement, effective time, whether work status changes, and affected audiences/materials.
- **Extended strike:** confirmation that action continues, current instructions, next confirmed briefing or accepted update and actual support access. Funding duration and end date remain unpromised unless verified.

## HOLD — Variant A — formal notice issued, not an immediate call

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
