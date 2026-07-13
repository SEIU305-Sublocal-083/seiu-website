#!/usr/bin/env python3
"""Synchronize the canonical Local 083 header and footer across public pages.

The page body between the site header and footer is intentionally left alone.
On the first run, the script replaces only a header before the first ``<main>``
and the final footer. Subsequent runs update the explicitly marked regions.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from public_pages import ROOT, public_html_paths


HEADER_START = "<!-- SITE SHELL: HEADER START -->"
HEADER_END = "<!-- SITE SHELL: HEADER END -->"
FOOTER_START = "<!-- SITE SHELL: FOOTER START -->"
FOOTER_END = "<!-- SITE SHELL: FOOTER END -->"

NAV_ITEMS = (
    ("About", "/about.html", "about"),
    ("Events", "/events.html", "events"),
    ("News", "/news.html", "news"),
    ("Resources & Rights", "/resources.html", "resources"),
    ("Leadership", "/leadership.html", "leadership"),
    ("Contact", "/contact.html", "contact"),
)

MARKED_HEADER_RE = re.compile(
    rf"{re.escape(HEADER_START)}.*?{re.escape(HEADER_END)}", re.DOTALL
)
MARKED_FOOTER_RE = re.compile(
    rf"{re.escape(FOOTER_START)}.*?{re.escape(FOOTER_END)}", re.DOTALL
)
BODY_RE = re.compile(r"<body\b[^>]*>", re.IGNORECASE)
MAIN_RE = re.compile(r"<main\b", re.IGNORECASE)
HEAD_END_RE = re.compile(r"</head\s*>", re.IGNORECASE)
STYLE_RE = re.compile(r"<style\b", re.IGNORECASE)
TAILWIND_LINK_RE = re.compile(
    r"<link\b[^>]*href=[\"']/styles/tailwind\.css[\"'][^>]*>", re.IGNORECASE
)
SHELL_STYLES_LINK_RE = re.compile(
    r"<link\b[^>]*href=[\"']/styles/site-shell\.css[\"'][^>]*>", re.IGNORECASE
)
MOBILE_HANDLER_RE = re.compile(
    r"(?:mobileMenuButton|menuButton)\.addEventListener\s*\(\s*['\"]click['\"]",
    re.IGNORECASE,
)


def active_section(relative_path: str) -> str | None:
    """Return the main-navigation section for a public path."""

    first = relative_path.split("/", 1)[0]
    if first in {"events", "news", "resources"}:
        return first
    stem = Path(relative_path).stem
    if "/" not in relative_path and stem in {"about", "leadership", "contact"}:
        return stem
    return None


def nav_link(label: str, href: str, key: str, active: str | None, *, mobile: bool) -> str:
    current = key == active
    if mobile:
        classes = (
            "block text-center py-3 px-6 text-lg text-brand-purple "
            "bg-brand-purple-light font-semibold"
            if current
            else "block text-center py-3 px-6 text-lg text-text-secondary hover:bg-brand-purple-light"
        )
    else:
        classes = (
            "text-brand-purple font-bold"
            if current
            else "text-text-secondary hover:text-brand-purple transition-colors"
        )
    aria = ' aria-current="page"' if current else ""
    escaped_label = label.replace("&", "&amp;")
    return f'<a href="{href}" class="{classes}"{aria}>{escaped_label}</a>'


def render_header(relative_path: str, *, needs_menu_script: bool) -> str:
    active = active_section(relative_path)
    desktop = "\n".join(
        f"                {nav_link(label, href, key, active, mobile=False)}"
        for label, href, key in NAV_ITEMS
    )
    mobile = "\n".join(
        f"            {nav_link(label, href, key, active, mobile=True)}"
        for label, href, key in NAV_ITEMS
    )
    onclick = ""
    toggle_function = ""
    if needs_menu_script:
        onclick = ' onclick="siteShellToggleMenu(this)"'
        toggle_function = """
        function siteShellToggleMenu(button) {
            const menu = document.getElementById('mobile-menu');
            if (!menu) return;
            menu.classList.toggle('hidden');
            if (window.siteShellSyncMenuState) window.siteShellSyncMenuState();
        }
