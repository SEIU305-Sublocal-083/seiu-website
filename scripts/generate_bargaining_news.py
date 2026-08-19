#!/usr/bin/env python3
"""Generate bilingual SEIU 503 Higher Ed bargaining news pages."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path

from sync_site_shell import render_footer, render_header


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.local083.org"
MANIFEST = ROOT / "data" / "higher-ed-bargaining-updates.json"
NEWS_INDEX = ROOT / "news" / "news.json"


UI = {
    "en": {
        "skip": "Skip to content",
        "kicker": "SEIU 503 HIGHER ED BARGAINING UPDATE",
        "language": "Read in Spanish",
        "published": "Published",
        "by": "By",
        "credit": "Image courtesy of SEIU Local 503.",
        "cta_heading": "Keep building our power",
        "cta_body": "Sign the strike pledge, talk with coworkers and follow the bargaining hub for the latest actions and updates.",
        "pledge": "Sign the strike pledge",
        "hub": "View the bargaining hub",
        "source": "Source note",
        "source_body": "This update was originally published by the SEIU 503 Higher Ed Bargaining Team and is republished here in Local 083's news format.",
        "source_link": "View the original bargaining page",
        "topic": "Bargaining",
    },
    "es": {
        "skip": "Saltar al contenido",
        "kicker": "ACTUALIZACIÓN DE NEGOCIACIÓN DE EDUCACIÓN SUPERIOR DE SEIU 503",
        "language": "Read in English",
        "published": "Publicado",
        "by": "Por",
        "credit": "Imagen cortesía de SEIU Local 503.",
        "cta_heading": "Sigamos construyendo nuestro poder",
        "cta_body": "Firma el compromiso de huelga, habla con tus compañeros y consulta la página de negociación para conocer las acciones y novedades más recientes.",
        "pledge": "Firmar el compromiso de huelga",
        "hub": "Ver la página de negociación",
        "source": "Nota sobre la fuente",
        "source_body": "Esta actualización fue publicada originalmente por el equipo de negociación de educación superior de SEIU 503 y se reproduce aquí con el formato de noticias de Local 083.",
        "source_link": "Ver la página original de negociación",
        "topic": "Negociación",
    },
}


SPANISH_MONTHS = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def display_date(value: str, language: str) -> str:
    date = datetime.strptime(value, "%Y-%m-%d")
    if language == "es":
        return f"{date.day} de {SPANISH_MONTHS[date.month]} de {date.year}"
    return f"{date.strftime('%B')} {date.day}, {date.year}"


def entries(payload: dict) -> list[tuple[dict, str, dict, dict]]:
    rows = []
    for update in payload["updates"]:
        for language in ("en", "es"):
            article = update["languages"][language]
            alternate = update["languages"]["es" if language == "en" else "en"]
            rows.append((update, language, article, alternate))
    return rows


def article_tags(update: dict, language: str) -> list[str]:
    tags = list(update["tags"])
    if language == "es":
        tags.append("Español")
    return tags


def render_page(
    payload: dict,
    update: dict,
    language: str,
    article: dict,
    alternate: dict,
    header: str,
    footer: str,
) -> str:
    ui = UI[language]
    author = payload["author"]["name"]
    url = f"{BASE_URL}{article['url']}"
    alternate_url = f"{BASE_URL}{alternate['url']}"
    en_url = f"{BASE_URL}{update['languages']['en']['url']}"
    es_url = f"{BASE_URL}{update['languages']['es']['url']}"
    source_url = payload["source"]["spanish" if language == "es" else "english"]
    page_title = f"{article['title']} - SEIU Local 503 at Oregon State University"
    tags = article_tags(update, language)
    body_html = "\n".join(line.rstrip() for line in article["bodyHtml"].splitlines())
    tag_meta = "\n".join(
        f'    <meta property="article:tag" content="{esc(tag)}">' for tag in tags
    )
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE_URL}#organization",
                "name": "SEIU Local 503 at Oregon State University",
                "alternateName": "Local 083",
                "url": BASE_URL,
                "logo": f"{BASE_URL}/images/logo.png",
            },
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}#website",
                "url": BASE_URL,
                "name": "SEIU Local 503 at Oregon State University",
                "publisher": {"@id": f"{BASE_URL}#organization"},
            },
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": page_title,
                "description": article["description"],
                "inLanguage": language,
                "isPartOf": {"@id": f"{BASE_URL}#website"},
                "about": {"@id": f"{BASE_URL}#organization"},
            },
            {
                "@type": "NewsArticle",
                "@id": f"{url}#article",
                "url": url,
                "headline": article["title"],
                "description": article["description"],
                "image": f"{BASE_URL}{article['heroImage']}",
                "datePublished": update["date"],
                "dateModified": payload["source"]["accessedAt"],
                "inLanguage": language,
                "articleSection": "Bargaining",
                "keywords": tags,
                "author": {"@type": "Organization", "name": author},
                "publisher": {"@id": f"{BASE_URL}#organization"},
                "mainEntityOfPage": {"@id": f"{url}#webpage"},
            },
        ],
    }
    return f'''<!DOCTYPE html>
<html lang="{language}" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{esc(article['description'])}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="{esc(author)}">
    <title>{esc(page_title)}</title>
    <link rel="stylesheet" href="/styles/tailwind.css">
    <link rel="stylesheet" href="/styles/fonts.css">
    <link rel="stylesheet" href="/styles/site-shell.css">
    <link rel="icon" href="/images/logo.png" type="image/png">
    <link rel="apple-touch-icon" href="/images/logo.png">
    <style>
        :root {{
            --brand-purple-dark: #4c1d95;
            --brand-purple: #7c3aed;
            --brand-purple-light: #ede9fe;
            --brand-light: #f9fafb;
            --text-primary: #1f2937;
            --text-secondary: #374151;
            --border-color: #d1d5db;
        }}
        body {{ background: var(--brand-light); color: var(--text-primary); font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
        h1, h2, h3, h4 {{ color: var(--brand-purple-dark); font-family: 'Lora', serif; }}
        a:focus-visible, button:focus-visible {{ border-radius: 4px; outline: 3px solid var(--brand-purple); outline-offset: 2px; }}
        .article-content > * + * {{ margin-top: 1.25rem; }}
        .article-content h2 {{ font-size: clamp(1.4rem, 2.6vw, 1.9rem); font-weight: 700; line-height: 1.25; margin-top: 2.25rem; }}
        .article-content ul, .article-content ol {{ padding-left: 1.5rem; }}
        .article-content ul {{ list-style: disc; }}
        .article-content ol {{ list-style: decimal; }}
        .article-content li + li {{ margin-top: .65rem; }}
        .article-content a {{ color: var(--brand-purple-dark); font-weight: 700; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }}
        .article-content a:hover {{ color: var(--brand-purple); }}
        .article-content blockquote {{ border-left: 4px solid var(--brand-purple); color: var(--text-primary); font-size: 1.1em; font-style: italic; padding-left: 1.25rem; }}
        .article-content table {{ border-collapse: collapse; display: block; max-width: 100%; overflow-x: auto; width: 100%; }}
        .article-content th, .article-content td {{ border: 1px solid #d1d5db; min-width: 10rem; padding: .75rem; text-align: left; vertical-align: top; }}
        .article-content th {{ background: var(--brand-purple-light); color: var(--brand-purple-dark); }}
        .article-content .source-inline-image {{ border-radius: .75rem; height: auto; margin: 1.5rem auto; max-height: 38rem; object-fit: contain; width: min(100%, 48rem); }}
        .article-content hr {{ border: 0; border-top: 1px solid #d1d5db; margin: 2rem 0; }}
        .article-content div:has(> a:only-child) {{ margin-top: 1.5rem; }}
        .article-content div:has(> a:only-child) > a {{ background: var(--brand-purple); border-radius: .5rem; color: white; display: inline-block; padding: .75rem 1.25rem; text-decoration: none; }}
        .article-content div:has(> a:only-child) > a:hover {{ background: var(--brand-purple-dark); color: white; }}
    </style>
    <link rel="canonical" href="{esc(url)}">
    <link rel="alternate" hreflang="en" href="{esc(en_url)}">
    <link rel="alternate" hreflang="es" href="{esc(es_url)}">
    <link rel="alternate" hreflang="x-default" href="{esc(en_url)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{esc(url)}">
    <meta property="og:title" content="{esc(article['title'])}">
    <meta property="og:description" content="{esc(article['description'])}">
    <meta property="og:image" content="{BASE_URL}{esc(article['heroImage'])}">
    <meta property="og:image:alt" content="{esc(article['heroAlt'])}">
    <meta property="og:image:width" content="{article['heroWidth']}">
    <meta property="og:image:height" content="{article['heroHeight']}">
    <meta property="og:site_name" content="SEIU Local 503 at Oregon State University">
    <meta property="article:published_time" content="{update['date']}">
    <meta property="article:section" content="Bargaining">
{tag_meta}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{esc(url)}">
    <meta name="twitter:title" content="{esc(article['title'])}">
    <meta name="twitter:description" content="{esc(article['description'])}">
    <meta name="twitter:image" content="{BASE_URL}{esc(article['heroImage'])}">
    <meta name="twitter:image:alt" content="{esc(article['heroAlt'])}">
    <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
    </script>
    <script src="/js/analytics.js" defer></script>
</head>
<body class="bg-brand-light">
    <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:bg-white focus:text-brand-purple-dark focus:px-4 focus:py-2 focus:rounded focus:shadow-lg">{esc(ui['skip'])}</a>

    {header}

    <main id="main-content" class="container mx-auto px-4 py-10 sm:px-6 md:py-16">
        <article class="max-w-6xl mx-auto bg-white rounded-2xl border border-border-color overflow-hidden shadow-sm">
            <header class="px-5 pt-8 pb-7 sm:px-8 md:px-12 md:pt-10 md:pb-8 bg-gradient-to-br from-white via-brand-purple-light/40 to-white border-b border-border-color">
                <div class="flex flex-wrap items-center justify-center gap-3 text-sm font-semibold tracking-wide">
                    <span class="inline-flex items-center rounded-full bg-brand-purple text-white px-4 py-1">{esc(ui['kicker'])}</span>
                    <a class="inline-flex items-center rounded-full border border-brand-purple/20 bg-white px-4 py-1 text-brand-purple-dark hover:border-brand-purple" href="{esc(alternate['url'])}" hreflang="{'es' if language == 'en' else 'en'}">{esc(ui['language'])}</a>
                </div>
                <h1 class="mt-5 text-center text-3xl md:mt-6 md:text-5xl font-bold">{esc(article['title'])}</h1>
                <p class="mt-3 max-w-4xl mx-auto text-center text-base md:mt-4 md:text-lg text-text-secondary">{esc(article['description'])}</p>
                <div class="mt-6 flex flex-col items-center gap-2 text-center text-sm text-text-secondary">
                    <p>{esc(ui['by'])} <span class="font-semibold">{esc(author)}</span></p>
                    <p>{esc(ui['published'])} <time datetime="{update['date']}">{esc(display_date(update['date'], language))}</time></p>
                </div>
            </header>

            <figure class="px-5 pt-6 sm:px-8 md:px-12 md:pt-8">
                <img src="{esc(article['heroImage'])}" alt="{esc(article['heroAlt'])}" class="w-full max-h-[42rem] h-auto object-contain rounded-xl bg-gray-50" decoding="async" width="{article['heroWidth']}" height="{article['heroHeight']}">
                <figcaption class="mt-2 text-center text-sm text-text-secondary">{esc(ui['credit'])}</figcaption>
            </figure>

            <div class="px-5 py-7 sm:px-8 md:px-12 md:py-10">
                <div class="article-content max-w-4xl mx-auto text-base md:text-lg leading-relaxed text-text-secondary">
{body_html}
                </div>

                <section class="max-w-4xl mx-auto mt-10 rounded-xl border border-brand-purple/20 bg-brand-purple-light/45 p-5 md:p-7">
                    <h2 class="text-2xl md:text-3xl font-bold">{esc(ui['cta_heading'])}</h2>
                    <p class="mt-3 text-text-secondary text-base md:text-lg">{esc(ui['cta_body'])}</p>
                    <div class="mt-5 flex flex-col sm:flex-row gap-3">
                        <a href="/pledge" class="btn btn-primary" data-ph-event="take_action_click" data-ph-label="Imported Bargaining Update Strike Pledge">{esc(ui['pledge'])}</a>
                        <a href="/2026-bargaining/" class="btn btn-outline">{esc(ui['hub'])}</a>
                    </div>
                </section>

                <section class="max-w-4xl mx-auto mt-8 border-t border-border-color pt-6 text-sm md:text-base text-text-secondary">
                    <h2 class="text-xl md:text-2xl font-bold text-text-primary">{esc(ui['source'])}</h2>
                    <p class="mt-2">{esc(ui['source_body'])} <a class="font-semibold text-brand-purple underline" href="{esc(source_url)}" target="_blank" rel="noopener noreferrer">{esc(ui['source_link'])}</a>.</p>
                </section>
            </div>
        </article>
    </main>

    {footer}
</body>
</html>
'''


def news_entry(payload: dict, update: dict, language: str, article: dict) -> dict:
    author = payload["author"]
    return {
        "status": "published",
        "title": article["title"],
        "description": article["description"],
        "url": article["url"],
        "image": article["heroImage"],
        "alt": article["heroAlt"],
        "tags": article_tags(update, language),
        "author": {"name": author["name"], "title": author["title"]},
        "publishedAt": update["date"],
        "createdAt": update["date"],
        "updatedAt": payload["source"]["accessedAt"],
        "featured": language == "en" and update["date"] == payload["updates"][0]["date"],
        "language": language,
    }


def sync_index(payload: dict) -> None:
    imported = [news_entry(payload, update, language, article) for update, language, article, _ in entries(payload)]
    imported_urls = {item["url"] for item in imported}
    existing = json.loads(NEWS_INDEX.read_text(encoding="utf-8"))
    merged = imported + [item for item in existing if item.get("url") not in imported_urls]
    NEWS_INDEX.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(imported)} bargaining stories into {NEWS_INDEX}")


def build(*, update_index: bool = False) -> list[Path]:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    written = []
    for update, language, article, alternate in entries(payload):
        path = ROOT / article["url"].lstrip("/")
        path.parent.mkdir(parents=True, exist_ok=True)
        relative_path = path.relative_to(ROOT).as_posix()
        header = render_header(relative_path)
        footer = render_footer(relative_path)
        path.write_text(render_page(payload, update, language, article, alternate, header, footer), encoding="utf-8")
        written.append(path)
    if update_index:
        sync_index(payload)
    else:
        indexed_urls = {item.get("url") for item in json.loads(NEWS_INDEX.read_text(encoding="utf-8"))}
        missing = [article["url"] for _, _, article, _ in entries(payload) if article["url"] not in indexed_urls]
        if missing:
            raise ValueError("Bargaining news pages are missing from news/news.json: " + ", ".join(missing))
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync-index", action="store_true", help="Add or refresh manifest entries in news/news.json.")
    args = parser.parse_args()
    for path in build(update_index=args.sync_index):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
