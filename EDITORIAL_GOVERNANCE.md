# Local 083 Website Editorial Governance

This document assigns role-based ownership for information that can become stale. Named officeholders may change; responsibility stays with the role.

## Ownership and review cadence

| Content | Accountable owner | Required reviewer | Review trigger | Maximum review interval |
| --- | --- | --- | --- | --- |
| Bargaining status, proposals and calls to action | Bargaining team designee | Communications chair | After every session, proposal or action change | Within 24 hours of a change |
| Leadership roster, vacancies and officer roles | Local 083 secretary | President | Election, appointment, resignation or vacancy | Quarterly |
| Events, meeting links, rooms, food and accessibility details | Named event organizer | Secretary or communications chair | Publication, 72 hours before the event and every change | Per event |
| Worker and county statistics | Membership coordinator | Communications chair | New OSU salary report or membership export | Quarterly |
| Contract and workplace-rights guides | Chief steward | A second designated steward | Contract, law or OSU-process change | Quarterly |
| Contact addresses and mailing location | Secretary | President | Any staffing or office change | Quarterly |
| News facts, names, quotations and photo credits | Story editor or communications chair | A person with direct knowledge of the event | Before publication and after corrections | Per story |
| Metadata, structured data, RSS and sitemap | Web maintainer | Communications chair | Every publication | Per release |
| Broken links and external destinations | Web maintainer | Content owner for affected page | Automated check on every change | Monthly full crawl |
| Privacy notice and analytics configuration | Web maintainer | Executive committee designee | Analytics vendor or configuration change | Quarterly |

## Required source record

For every time-sensitive factual update, record the source in the pull request, issue or editorial note:

- who confirmed it;
- the date and time confirmed;
- the source document, email or meeting;
- the page owner;
- the next review date when applicable.

Do not publish an unverified name, title, deadline, event location, bargaining proposal, member count or quotation. When information is intentionally incomplete, say so plainly and identify who will update it.

## Publication checklist

1. Content owner and reviewer approve the facts.
2. Dates use Oregon local time and include a timezone when a precise release time matters.
3. Images have accurate alt text, captions and credits; children are not named without explicit approval.
4. Page title, description, canonical URL, social metadata and structured data match the visible content.
5. Internal links, external actions, email links, PDFs and calendar files are tested.
6. Scheduled pages remain `noindex` and excluded from feeds and sitemap until publication.
7. Run `python3 scripts/build_site.py`, commit the source and generated output together, then run `python3 scripts/build_site.py --check` to confirm there is no drift.
8. Run `python3 scripts/site_quality_check.py --strict-placeholders`, `python3 scripts/accessibility_audit.py`, `python3 scripts/link_audit.py` and `python3 scripts/shell_consistency_audit.py`.
9. Complete a mobile, desktop, keyboard and screen-reader spot check for materially changed layouts.
10. Add or update the visible “last reviewed” date where the information can become stale.

## Corrections

Correct factual errors promptly. Update `dateModified` in structured data and the visible correction or review date when a correction changes the meaning of a story or guide. Preserve the original publication date.