"""
    # Legacy pages retain their existing toggle listener, but one canonical
    # state synchronizer keeps the button's accessible name/state and icon in
    # step with either the `hidden` or `is-open` menu convention. Observing the
    # menu class avoids attaching a second click listener and double-toggling.
    menu_script = f"""
    <script data-site-shell-menu-state-script>
        (() => {{
            const button = document.getElementById('mobile-menu-button');
            const menu = document.getElementById('mobile-menu');
            if (!button || !menu) return;
            const canonicalIcon = button.innerHTML;

            window.siteShellSyncMenuState = () => {{
                const isOpen = menu.classList.contains('is-open') || !menu.classList.contains('hidden');
                button.setAttribute('aria-expanded', String(isOpen));
                button.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
                if (button.innerHTML !== canonicalIcon) button.innerHTML = canonicalIcon;
            }};

            new MutationObserver(window.siteShellSyncMenuState).observe(menu, {{
                attributes: true,
                attributeFilter: ['class']
            }});
            document.addEventListener('keydown', (event) => {{
                if (event.key !== 'Escape' || button.getAttribute('aria-expanded') !== 'true') return;
                menu.classList.add('hidden');
                menu.classList.remove('is-open');
                window.siteShellSyncMenuState();
                button.focus();
            }});
            window.siteShellSyncMenuState();
        }})();
{toggle_function}    </script>"""
    return f"""{HEADER_START}
    <header class="bg-white/80 backdrop-blur-lg border-b border-border-color sticky top-0 z-50" data-site-shell-header>
        <nav class="container mx-auto px-6 py-4 flex justify-between items-center" aria-label="Primary navigation">
            <a href="/index.html" class="flex items-center space-x-2">
                <span class="text-2xl font-bold text-brand-purple-dark">SEIU 503</span>
                <span class="text-lg text-text-secondary hidden md:block">| Oregon State University</span>
            </a>
            <div class="hidden lg:flex space-x-8">
{desktop}
            </div>
            <button type="button" id="mobile-menu-button" class="lg:hidden text-text-secondary hover:text-brand-purple" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false"{onclick}>
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
            </button>
        </nav>
        <div id="mobile-menu" class="hidden lg:hidden absolute top-full left-0 w-full bg-white border-t border-border-color shadow-lg" role="navigation" aria-label="Mobile navigation">
{mobile}
        </div>
    </header>{menu_script}
{HEADER_END}"""


def render_footer(relative_path: str) -> str:
    privacy_current = ' aria-current="page"' if relative_path == "privacy.html" else ""
    return f"""{FOOTER_START}
    <footer class="bg-gray-100 pt-12 pb-8 text-text-primary border-t border-gray-200" data-site-shell-footer>
        <div class="container mx-auto px-6">
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div class="md:col-span-2 lg:col-span-1">
                    <div class="flex items-center mb-4">
                        <img src="/images/logo.png" alt="SEIU 503 logo" class="h-12 w-12 mr-3 bg-white p-1 rounded" width="48" height="48" loading="lazy" decoding="async">
                        <div><h3 class="text-xl font-bold">SEIU Local 503</h3><p class="text-text-secondary text-sm">Oregon State University</p></div>
                    </div>
                    <p class="text-text-secondary leading-relaxed">Our member-led union represents classified staff at Oregon State University. Together, we bargain fair contracts, defend our rights and build power at work.</p>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4 tracking-wider uppercase">Quick links</h4>
                    <ul class="space-y-3">
                        <li><a href="/about.html" class="text-text-secondary hover:text-brand-purple transition-colors">About our union</a></li>
                        <li><a href="/events.html" class="text-text-secondary hover:text-brand-purple transition-colors">Events</a></li>
                        <li><a href="/news.html" class="text-text-secondary hover:text-brand-purple transition-colors">News</a></li>
                        <li><a href="/leadership.html" class="text-text-secondary hover:text-brand-purple transition-colors">Leadership</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4 tracking-wider uppercase"><a href="/resources.html" class="hover:text-brand-purple transition-colors">Resources</a></h4>
                    <ul class="space-y-3">
                        <li><a href="/resources.html" class="text-text-secondary hover:text-brand-purple transition-colors">Resources &amp; Rights</a></li>
                        <li><a href="/resources/seiu_cba_2022-2026.pdf" class="text-text-secondary hover:text-brand-purple transition-colors">Our Contract (PDF)</a></li>
                        <li><a href="/resources/stewards.html" class="text-text-secondary hover:text-brand-purple transition-colors">Find a Steward</a></li>
                        <li><a href="/resources/weingarten-rights.html" class="text-text-secondary hover:text-brand-purple transition-colors">Weingarten Rights</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-lg font-semibold mb-4 tracking-wider uppercase"><a href="/contact.html" class="hover:text-brand-purple transition-colors">Contact us</a></h4>
                    <ul class="space-y-3">
                        <li><a href="mailto:083execteam@seiu503.org" class="text-text-secondary hover:text-brand-purple transition-colors break-all">083execteam@seiu503.org</a></li>
                        <li><a href="mailto:083stewards@seiu503.org" class="text-text-secondary hover:text-brand-purple transition-colors break-all">083stewards@seiu503.org</a></li>
                    </ul>
                </div>
            </div>
            <div class="mt-10 pt-8 border-t border-gray-300 text-center space-y-2">
                <p class="text-text-secondary text-sm">&copy; 2026 SEIU Local 503, Local 083. All rights reserved.</p>
                <p class="text-text-secondary text-xs"><a class="underline hover:text-brand-purple" href="/privacy.html#analytics-controls">Tracking settings</a><span aria-hidden="true"> · </span><a class="underline hover:text-brand-purple" href="/privacy.html"{privacy_current}>Privacy notice</a></p>
            </div>
        </div>
    </footer>
{FOOTER_END}"""


def element_span(source: str, tag: str, start: int = 0, end: int | None = None, *, last: bool = False) -> tuple[int, int] | None:
    """Locate a balanced HTML element without relying on indentation."""

    boundary = len(source) if end is None else end
    opener_re = re.compile(rf"<{tag}\b[^>]*>", re.IGNORECASE)
    openers = list(opener_re.finditer(source, start, boundary))
    if not openers:
        return None
    opener = openers[-1] if last else openers[0]
    token_re = re.compile(rf"</?{tag}\b[^>]*>", re.IGNORECASE)
    depth = 0
    for token in token_re.finditer(source, opener.start()):
        if token.group(0).lstrip().startswith("</"):
            depth -= 1
            if depth == 0:
                return opener.start(), token.end()
        elif not token.group(0).rstrip().endswith("/>"):
            depth += 1
    return None


def ensure_shell_styles(source: str) -> str:
    links: list[str] = []
    if not TAILWIND_LINK_RE.search(source):
        links.append('    <link rel="stylesheet" href="/styles/tailwind.css">')
    if not SHELL_STYLES_LINK_RE.search(source):
        links.append('    <link rel="stylesheet" href="/styles/site-shell.css">')
    if not links:
        return source
    style = STYLE_RE.search(source)
    head_end = HEAD_END_RE.search(source)
    insert_at = style.start() if style else (head_end.start() if head_end else None)
    if insert_at is None:
        raise ValueError("Missing </head> while adding site shell stylesheets")
    return source[:insert_at] + "\n".join(links) + "\n" + source[insert_at:]


def add_shell_layout_attribute(source: str) -> str:
    body = BODY_RE.search(source)
    if not body or "data-site-shell-added" in body.group(0):
        return source
    tag = body.group(0)[:-1] + " data-site-shell-added>"
    return source[: body.start()] + tag + source[body.end() :]


def sync_source(source: str, relative_path: str) -> str:
    """Return source with only the public site shell synchronized."""

    source = ensure_shell_styles(source)
    had_marked_header = bool(MARKED_HEADER_RE.search(source))
    body = BODY_RE.search(source)
    if not body:
        raise ValueError("Missing <body> element")
    main = MAIN_RE.search(source, body.end())
    header_span = None if had_marked_header else element_span(
        source, "header", body.end(), main.start() if main else None
    )
    shell_less = not had_marked_header and header_span is None

    # Existing inline page scripts keep controlling menus on legacy pages.
    # Every page receives a state observer; shell-less redirect stubs also
    # receive the small scoped toggle function in the shell.
    stripped_for_handler_check = MARKED_HEADER_RE.sub("", source)
    needs_menu_script = not MOBILE_HANDLER_RE.search(stripped_for_handler_check)
    header = render_header(
        relative_path,
        needs_menu_script=needs_menu_script,
    )
    if had_marked_header:
        source = MARKED_HEADER_RE.sub(lambda _: header, source, count=1)
    elif header_span:
        source = source[: header_span[0]] + header + source[header_span[1] :]
    else:
        source = add_shell_layout_attribute(source)
        body = BODY_RE.search(source)
        assert body is not None
        main = MAIN_RE.search(source, body.end())
        insert_at = main.start() if main else body.end()
        source = source[:insert_at] + "\n    " + header + "\n\n    " + source[insert_at:]

    footer = render_footer(relative_path)
    if MARKED_FOOTER_RE.search(source):
        source = MARKED_FOOTER_RE.sub(lambda _: footer, source, count=1)
    else:
        footer_span = element_span(source, "footer", last=True)
        if footer_span:
            source = source[: footer_span[0]] + footer + source[footer_span[1] :]
        else:
            body_end = re.search(r"</body\s*>", source, re.IGNORECASE)
            if not body_end:
                raise ValueError("Missing </body> while adding footer")
            source = source[: body_end.start()] + "\n    " + footer + "\n" + source[body_end.start() :]
    # Some redirect stubs contained an indentation-only line where the shell
    # is inserted. Keep the generated diff clean without touching body copy.
    source = re.sub(
        rf"(?m)^[ \t]+(?=\n[ \t]*{re.escape(HEADER_START)})",
        "",
        source,
        count=1,
    )
    return source


def synchronize(root: Path, *, check: bool) -> tuple[list[Path], list[str]]:
    changed: list[Path] = []
    errors: list[str] = []
    for path in public_html_paths(root, include_404=True):
        relative_path = path.relative_to(root).as_posix()
        source = path.read_text(encoding="utf-8", errors="replace")
        try:
            updated = sync_source(source, relative_path)
        except ValueError as error:
            errors.append(f"{relative_path}: {error}")
            continue
        if updated != source:
            changed.append(path)
            if not check:
                path.write_text(updated, encoding="utf-8")
    return changed, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any public shell is out of date")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    changed, errors = synchronize(args.root.resolve(), check=args.check)
    action = "would update" if args.check else "updated"
    print(f"Site shell {action} {len(changed)} public page(s).")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if args.check and changed:
        for path in changed:
            print(path.relative_to(args.root.resolve()).as_posix())
    return 1 if errors or (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
