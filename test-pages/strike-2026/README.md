# Strike communications: translation review workspace

**Drafts as of Sept. 12, 2026. No website publication or email delivery is authorized.**

This branch is the integration area for [28 separate content draft PRs](PR-INDEX.md), now open for the public GitHub review authorized by the user. GitHub Pages publishes from `main`, not this branch. Content PRs form four topic stacks; each targets its preceding branch, and the first in each stack targets `codex/strike-translation-review`. See [stack order and translation workflow](STACK.md). Keep the integration PR into `main` in draft; do not merge it as part of translation review.

Each item owns its directory. Translate that directory on its existing branch; earlier directories in the checkout belong to parent PRs. Carry parent updates through the stack before assembly. No production routes, redirects, news feeds, countdowns, Mailchimp campaigns or schedules are activated by these drafts. The proposed destination is recorded in each `item.json`. A later, separately authorized release must promote approved pages, connect navigation and rebuild the production site.

## Review one PR

1. Read its `REVIEW.md` and `item.json` for audience, intended destination and unresolved facts.
2. Review the full English copy in `copy/en/`. Conditional announcements have separate files; they are alternatives, not a sequence of events that has happened.
3. Open `index.html` locally, or use the committed desktop/mobile screenshots. Each alternative also has its own preview and screenshots. These screenshots show the actual rendered HTML.
4. On H01–H07 and Q01, open “Sources and references” for citations. It is collapsed by default. Routine emails, news, action pages, posters, the hub and internal plans have no citation footer. Practical contact/action links and important qualifications stay in the body; editorial source files remain available for every item. A contact route is not evidence of a guaranteed benefit. A dated union summary is not an agreed contract.

## Translator handoff

Create the Spanish text in the corresponding files in `copy/es/`. The English files are the source of truth for this handoff; Spanish from earlier machine drafts has deliberately not been prefilled or marked approved. Translate headlines, email subject/preheader, actions, captions/transcript, table headings, plus the source notes for items with `citations: "collapsed"`. Source-note translation is not required for pages with `citations: "none"`. Keep official contact addresses and URLs intact. Use agency Spanish links only when their content supports the same claim.

Set the Spanish display title in `item.json` under `title_es`, and set each translated variant's `translation_status` to `ready_for_review`. The bilingual reviewer records approval and the English source SHA-256 in that variant only after checking the final pair. A subsequent English edit invalidates that approval automatically. Internal-only plans explicitly do not require Spanish; their statuses must remain distinct from member-facing work.

Do not remove uncertainty, convert a proposal into an agreement, turn authorization into a strike call, promise money or coverage, or guess missing event details while translating. Raise questions in the PR. Never put personal ballot links, medical/financial cases, private email bodies or member rosters in this public repository.

## Build and check locally

From the repository root:

```sh
python3 -m venv /tmp/local083-review-env
/tmp/local083-review-env/bin/pip install -r test-pages/strike-2026/requirements.txt
/tmp/local083-review-env/bin/python scripts/build_strike_review.py
/tmp/local083-review-env/bin/python scripts/build_strike_review.py --check
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/test-pages/strike-2026/ITEM-ID/index.html`. You can also open the HTML directly; all preview styling is embedded and the existing logo uses a local relative path. No analytics, remote fonts or automatic publishing scripts run in these previews.

`--item H04` limits the builder to one item. `--release-check --item H04` additionally requires the selected variant, current editorial approval, completed human-reviewed Spanish and, where displayed, source-note approval; it fails while those conditions are unresolved. This is a readiness check, not a publish command. Current draft PRs are expected to pass preview checks and fail release checks.

## Merge order and eventual release

The 28 content PRs are arranged in four topic stacks. Each PR adds one item relative to its parent. After translation and review, assemble each stack in the order in [STACK.md](STACK.md), retargeting the next approved item to the integration branch as its predecessor is merged. Topic stacks can be reviewed independently. The integration PR into `main` is the final stop, not a translation convenience. Keep it unmerged until the user authorizes publication and the promotion changes, sources, time-sensitive facts, Spanish pages, internal links and production build have been reviewed together.

Do not automatically replace the bargaining archive or redirect pages during this stage. Preserve dated history. The migration proposal (W02) identifies the later production work and existing guides to reuse.
