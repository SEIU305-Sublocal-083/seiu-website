#!/usr/bin/env python3
"""Audit public links and downloadable actions without requiring a browser."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from public_pages import public_html_paths

ROOT = Path(__file__).resolve().parents[1]
LOCAL_HOSTS = {"local083.org", "www.local083.org"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, dict[str, str], int]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
        if values.get("name") and tag.lower() == "a":
            self.ids.add(values["name"])
        attribute = "href" if tag.lower() in {"a", "area", "link"} else "src" if tag.lower() in {"img", "script", "iframe", "source"} else ""
        if attribute and values.get(attribute):
            self.links.append((tag.lower(), values, self.getpos()[0]))


def public_pages() -> list[Path]:
    return public_html_paths(ROOT, include_404=True)


def local_path(source: Path, raw_url: str) -> tuple[Path, str] | None:
    parsed = urlsplit(raw_url)
    if parsed.scheme in {"http", "https"}:
        if parsed.hostname not in LOCAL_HOSTS:
            return None
        path = unquote(parsed.path)
    elif parsed.scheme or raw_url.startswith("//"):
        return None
    else:
        path = unquote(parsed.path)
    if not path:
        target = source
    elif path.startswith("/"):
        target = ROOT / path.lstrip("/")
    else:
        target = source.parent / path
    if path.endswith("/") or (target.exists() and target.is_dir()):
        target /= "index.html"
    return target.resolve(), unquote(parsed.fragment)


def validate_mailto(url: str) -> str | None:
    parsed = urlsplit(url)
    addresses = unquote(parsed.path)
    if not addresses or any(char.isspace() for char in addresses):
        return "invalid mail recipient"
    for address in addresses.split(","):
        if not re.fullmatch(r"[^@,\s]+@[^@,\s]+\.[^@,\s]+", address):
            return f"invalid mail recipient: {address}"
    if "\n" in url or "\r" in url:
        return "literal newline in mail link"
    return None


def validate_download(path: Path) -> str | None:
    suffix = path.suffix.lower()
    try:
        data = path.read_bytes()
    except OSError as error:
        return str(error)
    if suffix == ".pdf" and not data.startswith(b"%PDF-"):
        return "invalid PDF signature"
    if suffix == ".ics":
        text = data.decode("utf-8-sig", errors="replace")
        required = ("BEGIN:VCALENDAR", "VERSION:2.0", "BEGIN:VEVENT", "END:VEVENT", "END:VCALENDAR")
        missing = [item for item in required if item not in text]
        if missing:
            return "invalid calendar file; missing " + ", ".join(missing)
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="link-audit-report.md")
    args = parser.parse_args()
    pages = public_pages()
    parsed_pages: dict[Path, PageParser] = {}
    findings: list[str] = []
    checked = 0

    for page in pages:
        parsed = PageParser()
        parsed.feed(page.read_text(encoding="utf-8", errors="replace"))
        parsed_pages[page.resolve()] = parsed

    for page, parsed in parsed_pages.items():
        rel = page.relative_to(ROOT)
        for tag, attrs, line in parsed.links:
            url = attrs.get("href") or attrs.get("src") or ""
            checked += 1
            if url.startswith(("data:", "tel:", "javascript:")):
                continue
            if url.startswith("mailto:"):
                problem = validate_mailto(url)
                if problem:
                    findings.append(f"`{rel}:{line}` {problem}: `{url}`")
                continue
            split = urlsplit(url)
            if split.scheme in {"http", "https"} and split.hostname not in LOCAL_HOSTS:
                if tag in {"a", "area"} and attrs.get("target") == "_blank":
                    rel_values = set(attrs.get("rel", "").lower().split())
                    if "noopener" not in rel_values:
                        findings.append(f"`{rel}:{line}` external new-window link is missing `noopener`: `{url}`")
                continue
            resolved = local_path(page, url)
            if not resolved:
                continue
            target, fragment = resolved
            try:
                target.relative_to(ROOT)
            except ValueError:
                findings.append(f"`{rel}:{line}` link escapes the site root: `{url}`")
                continue
            if not target.exists() or not target.is_file():
                findings.append(f"`{rel}:{line}` missing internal target: `{url}`")
                continue
            download_problem = validate_download(target)
            if download_problem:
                findings.append(f"`{rel}:{line}` {download_problem}: `{url}`")
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed_pages.get(target)
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8", errors="replace"))
                    parsed_pages[target] = target_parser
                if fragment not in target_parser.ids:
                    findings.append(f"`{rel}:{line}` missing fragment `#{fragment}` in `{target.relative_to(ROOT)}`")

    report = ROOT / args.report
    lines = [
        "# Link and action audit",
        "",
        f"- Public pages: {len(pages)}",
        f"- References checked: {checked}",
        f"- Findings: {len(findings)}",
        "",
    ]
    if findings:
        lines += ["## Findings", ""] + [f"- {item}" for item in findings]
    else:
        lines += ["No broken internal targets, fragments, PDF signatures, calendar structures, mail recipients or unsafe external new-window links were found.", ""]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Checked {len(pages)} pages and {checked} references: {len(findings)} findings")
    print(f"Report: {report}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
