# Strike communications PR stacks

The existing 28 content PRs are arranged in **four topic stacks** above foundation [#253](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/253). All 29 PRs remain drafts. Each PR targets the preceding branch and adds only its own item relative to that parent. The existing PR numbers, English copy, translation files and page screenshots are preserved.

| Stack | Review order, beginning above the foundation | Combined stack files |
|---|---|---|
| Guides and Q&A | [#263](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/263) → [#264](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/264) → [#265](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/265) → [#266](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/266) → [#267](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/267) → [#268](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/268) → [#269](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/269) → [#278](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/278) | [Browse this stack](https://github.com/SEIU305-Sublocal-083/seiu-website/tree/codex/strike-q01-common-and-complex-questions-index/test-pages/strike-2026) |
| Website and news | [#280](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/280) → [#270](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/270) → [#271](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/271) → [#272](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/272) → [#273](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/273) → [#281](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/281) | [Browse this stack](https://github.com/SEIU305-Sublocal-083/seiu-website/tree/codex/strike-w02-website-audit-and-migration-plan/test-pages/strike-2026) |
| Emails | [#255](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/255) → [#256](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/256) → [#257](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/257) → [#258](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/258) → [#259](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/259) → [#260](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/260) → [#261](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/261) → [#262](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/262) | [Browse this stack](https://github.com/SEIU305-Sublocal-083/seiu-website/tree/codex/strike-e08-monday-sept21-weekly-update-variants/test-pages/strike-2026) |
| Organizing materials | [#274](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/274) → [#275](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/275) → [#254](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/254) → [#276](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/276) → [#277](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/277) → [#279](https://github.com/SEIU305-Sublocal-083/seiu-website/pull/279) | [Browse this stack](https://github.com/SEIU305-Sublocal-083/seiu-website/tree/codex/strike-v01-optional-short-video-script-captions-and-transcript/test-pages/strike-2026) |

An arrow means “the following PR is based on the preceding PR.” The first PR in each row is based on `codex/strike-translation-review`. The last branch in each row contains every item in that topic stack. The foundation PR targets `main` and must remain unmerged during translation review.

## Review and translate

1. Open the item PR from the [complete index](PR-INDEX.md). Its description links to the previous and next PRs.
2. Edit only that item's `test-pages/strike-2026/ITEM-ID/` directory on its existing branch. Earlier items visible in the checkout belong to parent PRs.
3. Add and review the Spanish copy. H01–H07 and Q01 also require translated citation notes; other pages do not display a citation section.
4. Run the preview checks and refresh screenshots when rendered copy changes. Preserve existing factual holds and conditional alternatives.
5. When a parent branch changes, merge its current head into the next branch, continuing toward the tip. Resolve translation conflicts deliberately and recheck each PR's diff. Do not overwrite or force-push a translator's work. The branch relationships are recorded in [STACK.json](STACK.json).

## Later assembly into the review branch

No PR is being merged as part of arranging these stacks. After translation and review, assemble a topic stack in the order shown: merge its first approved item into `codex/strike-translation-review`, then retarget the next PR to that review branch and verify that its diff contains only the remaining item. Continue in sequence. Keep parent branches until their dependent PRs have been updated. Different topic stacks can be reviewed independently.

The foundation PR to `main` stays draft and unmerged. Website publication, production-route promotion and email delivery require separate authorization. Stacking does not approve content, resolve missing facts, send a message or publish the website.
