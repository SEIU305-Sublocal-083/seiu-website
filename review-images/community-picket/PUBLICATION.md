# Community support and picket preparation publication

September 22, 2026. Promoted following the user's instruction to move the reviewed draft pages to production.

Public destinations:

- [Community support](https://www.local083.org/strike/community-support/)
- [Picket preparation](https://www.local083.org/strike/picket-preparation/)
- [Strike information and member support](https://www.local083.org/strike/)
- [Homepage](https://www.local083.org/)

Both guides are linked directly below the homepage hero and below the strike hub's timeline. The strike picketing and community-support FAQs link to the corresponding guide at the point of need. Both guides return to the strike hub and link to each other.

The strike hub includes the reviewed September 22 pay and benefits revision. Companion-page content retains the reviewed preparation status, Kerr map, solidarity actions, union email contacts and leadership inquiry drafts.

Removed the visible review notices and noindex tags from the promoted pages. Canonical, Open Graph, Twitter and WebPage schema URLs use the permanent destinations. Both companion pages include Organization and WebSite schema and appear in the generated sitemap. The homepage cards are outside generated content regions and survive the site build.

The four previous `/test-pages/` review URLs now redirect to their published counterparts. The redirect documents remain noindex and excluded from the sitemap; JavaScript preserves section anchors and an immediate HTML refresh provides a fallback without JavaScript. A visible destination link is also provided. These are static-page redirects, not HTTP 301 responses.

Prepublication validation:

- Build and generated-file check passed.
- All 69 Python tests and four email-draft tests passed.
- Quality, accessibility, link and shared-shell audits passed across 184 public pages.
- Chromium desktop (1440px) and mobile (390px) checks passed for all four destinations: metadata, structured data, navigation, no horizontal overflow, shared menus, source links and union email actions.
- Review redirects passed with and without JavaScript; section links into the strike guide open their containing topic.
- The 30 leadership inquiry variants remain distinct across the two pages; the failed-data and blocked-storage fallbacks passed. No email was sent.
- Inspected publication screenshots in `published/`. The companion pages retain the canonical navigation and footer.

Screenshots:

| Page | Desktop | Mobile |
| --- | --- | --- |
| Community support | [View](published/community-support-1440.png) | [View](published/community-support-390.png) |
| Picket preparation | [View](published/picket-preparation-1440.png) | [View](published/picket-preparation-390.png) |
| Homepage links | [View](published/homepage-1440.png) | [View](published/homepage-390.png) |
| Strike links | [View](published/strike-1440.png) | [View](published/strike-390.png) |

Earlier drafting and copy-review notes are retained as history in REVIEW.md, MARKETING-REVISIONS.md and BENEFITS-REVISIONS.md.
