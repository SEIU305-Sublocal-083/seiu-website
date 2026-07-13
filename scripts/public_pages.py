#!/usr/bin/env python3
"""Shared discovery rules for Local 083 public HTML pages.

Keeping this logic in one place prevents the sitemap and quality audits from
quietly checking different sets of pages.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.local083.org"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "jules-scratch",
    "marketing",
    "node_modules",
    "review-images",
    "slides",
    "templates",
    "test-pages",
    "tmp",
    "welcome",
}
EXCLUDED_FILES = {"test-pages.html"}

NOINDEX_RE = re.compile(
    r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex[^"\']*["\'][^>]*>',
    re.IGNORECASE,
)
CANONICAL_RE = re.compile(
    r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PublicPage:
    path: Path
    canonical_url: str
    in_sitemap: bool


def default_url(path: Path, root: Path = ROOT) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel.removesuffix('index.html')}"
    return f"{BASE_URL}/{rel}"


def discover_public_pages(root: Path = ROOT, *, include_404: bool = True) -> list[PublicPage]:
    pages: list[PublicPage] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        if path.name in EXCLUDED_FILES or any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.name == "404.html" and not include_404:
            continue

        source = path.read_text(encoding="utf-8", errors="replace")
        canonical_match = CANONICAL_RE.search(source)
        canonical_url = canonical_match.group(1) if canonical_match else default_url(path, root)
        in_sitemap = path.name != "404.html" and not NOINDEX_RE.search(source)
        pages.append(PublicPage(path=path, canonical_url=canonical_url, in_sitemap=in_sitemap))
    return pages


def public_html_paths(root: Path = ROOT, *, include_404: bool = True) -> list[Path]:
    return [page.path for page in discover_public_pages(root, include_404=include_404)]


def sitemap_urls(root: Path = ROOT) -> list[str]:
    return sorted({
        page.canonical_url
        for page in discover_public_pages(root, include_404=False)
        if page.in_sitemap
    })
