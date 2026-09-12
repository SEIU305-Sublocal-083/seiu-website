#!/usr/bin/env python3
"""Build isolated translation previews. This script cannot publish or send."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / 'test-pages' / 'strike-2026'
CSS = '''
:root{--purple:#4c1d95;--light:#ede9fe;--ink:#1f2937;--muted:#4b5563;--line:#d1d5db}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f9fafb;font:18px/1.65 Inter,Arial,sans-serif}
a{color:var(--purple);text-decoration:underline;text-underline-offset:.18em;overflow-wrap:anywhere}a:hover{color:#6d28d9}
a:focus-visible,summary:focus-visible{outline:3px solid #7c3aed;outline-offset:4px}.skip{position:absolute;top:-100px}.skip:focus{top:8px;background:white;padding:10px;z-index:4}
.review-banner{background:#fff3cd;color:#513c00;border-bottom:1px solid #dcc477;padding:12px max(20px,calc((100vw - 1100px)/2));font-size:14px;font-weight:700}
.masthead{max-width:1100px;margin:auto;padding:26px 24px;display:flex;gap:18px;align-items:center}.masthead img{width:74px;height:64px;object-fit:contain}.masthead p{margin:0;font-size:14px;color:var(--muted)}.brand{color:var(--purple);font-weight:800;font-size:21px}
.frame{max-width:1100px;margin:0 auto;padding:0 24px 56px}.eyebrow{font-size:13px;letter-spacing:.09em;text-transform:uppercase;font-weight:800;color:var(--purple)}
.review-meta{border:1px solid #c4b5fd;background:#f5f3ff;border-radius:12px;padding:18px 22px;margin-bottom:22px;font-size:15px}.review-meta p{margin:4px 0}.review-meta strong{color:#4c1d95}
.variants{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0}.variants a{display:inline-block;border:1px solid #a78bfa;background:white;border-radius:7px;padding:7px 12px;font-size:14px}.variants a[aria-current=page]{background:var(--purple);color:white}
article{background:white;border:1px solid var(--line);border-top:6px solid var(--purple);border-radius:12px;padding:clamp(22px,5vw,60px);box-shadow:0 3px 15px #11182708}
.prose{max-width:840px;margin:auto}.email .prose{max-width:680px}h1,h2,h3{font-family:Lora,Georgia,serif;color:#35205f;line-height:1.2;overflow-wrap:anywhere}h1{font-size:clamp(32px,4.5vw,48px);margin:10px 0 25px;letter-spacing:-.025em}h2{font-size:28px;margin:38px 0 16px}h3{font-size:23px;margin:30px 0 12px}p{margin:0 0 20px}li{margin:8px 0}ul,ol{padding-left:25px}strong{font-weight:750}
blockquote{margin:24px 0;padding:18px 22px;border-left:5px solid #b45309;background:#fffbeb;color:#593706}blockquote p:last-child{margin-bottom:0}
.table-wrap{overflow-x:auto;margin:24px 0;border:1px solid var(--line);border-radius:8px}table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.5}th,td{text-align:left;vertical-align:top;padding:15px;border-bottom:1px solid var(--line)}th{background:var(--light);color:#35205f}tbody tr:nth-child(even){background:#faf8ff}
.sources{border-top:2px solid var(--line);margin-top:40px;padding-top:4px;font-size:15px;color:#374151}.sources h2{font-size:24px}.sources li{margin:14px 0}.footer{max-width:1100px;margin:auto;padding:0 24px 36px;font-size:14px;color:var(--muted)}code{font-size:.9em;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#f3f4f6;padding:18px;border-radius:8px}.poster h1{font-size:clamp(42px,6vw,66px)}.poster article{border-top-width:12px}.poster .prose{max-width:760px}
@media(max-width:600px){body{font-size:17px}.frame{padding:0 14px 30px}.masthead{padding:18px 16px}.masthead img{width:55px;height:50px}.brand{font-size:18px}.review-banner{padding:10px 16px;font-size:12px}.review-meta{padding:14px;font-size:14px}article{padding:22px 18px}h2{font-size:25px}h3{font-size:22px}th,td{min-width:155px;padding:12px}table{font-size:14px}.footer{padding:0 18px 28px}}
@media print{.review-banner{border:2px solid #111}.variants,.skip{display:none}body{background:white;font-size:12pt}.frame{padding:0}article{border:0;box-shadow:none;padding:18px}.table-wrap{overflow:visible}h1{font-size:28pt}h2{font-size:20pt}a{color:#111}.review-meta{break-inside:avoid}.sources{font-size:10pt}}
'''


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_without_comments(value: str) -> str:
    return re.sub(r'<!--.*?-->', '', value, flags=re.S).strip()


def render_md(value: str) -> str:
    result = markdown.markdown(value, extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    return result.replace('<table>', '<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable comparison table"><table>').replace('</table>', '</table></div>')


def page(title: str, body: str, *, lang: str = 'en', kind: str = '', meta: str = '', root: bool = False) -> str:
    logo = '../../images/logo.png' if root else '../../../images/logo.png'
    banner = 'REVIEW DRAFT · Translation and editorial approval pending · Not an announcement or work instruction'
    if lang == 'es':
        banner = 'BORRADOR PARA REVISIÓN · Pendiente de aprobación · No es un anuncio ni una instrucción laboral'
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{html.escape(title)} — Local 083 review</title><style>{CSS}</style></head>
<body class="{html.escape(kind)}"><a class="skip" href="#content">Skip to content</a><div class="review-banner">{banner}</div>
<header class="masthead"><img src="{logo}" alt="SEIU 503" width="74" height="64"><div><div class="brand">SEIU 503 · Sublocal 083</div><p>Oregon State University · Our contract. Our voice.</p></div></header>
<main id="content" class="frame">{meta}<article><div class="prose">{body}</div></article></main>
<footer class="footer">Local preview only. Source snapshot: Sept. 12, 2026. No analytics, email delivery or publication.<br>Maintained sources and individual help routes belong with the member copy at release.</footer></body></html>
'''


def outputs(folder: Path) -> dict[Path, str]:
    item = json.loads((folder / 'item.json').read_text())
    result = {}
    for language in ('en', 'es'):
        for i, variant in enumerate(item['variants']):
            source = folder / variant[language]
            if not source.exists() or not text_without_comments(source.read_text()):
                continue
            body = source.read_text()
            headings = re.findall(r'^# (.+)$', body, re.M)
            title = headings[0] if headings else (item.get('title_es') if language == 'es' else item['title'])
            title = title or item['title']
            if not headings:
                body = '# ' + title + '\n\n' + body
            sources = folder / 'sources' / f'{language}.md'
            sources_text = sources.read_text() if sources.exists() else ''
            sources_heading = 'Sources and source limits' if language == 'en' else 'Fuentes y límites de la información'
            sources_html = render_md(sources_text) if text_without_comments(sources_text) else '<p>Source-note translation awaits human review.</p>'
            if item.get('internal_only'):
                status = 'Internal plan · proposed responsibilities and dates require acceptance.'
            elif variant.get('conditional'):
                status = 'Conditional draft · this event has not been verified. Complete the factual panel before release.'
            else:
                status = 'English source for translation · refresh time-sensitive facts before release.'
            nav = ''.join(f'<a href="{v["key"]}.{language}.html"'+(' aria-current="page"' if v['key'] == variant['key'] else '')+f'>{html.escape(v["label"])}</a>' for v in item['variants'] if text_without_comments((folder / v[language]).read_text()))
            translation = 'Not required for this internal plan' if item.get('internal_only') else variant['translation_status'].replace('_', ' ')
            meta = f'<aside class="review-meta" aria-label="Editorial review status"><div class="eyebrow">{item["id"]} · {html.escape(item["channel"])}</div><p><strong>{status}</strong></p><p>Spanish: {html.escape(translation)}. Proposed destination: {html.escape(item["proposed_destination"])}.</p><nav class="variants" aria-label="Draft alternatives">{nav}</nav></aside>'
            content = render_md(body) + f'<section class="sources" aria-label="{sources_heading}"><h2>{sources_heading}</h2>{sources_html}</section>'
            document = page(title, content, lang=language, kind=item['channel'], meta=meta)
            result[folder / f'{variant["key"]}.{language}.html'] = document
            if i == 0 and language == 'en':
                result[folder / 'index.html'] = document
    return result


def validate(folder: Path, release: bool) -> list[str]:
    item = json.loads((folder / 'item.json').read_text())
    errors = []
    keys = [v['key'] for v in item['variants']]
    if len(keys) != len(set(keys)):
        errors.append('duplicate variant keys')
    for path in folder.rglob('*'):
        if path.suffix not in {'.md', '.json', '.html'}:
            continue
        value = path.read_text()
        if re.search(r'https?://[^\s<>"\)]+(?:targetId=|mail\.google\.com|/gmail/)|/Users/|data:image/|(?:sk-proj-)[A-Za-z0-9]', value, re.I):
            errors.append(f'private link, local path or embedded payload in {path.name}')
    for variant in item['variants']:
        for language in ('en', 'es'):
            path = folder / variant[language]
            if not path.exists():
                errors.append(f'missing translation/source slot: {path}')
        if not text_without_comments((folder / variant['en']).read_text()):
            errors.append(f'empty English source: {variant["key"]}')
        if variant['translation_status'] == 'approved' and variant.get('approved_english_sha256') != sha(folder / variant['en']):
            errors.append(f'Spanish approval invalidated by English change: {variant["key"]}')
    if not text_without_comments((folder / 'sources/en.md').read_text()):
        errors.append('missing visible English source notes')
    if release:
        selected = next((v for v in item['variants'] if v['key'] == item.get('selected_variant')), None)
        if selected is None:
            errors.append('select exactly one variant for release')
        else:
            if not item.get('editor_approved_by') or not item.get('facts_rechecked_at') or item.get('open_release_gates'):
                errors.append('editor approval, current fact check or release conditions unresolved')
            if not item.get('internal_only'):
                if selected['translation_status'] != 'approved' or not selected.get('spanish_reviewer'):
                    errors.append('human Spanish review is required')
                if not item.get('source_notes_spanish_reviewer') or not text_without_comments((folder / 'sources/es.md').read_text()) or not item.get('title_es'):
                    errors.append('Spanish title and visible source notes require review')
            for language in ('en', 'es') if not item.get('internal_only') else ('en',):
                value = text_without_comments((folder / selected[language]).read_text())
                if not value or re.search(r'\bHOLD\b|\bTBD\b|\[insert|\[name', value, re.I):
                    errors.append(f'incomplete {language} member copy')
    return [f'{folder.name}: {error}' for error in errors]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--item', help='Item ID, for example H04')
    parser.add_argument('--check', action='store_true', help='Validate committed preview output without writing')
    parser.add_argument('--release-check', action='store_true', help='Additionally require completed translation and release conditions; never publishes')
    args = parser.parse_args()
    folders = sorted(p.parent for p in REVIEWS.glob('*/item.json') if not args.item or p.parent.name == args.item)
    if args.item and not folders:
        parser.error('unknown item ID')
    failures = []
    generated = 0
    if not args.item:
        overview = REVIEWS / 'OVERVIEW.md'
        overview_page = page('Translation review workspace', render_md(overview.read_text()), root=True)
        overview_path = REVIEWS / 'index.html'
        if args.check:
            if not overview_path.exists() or overview_path.read_text() != overview_page:
                failures.append('stale translation-workspace overview')
        elif not args.release_check:
            overview_path.write_text(overview_page)
    for folder in folders:
        failures.extend(validate(folder, args.release_check))
        for path, content in outputs(folder).items():
            generated += 1
            if args.check:
                if not path.exists() or path.read_text() != content:
                    failures.append(f'stale preview: {path.relative_to(ROOT)}')
            elif not args.release_check:
                path.write_text(content)
    if failures:
        print('\n'.join(failures))
        return 1
    print(f'{len(folders)} items; {generated} previews checked. No publication or email action.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
