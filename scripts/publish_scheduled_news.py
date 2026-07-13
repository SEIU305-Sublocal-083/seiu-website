#!/usr/bin/env python3
"""Publish due Local 083 news in Oregon local time and rebuild the static site."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
NEWS_JSON = ROOT / "news" / "news.json"
OREGON_TZ = ZoneInfo("America/Los_Angeles")
BASE_URL = "https://www.local083.org"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report due stories without changing files.")
    parser.add_argument("--now", help="Override current time with an ISO timestamp for testing.")
    return parser.parse_args()


def local_now(value: str | None) -> datetime:
    if not value:
        return datetime.now(OREGON_TZ)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=OREGON_TZ)
    return parsed.astimezone(OREGON_TZ)


def due_on(article: dict) -> datetime:
    value = article.get("publishedAt", "")
    if len(value) == 10:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=OREGON_TZ)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(OREGON_TZ)


def remove_noindex(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"\s*<meta\s+name=[\"']robots[\"']\s+content=[\"'][^\"']*noindex[^\"']*[\"']\s*/?>\s*",
        "\n    ",
        source,
        count=1,
        flags=re.IGNORECASE,
    )
    if count != 1:
        raise RuntimeError(f"Expected one noindex robots tag in {path.relative_to(ROOT)}")
    path.write_text(updated, encoding="utf-8")


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    args = parse_args()
    now = local_now(args.now)
    news = json.loads(NEWS_JSON.read_text(encoding="utf-8"))
    due = [item for item in news if item.get("status") == "scheduled" and due_on(item) <= now]
    if not due:
        print(f"No scheduled news is due as of {now.isoformat()}")
        return 0

    print("Due for publication:")
    for item in due:
        print(f"- {item['publishedAt']}: {item['title']}")
    if args.dry_run:
        return 0

    for item in due:
        item["status"] = "published"
        page = ROOT / item["url"].lstrip("/")
        remove_noindex(page)

    NEWS_JSON.write_text(json.dumps(news, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run(["python3", "scripts/build_site.py"])
    run(["python3", "scripts/site_quality_check.py", "--strict-placeholders"])

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    rss = (ROOT / "news" / "rss.xml").read_text(encoding="utf-8")
    for item in due:
        absolute = f"{BASE_URL}{item['url']}"
        if absolute not in sitemap or absolute not in rss:
            raise RuntimeError(f"Published story missing from sitemap or RSS: {absolute}")
    print(f"Published {len(due)} scheduled story/stories at {now.isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
