# Strike Prep

Draft English and Spanish communications for SEIU 503 Sublocal 083. See [the review index](PR-INDEX.md) and [four topic stacks](STACK.md).

## Review and translation

English sources are in `en/` and matching human Spanish translation slots are in `es/`. Each page has a language switch. Use the same slug and variant key on both sides; for example, `en/voting/a.md` pairs with `es/voting/a.md`. Empty Spanish slots render a clear pending notice, never a completed translation. The primary preview is `index.html`; named alternatives are `a.html`, `b.html`, and so on.

Review notes, factual holds, metadata, and screenshots live under `review/ITEM/`. Translators may provide text and comments in the relevant PR; maintainers can apply them to the matching Spanish source. Human bilingual review, factual refresh, and explicit release approval remain required. Changing English invalidates a Spanish approval recorded against an older English hash.

Only H01–H07 and Q01 display citations, inside a collapsed Sources and references section. Other items retain editorial source notes without displaying a citation section. Keep substantive qualifications in the main copy.

## Local previews

From the repository root:

```sh
python3 -m pip install -r test-pages/strike/requirements.txt
python3 scripts/build_strike_review.py
python3 -m http.server 8766 --bind 127.0.0.1 --directory test-pages
```

Open `http://127.0.0.1:8766/strike/` for the index. On W01 or its descendants, the hub pair is `/strike/en/` and `/strike/es/`. Item pages exist on their own branch and descendants. For example, H01 provides `/strike/en/voting/` and `/strike/es/voting/`.

```sh
python3 scripts/build_strike_review.py --check
python3 scripts/build_strike_review.py --item H01 --release-check
node scripts/capture_strike_reviews.cjs H01
```

Release checks are expected to fail while translations or facts remain unresolved; they do not publish. Files remain staged under `test-pages/strike/` on draft branches. No live routes, redirects, navigation, or email delivery have been changed. A later approved release must choose final content and promote only approved public pages, never internal plans or review controls.
