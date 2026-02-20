#!/usr/bin/env python3
"""Validate public site content for broken links and incomplete content markers."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

PUBLIC_HTML_GLOBS = ["*.html", "news/*.html", "events/*.html", "resources/*.html", "2026-bargaining/*.html"]

EXCLUDED_HTML_PATTERNS = (
    "test-pages/",
    "jules-scratch/",
    "/template.html",
    "redirect-time-change-template.html",
    "news/ba-template.html",
    "news/spotlight-template.html",
    "marketing/",
)

# Keep this list narrow to avoid noisy false positives.
PLACEHOLDER_PATTERNS = (
    re.compile(r"\\blorem ipsum\\b", re.IGNORECASE),
    re.compile(r"\\bTODO\\b"),
    re.compile(r"\\bTBD\\b"),
    re.compile(r"\\bplaceholder\\b", re.IGNORECASE),
    re.compile(r"\\[\\s*insert[^\\]]*\\]", re.IGNORECASE),
)

REQUIRED_NEWS_FIELDS = ("title", "description", "url", "image", "alt", "publishedAt")
REQUIRED_EVENT_FIELDS = ("date", "time", "title", "description", "type", "url", "location_detail")


@dataclass
class Issue:
    level: str  # ERROR | WARN
    source: str
    message: str


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        for attr in ("href", "src"):
            value = attrs_dict.get(attr)
            if value:
                self.links.append(value.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public content quality.")
    parser.add_argument(
        "--report",
        default="site-quality-report.md",
        help="Output markdown report path (repo-relative).",
    )
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Treat placeholder content markers as errors.",
    )
    return parser.parse_args()


def is_excluded_html(path: Path) -> bool:
    value = path.as_posix()
    return any(pattern in value for pattern in EXCLUDED_HTML_PATTERNS)


def collect_public_html() -> list[Path]:
    pages: set[Path] = set()
    for pattern in PUBLIC_HTML_GLOBS:
        for candidate in ROOT.glob(pattern):
            if candidate.is_file() and not is_excluded_html(candidate.relative_to(ROOT)):
                pages.add(candidate)
    return sorted(pages)


def is_ignorable_url(url: str) -> bool:
    if not url:
        return True
    if url.startswith("#"):
        return True
    for prefix in ("mailto:", "tel:", "javascript:", "data:"):
        if url.startswith(prefix):
            return True
    return False


def resolve_internal_target(url: str, base_file: Path) -> Path | None:
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https"):
        if parsed.netloc not in ("www.local083.org", "local083.org"):
            return None
        path_part = parsed.path
    else:
        path_part = parsed.path

    if not path_part:
        return None

    if path_part.startswith("/"):
        target = ROOT / path_part.lstrip("/")
    else:
        target = base_file.parent / path_part

    return target


def candidate_paths(path: Path) -> Iterable[Path]:
    yield path

    as_text = path.as_posix()
    if as_text.endswith("/"):
        yield path / "index.html"
    elif path.suffix == "":
        yield Path(as_text + ".html")
        yield path / "index.html"


def path_exists(path: Path) -> bool:
    return any(candidate.exists() for candidate in candidate_paths(path))


def check_html_links(pages: list[Path]) -> list[Issue]:
    issues: list[Issue] = []

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        parser = LinkExtractor()
        parser.feed(page.read_text(encoding="utf-8"))

        for link in parser.links:
            if is_ignorable_url(link):
                continue

            target = resolve_internal_target(link, page)
            if target is None:
                continue

            if not path_exists(target):
                issues.append(
                    Issue(
                        level="ERROR",
                        source=rel,
                        message=f"Broken internal link: {link}",
                    )
                )

    return issues


def find_placeholder_issues(pages: list[Path], strict: bool) -> list[Issue]:
    issues: list[Issue] = []
    level = "ERROR" if strict else "WARN"

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                issues.append(
                    Issue(
                        level=level,
                        source=rel,
                        message=f"Possible unfinished content marker found ({pattern.pattern})",
                    )
                )

    return issues


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def require_fields(item: dict, fields: tuple[str, ...], source: str) -> list[Issue]:
    issues: list[Issue] = []
    for field in fields:
        value = item.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(Issue("ERROR", source, f"Missing or empty required field: {field}"))
    return issues


def check_news_json() -> list[Issue]:
    issues: list[Issue] = []
    path = ROOT / "news" / "news.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for idx, item in enumerate(data):
        source = f"news/news.json[{idx}]"
        issues.extend(require_fields(item, REQUIRED_NEWS_FIELDS, source))

        url = item.get("url", "")
        if isinstance(url, str) and url.startswith("/"):
            if not path_exists(ROOT / url.lstrip("/")):
                issues.append(Issue("ERROR", source, f"News URL not found: {url}"))

        image = item.get("image", "")
        if isinstance(image, str) and image.startswith("/"):
            if not path_exists(ROOT / image.lstrip("/")):
                issues.append(Issue("ERROR", source, f"News image not found: {image}"))

        for date_key in ("publishedAt", "createdAt", "updatedAt"):
            date_value = item.get(date_key)
            if isinstance(date_value, str) and date_value.strip() and not is_valid_date(date_value):
                issues.append(Issue("ERROR", source, f"Invalid {date_key} date format: {date_value}"))

    return issues


def check_events_json() -> list[Issue]:
    issues: list[Issue] = []
    path = ROOT / "events" / "events.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    for idx, item in enumerate(data):
        source = f"events/events.json[{idx}]"
        issues.extend(require_fields(item, REQUIRED_EVENT_FIELDS, source))

        date_value = item.get("date", "")
        if isinstance(date_value, str) and date_value.strip() and not is_valid_date(date_value):
            issues.append(Issue("ERROR", source, f"Invalid event date format: {date_value}"))

        url = item.get("url", "")
        if isinstance(url, str) and url.startswith("/"):
            if not path_exists(ROOT / url.lstrip("/")):
                issues.append(Issue("ERROR", source, f"Event URL not found: {url}"))

        calendar_link = item.get("calendar_link")
        if isinstance(calendar_link, str) and calendar_link.strip().startswith("/"):
            if not path_exists(ROOT / calendar_link.lstrip("/")):
                issues.append(Issue("ERROR", source, f"Calendar file not found: {calendar_link}"))

    return issues


def write_report(path: Path, issues: list[Issue]) -> None:
    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARN"]

    lines = [
        "# Site Quality Report",
        "",
        f"Generated: {datetime.now(UTC).isoformat().replace('+00:00', 'Z')}",
        "",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]

    if not issues:
        lines.append("No issues found.")
    else:
        lines.append("## Findings")
        lines.append("")
        for issue in issues:
            lines.append(f"- [{issue.level}] `{issue.source}`: {issue.message}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    pages = collect_public_html()

    issues: list[Issue] = []
    issues.extend(check_html_links(pages))
    issues.extend(find_placeholder_issues(pages, strict=args.strict_placeholders))
    issues.extend(check_news_json())
    issues.extend(check_events_json())

    report_path = ROOT / args.report
    write_report(report_path, issues)

    errors = [i for i in issues if i.level == "ERROR"]
    warnings = [i for i in issues if i.level == "WARN"]
    print(f"Checked {len(pages)} public HTML page(s).")
    print(f"Report: {report_path}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
