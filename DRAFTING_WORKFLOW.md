# Draft-to-Publish Workflow

This workflow defines how Local 083 pages move from first draft to production.

## Purpose
- Keep production pages accurate, searchable, and consistent.
- Build and review in `test-pages/` first.
- Promote only after content, SEO, and technical checks pass.

## Phase 1: Draft in `test-pages/`
1. Copy the closest template from `/templates/` (events, news, minutes, marketing, misc) into `test-pages/`.
2. Build complete draft content there first.
3. Keep draft URL out of production navigation.
4. Use union-first voice: speak as "our union," never as an outside entity.

## Phase 2: Content and QA Review
1. Remove placeholders (`TODO`, `TBD`, `[LINK]`, dummy `#` links).
2. Confirm all dates, times, locations, and names are correct.
3. Check voice and framing:
   - Use "our union" framing.
   - Include a clear member action where relevant.
4. Check accessibility basics:
   - Descriptive headings
   - Meaningful image `alt` text
   - Focus-visible behavior on interactive elements

## Phase 3: Promote to Production Path
1. Move/copy final page from `test-pages/` to correct directory:
   - root (`/`) for top-level pages
   - `events/` for event pages
   - `news/` for news pages
   - `resources/` for resources pages
   - `minutes/` for minutes pages
2. Update canonical URL and all share URLs (`og:url`, `twitter:url`) to production path.
3. Confirm nav/footer links are correct for that page type.

Helper script (copies and prints reminders):

```bash
scripts/promote_page.sh test-pages/my-draft.html events 2026-04-12-rally.html
```

## Phase 4: Update Data and Index Sources
1. If publishing an event page, update `events/events.json`.
2. If publishing a news page, update `news/news.json`.
3. If event has calendar support, add/update corresponding file in `events/ical/` and reference it.
4. Treat the JSON and generated listings as one change: the source data and rebuilt static files belong in the same commit.

## Phase 5: Technical Publish Tasks
Run from repo root:

```bash
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/site_quality_check.py --strict-placeholders
python3 scripts/accessibility_audit.py
python3 scripts/link_audit.py
python3 scripts/shell_consistency_audit.py
```

Then confirm:
1. The build completed and `--check` reports no generated-file drift.
2. `sitemap.xml` includes the production page and excludes `test-pages/`.
3. `robots.txt` includes `Sitemap: https://www.local083.org/sitemap.xml`.
4. If `events/events.json` or `news/news.json` changed, commit its generated output in the same commit:
   - `index.html`, `events.html`, and/or `news.html`
   - `events/rss.xml`
   - `news/rss.xml`
   - `feed.xml`
5. If public page paths changed, also commit `sitemap.xml` and `robots.txt`. If the shared shell or Tailwind classes changed, commit the synchronized HTML pages and `styles/tailwind.css`.

GitHub Actions reruns the build and fails if these committed artifacts are stale. It does not repair drift or create a follow-up commit. Scheduled news publishing is the exception: its workflow promotes due stories, runs the same full build and checks, and commits the source/status change with all generated outputs.

## Phase 6: Final Verification Checklist
1. Metadata complete:
   - title + meta description
   - canonical
   - OG tags
   - Twitter tags
   - JSON-LD (`Organization`, `WebSite`, `WebPage`, plus `Event` when relevant)
2. All internal links resolve.
3. Mobile layout and sticky header behavior are intact.
4. No placeholder content remains.
5. Copy uses "our union" framing throughout.

## Decision Table

| Page type | Where to draft | Production path | Required data/index updates | Required checks |
| --- | --- | --- | --- | --- |
| Event page | `test-pages/` | `events/*.html` | `events/events.json` (+ `events/ical/*.ics` if used) | `build_site.py`, `build_site.py --check`, quality audits |
| News page | `test-pages/` | `news/*.html` | `news/news.json` | `build_site.py`, `build_site.py --check`, quality audits |
| Resource page | `test-pages/` | `resources/*.html` | none by default | `build_site.py`, `build_site.py --check`, quality audits |
| Top-level page | `test-pages/` | `/[page].html` | none by default | `build_site.py`, `build_site.py --check`, quality audits |

## Copy Checklist (Union Voice)
1. Replace language that others our union.
   - Replace "the union" (as outsider) with "our union" or "we".
2. Emphasize member ownership and action.
3. Keep language specific, direct, and practical.
4. Use clear action text for buttons and links.
