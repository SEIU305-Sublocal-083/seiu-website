# V01: Optional short video script captions and transcript

**Draft PR only. No publication, email send or schedule.**

This PR adds one independently mergeable review item. Target the translation integration branch, never `main` during this stage.

- Intended destination: Video production script, captions, transcript and accessible accompanying post.
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

# V01 — Optional 60–90-second video

## Editorial controls — not for narration

Prepared Sept. 12, 2026. Two complete spoken versions, captions and transcripts below. Record only after the essential bilingual voting email/text, P01/P02 and working hub fallback are complete. Video must never delay them. No named speaker or endorsement is invented; obtain a willing speaker's consent and approved use of voice/image. No recording has been created. Sources: S01/S03, ER1/ER3, web V01/R09. Recheck spoken facts just before recording; use only before Sept. 14 daytime voting. Update/retire afterward.

Each timestamped paragraph below is the production script AND its exact caption wording. A separate complete transcript follows each language and repeats that wording verbatim. Caption ranges are provisional editing guides, not measured audio. The revised narration contains approximately 152 English words and 177 Spanish words. At an assumed 130–150 words per minute, that is roughly 61–70 seconds in English and 71–82 seconds in Spanish before pauses. This is a word-count estimate, not a timed reading. Time actual natural reads; shorten further if needed instead of rushing. Split captions into short lines and synchronize them to the actual audio before release. Do not omit spoken meaning. Human bilingual/caption review remains required.

Visual plan: consenting local speaker; simple headline and date card; high-contrast venue card; final readable `www.local083.org/events.html` and `www.local083.org/contact.html`. Display each route long enough to read. Full text/transcript accompanies the video. If the proposed `/strike` later launches, replace the destination only after testing; the current draft uses existing fallbacks.

## Packaging note

The earlier working package was planning-only. The user has now authorized separate draft PRs and rendered-page screenshots. That authorization does not approve live changes or sending. All original factual holds continue to apply. Unreviewed machine Spanish is not included in this PR.
