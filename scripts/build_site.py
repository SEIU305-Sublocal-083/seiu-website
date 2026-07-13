#!/usr/bin/env python3
"""Build every committed static artifact from its source data."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED_PATHS = [
    "index.html",
    "news.html",
    "events.html",
    "feed.xml",
    "news/rss.xml",
    "events/rss.xml",
    "sitemap.xml",
    "robots.txt",
    "styles/tailwind.css",
]


def run(command: list[str]) -> None:
    print(f"+ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def snapshot(paths: list[str]) -> dict[str, bytes | None]:
    return {
        path: (ROOT / path).read_bytes() if (ROOT / path).exists() else None
        for path in paths
    }


def restore(files: dict[str, bytes | None]) -> None:
    for relative, content in files.items():
        path = ROOT / relative
        if content is None:
            path.unlink(missing_ok=True)
        else:
            path.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if rebuilding changes a generated file, then restore it.")
    parser.add_argument("--skip-css", action="store_true", help="Skip Tailwind compilation (intended for focused generator tests).")
    args = parser.parse_args()

    paths = [path for path in GENERATED_PATHS if not args.skip_css or path != "styles/tailwind.css"]
    before = snapshot(paths) if args.check else {}

    try:
        run(["python3", "scripts/generate_static_content.py"])
        run(["python3", "scripts/generate_rss.py"])
        run(["python3", "scripts/generate_sitemap.py"])
        shell_command = ["python3", "scripts/sync_site_shell.py"]
        if args.check:
            shell_command.append("--check")
        run(shell_command)
        if not args.skip_css:
            run(["bash", "scripts/build_css.sh"])
    except subprocess.CalledProcessError as error:
        if args.check:
            restore(before)
        print(f"Site build stopped because a build step failed ({error.returncode}).", file=sys.stderr)
        return error.returncode or 1
    except BaseException:
        if args.check:
            restore(before)
        raise
    if args.check:
        after = snapshot(paths)
        changed = [path for path in paths if before[path] != after[path]]
        restore(before)
        if changed:
            print("Generated site files are out of date:", file=sys.stderr)
            for path in changed:
                print(f"- {path}", file=sys.stderr)
            print("Run `python3 scripts/build_site.py` and commit the results.", file=sys.stderr)
            return 1
    print("Site build complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
