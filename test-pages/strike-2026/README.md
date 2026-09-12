# Strike communications: translation review workspace

**Drafts as of Sept. 12, 2026. No website publication or email delivery is authorized.**

This branch is the integration area for [28 separate content draft PRs](PR-INDEX.md), now open for the public GitHub review authorized by the user. GitHub Pages publishes from `main`, not this branch. Each content PR targets `codex/strike-translation-review`. Keep the integration PR into `main` in draft; do not merge it as part of translation review.

Each item owns its directory, so translators can work and maintainers can merge reviewed items here without conflicts in shared news, event, sitemap or homepage files. No production routes, redirects, news feeds, countdowns, Mailchimp campaigns or schedules are activated by these drafts. The proposed destination is recorded in each `item.json`. A later, separately authorized release must promote approved pages, connect navigation and rebuild the production site.

## Review one PR

1. Read its `REVIEW.md` and `item.json` for audience, intended destination and unresolved facts.
2. Review the full English copy in `copy/en/`. Conditional announcements have separate files; they are alternatives, not a sequence of events that has happened.
3. Open `index.html` locally, or use the committed desktop/mobile screenshots. Each alternative also has its own preview and screenshots. These screenshots show the actual rendered HTML.
4. Read the visible “Sources and source limits” section in the preview. Citations remain in the page body, alongside factual claims where applicable. A contact route is not evidence of a guaranteed benefit. A dated union summary is not an agreed contract.

## Translator handoff

Create the Spanish text in the corresponding files in `copy/es/`. The English files are the source of truth for this handoff; Spanish from earlier machine drafts has deliberately not been prefilled or marked approved. Translate headlines, email subject/preheader, actions, captions/transcript, table headings and the visible source notes. Keep official contact addresses and URLs intact. Use agency Spanish links only when their content supports the same claim.

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

`--item H04` limits the builder to one item. `--release-check --item H04` additionally requires the selected variant, current editorial approval, completed human-reviewed Spanish and source-note approval; it fails while those conditions are unresolved. This is a readiness check, not a publish command. Current draft PRs are expected to pass preview checks and fail release checks.

## Merge order and eventual release

The 28 content PRs share this integration branch as their base and each adds one independent directory. They can be merged into this branch in any order after review. The integration PR into `main` is the final stop, not a translation convenience. Keep it unmerged until the user authorizes publication and the promotion changes, sources, time-sensitive facts, Spanish pages, internal links and production build have been reviewed together.

Do not automatically replace the bargaining archive or redirect pages during this stage. Preserve dated history. The migration proposal (W02) identifies the later production work and existing guides to reuse.
