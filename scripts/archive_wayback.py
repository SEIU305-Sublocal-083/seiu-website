#!/usr/bin/env python3
"""Submit sitemap URLs to the Internet Archive Save Page Now endpoint."""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


DEFAULT_USER_AGENT = "SEIU-Local-083-Wayback-Archiver/1.0 (+https://www.local083.org)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive URLs from a sitemap using Wayback Machine Save Page Now."
    )
    parser.add_argument("--sitemap", default="sitemap.xml", help="Path to sitemap XML file.")
    parser.add_argument(
        "--max-urls",
        type=int,
        default=0,
        help="Maximum number of URLs to submit (0 = all).",
    )
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=5.0,
        help="Delay between submissions in seconds.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=30.0,
        help="HTTP timeout per request in seconds.",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="User-Agent header for Save Page Now requests.",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with non-zero status if any submission fails.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print URLs without submitting to Wayback.",
    )
    return parser.parse_args()


def load_urls(sitemap_path: Path) -> list[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    urls: list[str] = []
    seen: set[str] = set()
    for loc in root.findall(".//{*}loc"):
        if loc.text is None:
            continue
        url = loc.text.strip()
        if not url or url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def submit_url(url: str, user_agent: str, timeout_seconds: float) -> tuple[bool, str]:
    encoded_target = urllib.parse.quote(url, safe="")
    save_url = f"https://web.archive.org/save/{encoded_target}"
    request = urllib.request.Request(
        save_url,
        method="GET",
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            status = response.getcode()
            if 200 <= status < 400:
                return True, f"HTTP {status}"
            return False, f"HTTP {status}"
    except urllib.error.HTTPError as err:
        return False, f"HTTP {err.code}"
    except urllib.error.URLError as err:
        return False, f"URL error: {err.reason}"
    except TimeoutError:
        return False, "Timeout"


def main() -> int:
    args = parse_args()
    sitemap_path = Path(args.sitemap)
    if not sitemap_path.exists():
        print(f"ERROR: sitemap not found: {sitemap_path}", file=sys.stderr)
        return 2

    urls = load_urls(sitemap_path)
    if args.max_urls > 0:
        urls = urls[: args.max_urls]

    if not urls:
        print("No URLs found in sitemap.")
        return 0

    print(
        f"Submitting {len(urls)} URL(s) from {sitemap_path} "
        f"(delay={args.delay_seconds}s, dry_run={args.dry_run})"
    )

    success_count = 0
    failure_count = 0

    for index, url in enumerate(urls, start=1):
        if args.dry_run:
            print(f"[{index}/{len(urls)}] DRY RUN {url}")
            success_count += 1
        else:
            ok, detail = submit_url(url, args.user_agent, args.timeout_seconds)
            status = "OK" if ok else "FAIL"
            print(f"[{index}/{len(urls)}] {status} {url} ({detail})")
            if ok:
                success_count += 1
            else:
                failure_count += 1

        if index < len(urls) and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)

    print(
        f"Done. succeeded={success_count} failed={failure_count} total={len(urls)}"
    )

    if failure_count > 0 and args.fail_on_error:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
