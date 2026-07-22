#!/usr/bin/env python3
"""Generate stable, noindex short-URL redirect pages from one manifest."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from public_pages import BASE_URL, ROOT
from sync_site_shell import sync_source


MANIFEST = ROOT / "data" / "short-urls.json"
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def canonical_target(target: str) -> str:
    if target.startswith("/"):
        return f"{BASE_URL}{target}"
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Redirect target must be root-relative or HTTP(S): {target!r}")
    return target


def render_redirect(entry: dict[str, str]) -> str:
    slug = entry["slug"]
    if not SLUG_RE.fullmatch(slug):
        raise ValueError(f"Invalid short URL slug: {slug!r}")

    target = entry["target"]
    target_canonical = canonical_target(target)
    title = entry["title"]
    description = entry["description"]
    short_url = f"{BASE_URL}/{slug}/"
    escaped_target = html.escape(target, quote=True)
    escaped_title = html.escape(title)
    escaped_description = html.escape(description, quote=True)

    page = f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escaped_description}">
    <meta name="robots" content="noindex, follow">
    <meta name="author" content="SEIU Local 503 at OSU">
    <meta http-equiv="refresh" content="0; url={escaped_target}">
    <title>{escaped_title} - SEIU Local 503, OSU</title>
    <link rel="stylesheet" href="/styles/tailwind.css">
    <link rel="stylesheet" href="/styles/fonts.css">
    <link rel="stylesheet" href="/styles/site-shell.css">
    <link rel="icon" href="/images/logo.png" type="image/png">
    <link rel="apple-touch-icon" href="/images/logo.png">
    <link rel="canonical" href="{html.escape(target_canonical, quote=True)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{short_url}">
    <meta property="og:title" content="{escaped_title} - SEIU Local 503, OSU">
    <meta property="og:description" content="{escaped_description}">
    <meta property="og:image" content="{BASE_URL}/images/card.webp">
    <meta property="og:site_name" content="SEIU Local 503 at Oregon State University">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{short_url}">
    <meta name="twitter:title" content="{escaped_title} - SEIU Local 503, OSU">
    <meta name="twitter:description" content="{escaped_description}">
    <meta name="twitter:image" content="{BASE_URL}/images/card.webp">
</head>
<body class="min-h-screen bg-brand-light" data-site-shell-added>
    <a href="#main-content" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:bg-white focus:text-brand-purple-dark focus:px-4 focus:py-2 focus:rounded focus:shadow-lg">Skip to content</a>
    <main id="main-content" class="container mx-auto px-6 py-16 text-center">
        <p class="text-sm font-semibold uppercase tracking-[0.2em] text-brand-purple">Redirecting</p>
        <h1 class="mt-4 text-4xl font-bold">{escaped_title}</h1>
        <p class="mx-auto mt-4 max-w-2xl text-lg text-text-secondary">{escaped_description}</p>
        <p class="mt-6 text-text-secondary">If the redirect does not start automatically, <a href="{escaped_target}" class="font-semibold text-brand-purple underline decoration-2 underline-offset-2">continue to {escaped_title.lower()}</a>.</p>
    </main>
</body>
</html>
'''
    return sync_source(page, f"{slug}/index.html")


def load_manifest(path: Path = MANIFEST) -> list[dict[str, str]]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("Short URL manifest must contain a list")
    slugs = [entry.get("slug") for entry in entries]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Short URL slugs must be unique")
    required = {"slug", "target", "title", "description"}
    for entry in entries:
        if not isinstance(entry, dict) or not required <= entry.keys():
            raise ValueError(f"Short URL entry is missing required fields: {entry!r}")
        if not all(isinstance(entry[key], str) and entry[key].strip() for key in required):
            raise ValueError(f"Short URL fields must be non-empty strings: {entry!r}")
    return entries


def generate(root: Path = ROOT, entries: list[dict[str, str]] | None = None) -> list[Path]:
    output_paths: list[Path] = []
    for entry in entries if entries is not None else load_manifest():
        output = root / entry["slug"] / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_redirect(entry), encoding="utf-8")
        output_paths.append(output)
    return output_paths


def main() -> int:
    outputs = generate()
    print(f"Generated {len(outputs)} short URL redirect page(s).")
    for output in outputs:
        print(output.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
