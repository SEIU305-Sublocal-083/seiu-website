#!/usr/bin/env python3
"""Static accessibility checks for Local 083 public HTML.

This complements, but does not replace, rendered axe, screen-reader, keyboard,
zoom, contrast and real-device testing.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from public_pages import public_html_paths


ROOT = Path(__file__).resolve().parent.parent
@dataclass
class Issue:
    level: str
    page: str
    message: str


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_attrs: dict[str, str | None] = {}
        self.ids: list[str] = []
        self.refs: list[tuple[str, str]] = []
        self.fragment_links: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.inputs: list[tuple[str, dict[str, str | None], bool]] = []
        self.labels_for: set[str] = set()
        self.buttons: list[dict] = []
        self.summaries = 0
        self.details = 0
        self.main_count = 0
        self.h1_count = 0
        self.title_count = 0
        self.title_text = ""
        self.viewport = False
        self.skip_to_main = False
        self.external_blank: list[dict[str, str | None]] = []
        self.stack: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        self.stack.append((tag, data))
        if tag == "html":
            self.html_attrs = data
        if data.get("id"):
            self.ids.append(str(data["id"]))
        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            for ref in str(data.get(name) or "").split():
                self.refs.append((name, ref))
        if tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_count += 1
        elif tag == "meta" and str(data.get("name") or "").lower() == "viewport":
            self.viewport = True
        elif tag == "img":
            self.images.append(data)
        elif tag in {"input", "select", "textarea"}:
            inside_label = any(parent == "label" for parent, _ in self.stack[:-1])
            self.inputs.append((tag, data, inside_label))
        elif tag == "label" and data.get("for"):
            self.labels_for.add(str(data["for"]))
        elif tag == "button":
            self.buttons.append({"attrs": data, "text": ""})
        elif tag == "details":
            self.details += 1
        elif tag == "summary":
            self.summaries += 1
        elif tag == "a":
            href = str(data.get("href") or "")
            if href.startswith("#") and len(href) > 1:
                self.fragment_links.append(href[1:])
                if href == "#main-content":
                    self.skip_to_main = True
            parsed = urlparse(href)
            if data.get("target") == "_blank" and parsed.scheme in {"http", "https"}:
                self.external_blank.append(data)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if any(tag == "title" for tag, _ in self.stack):
            self.title_text += data
        if self.buttons and any(tag == "button" for tag, _ in self.stack):
            self.buttons[-1]["text"] += data


def pages() -> list[Path]:
    return public_html_paths(ROOT, include_404=True)


def audit(path: Path) -> list[Issue]:
    rel = path.relative_to(ROOT).as_posix()
    parser = AuditParser()
    parser.feed(path.read_text(encoding="utf-8"))
    issues: list[Issue] = []

    def add(level: str, message: str) -> None:
        issues.append(Issue(level, rel, message))

    if not parser.html_attrs.get("lang"):
        add("ERROR", "Missing html lang attribute")
    if not parser.viewport:
        add("ERROR", "Missing viewport meta tag")
    if parser.title_count != 1 or not parser.title_text.strip():
        add("ERROR", f"Expected one nonempty title; found {parser.title_count}")
    if parser.main_count != 1:
        add("ERROR", f"Expected one main landmark; found {parser.main_count}")
    if parser.h1_count != 1:
        add("ERROR", f"Expected one h1; found {parser.h1_count}")
    if not parser.skip_to_main:
        add("WARN", "No skip link to #main-content")

    duplicates = [value for value, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        add("ERROR", f"Duplicate IDs: {', '.join(sorted(duplicates))}")
    known_ids = set(parser.ids)
    for name, ref in parser.refs:
        if ref not in known_ids:
            add("ERROR", f"{name} references missing ID: {ref}")
    for ref in parser.fragment_links:
        if ref not in known_ids:
            add("ERROR", f"Fragment link references missing ID: {ref}")

    for index, image in enumerate(parser.images, start=1):
        if "alt" not in image:
            add("ERROR", f"Image {index} is missing alt (src={image.get('src', '')})")
        if not image.get("width") or not image.get("height"):
            add("WARN", f"Image {index} lacks intrinsic dimensions (src={image.get('src', '')})")

    for index, (tag, control, inside_label) in enumerate(parser.inputs, start=1):
        if tag == "input" and control.get("type") in {"hidden", "submit", "button", "reset"}:
            continue
        labelled = inside_label or (control.get("id") in parser.labels_for) or control.get("aria-label") or control.get("aria-labelledby")
        if not labelled:
            add("ERROR", f"Form control {index} has no accessible label ({tag} id={control.get('id', '')})")

    for index, button in enumerate(parser.buttons, start=1):
        attrs = button["attrs"]
        if not button["text"].strip() and not attrs.get("aria-label") and not attrs.get("aria-labelledby") and not attrs.get("title"):
            add("ERROR", f"Button {index} has no accessible name")
    if parser.details != parser.summaries:
        add("ERROR", f"Found {parser.details} details elements but {parser.summaries} summaries")
    for link in parser.external_blank:
        rel_tokens = set(str(link.get("rel") or "").lower().split())
        if "noopener" not in rel_tokens:
            add("ERROR", f"External target=_blank link lacks noopener: {link.get('href', '')}")
    return issues


def main() -> int:
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("--report", default="accessibility-report.md")
    args = arg_parser.parse_args()
    checked = pages()
    issues = [issue for page in checked for issue in audit(page)]
    errors = [issue for issue in issues if issue.level == "ERROR"]
    warnings = [issue for issue in issues if issue.level == "WARN"]
    lines = ["# Static Accessibility Report", "", f"- Pages checked: {len(checked)}", f"- Errors: {len(errors)}", f"- Warnings: {len(warnings)}", "", "> This structural audit does not replace rendered axe, contrast, keyboard, screen-reader, zoom or real-device testing.", ""]
    if issues:
        lines.extend(["## Findings", ""])
        lines.extend(f"- [{issue.level}] `{issue.page}`: {issue.message}" for issue in issues)
    else:
        lines.append("No structural accessibility issues found.")
    (ROOT / args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Checked {len(checked)} pages: {len(errors)} errors, {len(warnings)} warnings")
    print(f"Report: {ROOT / args.report}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
