#!/usr/bin/env python3
"""Generate the public sitemap from the shared public-page manifest."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from public_pages import BASE_URL, ROOT, sitemap_urls


def render_sitemap(urls: list[str]) -> str:
    rows = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        rows.extend(("  <url>", f"    <loc>{escape(url)}</loc>", "  </url>"))
    rows.append("</urlset>")
    return "\n".join(rows) + "\n"


def ensure_robots_sitemap(robots_path: Path) -> None:
    entry = f"Sitemap: {BASE_URL}/sitemap.xml"
    source = robots_path.read_text(encoding="utf-8") if robots_path.exists() else ""
    if entry in source.splitlines():
        return
    robots_path.write_text(source.rstrip() + f"\n\n{entry}\n", encoding="utf-8")


def main() -> None:
    output = ROOT / "sitemap.xml"
    output.write_text(render_sitemap(sitemap_urls(ROOT)), encoding="utf-8")
    ensure_robots_sitemap(ROOT / "robots.txt")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
