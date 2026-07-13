#!/usr/bin/env python3
"""Check that every public page uses the canonical Local 083 header/footer shell."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from public_pages import ROOT, public_html_paths


EXPECTED_NAV = [
    ("About", "/about.html"),
    ("Events", "/events.html"),
    ("News", "/news.html"),
    ("Resources & Rights", "/resources.html"),
    ("Leadership", "/leadership.html"),
    ("Contact", "/contact.html"),
]
REQUIRED_FOOTER_LINKS = {
    "/resources.html": "Resources & Rights",
    "/contact.html": "Contact us",
    "/privacy.html": "Privacy notice",
    "/privacy.html#analytics-controls": "Tracking settings",
    "mailto:083execteam@seiu503.org": "Executive team email",
    "mailto:083stewards@seiu503.org": "Steward team email",
}


@dataclass
class Finding:
    page: str
    message: str


class ShellParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.primary_nav_level: int | None = None
        self.current_link: dict | None = None
        self.primary_links: list[tuple[str, str]] = []
        self.footer_links: list[tuple[str, str]] = []
        self.footer_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        in_header = "header" in self.stack or tag == "header"
        in_footer = "footer" in self.stack or tag == "footer"
        if in_header and tag == "nav" and values.get("aria-label") == "Primary navigation":
            self.primary_nav_level = len(self.stack)
        if tag == "a" and (self.primary_nav_level is not None or in_footer):
            self.current_link = {
                "href": str(values.get("href") or ""),
                "text": "",
                "context": "primary" if self.primary_nav_level is not None else "footer",
            }
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.current_link:
            record = (normalize_text(self.current_link["text"]), self.current_link["href"])
            (self.primary_links if self.current_link["context"] == "primary" else self.footer_links).append(record)
            self.current_link = None
        if self.primary_nav_level is not None and tag == "nav" and len(self.stack) - 1 == self.primary_nav_level:
            self.primary_nav_level = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self.current_link:
            self.current_link["text"] += data
        if "footer" in self.stack:
            self.footer_text += " " + data


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def audit_page(path: Path, root: Path = ROOT) -> list[Finding]:
    rel = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    parser = ShellParser()
    parser.feed(source)
    findings: list[Finding] = []

    menu_script_count = source.count("<script data-site-shell-menu-state-script>")
    if menu_script_count != 1:
        findings.append(
            Finding(
                rel,
                f"Expected exactly one canonical mobile-menu state script; found {menu_script_count}",
            )
        )

    if not parser.primary_links:
        findings.append(Finding(rel, "Missing nav with aria-label=\"Primary navigation\" inside the header"))
    else:
        found_nav = [(text, href) for text, href in parser.primary_links if any(text == label for label, _ in EXPECTED_NAV)]
        if found_nav != EXPECTED_NAV:
            findings.append(Finding(rel, f"Primary navigation differs from canonical order/targets: {found_nav!r}"))

    footer_text = normalize_text(parser.footer_text)
    for phrase in ("SEIU Local 503", "Oregon State University"):
        if phrase not in footer_text:
            findings.append(Finding(rel, f"Footer is missing brand text: {phrase}"))
    footer_hrefs = {href for _, href in parser.footer_links}
    for href, label in REQUIRED_FOOTER_LINKS.items():
        if href not in footer_hrefs:
            findings.append(Finding(rel, f"Footer is missing {label} link: {href}"))
    return findings


def run(root: Path = ROOT) -> tuple[list[Path], list[Finding]]:
    pages = public_html_paths(root, include_404=True)
    return pages, [finding for page in pages for finding in audit_page(page, root)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="shell-consistency-report.md")
    args = parser.parse_args()
    pages, findings = run(ROOT)
    lines = [
        "# Public shell consistency report",
        "",
        f"- Public pages checked: {len(pages)}",
        f"- Findings: {len(findings)}",
        "- Intentional exception: `404.html` is audited because visitors see it, but it is excluded from the sitemap.",
        "",
    ]
    if findings:
        lines.extend(["## Findings", ""])
        lines.extend(f"- `{finding.page}`: {finding.message}" for finding in findings)
    else:
        lines.append("All public pages use the canonical header navigation and required footer elements.")
    report = ROOT / args.report
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Checked {len(pages)} public page shells: {len(findings)} findings")
    print(f"Report: {report}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
