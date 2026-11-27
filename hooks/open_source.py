"""Homepage PR list, built from the PR pages you add by hand.

Every post (a .md file directly in docs/) whose front matter has `pr:` is listed on
the homepage in place of the `<!-- OSS_PRS -->` marker, grouped by repository,
newest first. Nothing is fetched from GitHub: what you write is what is shown.

    pr: https://github.com/OWNER/REPO/pull/123
    status: merged          # merged | open | draft | closed (default: open)

Each post also gets a link to its PR at the top.
"""

from __future__ import annotations

import datetime as dt
import html
import logging

from mkdocs.utils import get_relative_url
from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.open_source")

PAGE = "index.md"
MARKER = "<!-- OSS_PRS -->"
STATUSES = ("merged", "open", "draft", "closed")
ENTRIES: list[dict] = []


def _parse(url: str) -> tuple[str, str] | None:
    """https://github.com/owner/repo/pull/123 -> ("owner/repo", "123")"""
    parts = url.strip().rstrip("/").split("/")
    if len(parts) >= 7 and parts[-2] == "pull":
        return f"{parts[-4]}/{parts[-3]}", parts[-1]
    return None


def on_files(files, config):
    ENTRIES.clear()
    for f in files:
        if not (f.src_uri.endswith(".md") and "/" not in f.src_uri and f.src_uri != PAGE):
            continue
        if not f.inclusion.is_included():
            continue
        with open(f.abs_src_path, encoding="utf-8") as fh:
            _, meta = get_data(fh.read())
        url = meta.get("pr")
        if not isinstance(url, str) or not _parse(url):
            continue
        status = str(meta.get("status", "open")).lower()
        if status not in STATUSES:
            log.info("%s: unknown status %r, showing as open", f.src_uri, status)
            status = "open"
        date = meta.get("date")
        ENTRIES.append({
            "file": f, "url": url, "status": status,
            "title": meta.get("title") or f.src_uri[:-3],
            "date": date if isinstance(date, (dt.date, dt.datetime)) else None,
        })
    ENTRIES.sort(key=lambda e: (e["date"] or dt.date.min), reverse=True)
    return files


def _render(here: str) -> str:
    if not ENTRIES:
        return '<div class="oss-empty">No pull requests here yet. First contributions are in progress.</div>'

    counts: dict[str, int] = {}
    repos: dict[str, list[dict]] = {}
    for e in ENTRIES:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        repos.setdefault(_parse(e["url"])[0], []).append(e)

    stats = "".join(f'<span class="oss-stat"><b>{counts[s]}</b> {s}</span>' for s in STATUSES if s in counts)
    out = [f'<div class="oss-stats"><span class="oss-stat"><b>{len(ENTRIES)}</b> PRs</span>'
           f'<span class="oss-stat"><b>{len(repos)}</b> repos</span>{stats}</div>']

    for repo, items in repos.items():
        r = html.escape(repo)
        out.append(f'<section class="oss-repo"><h2 id="{r.replace("/", "-")}">'
                   f'<a href="https://github.com/{r}">{r}</a></h2><ul class="oss-list">')
        for e in items:
            num = _parse(e["url"])[1]
            date = e["date"].strftime("%b %Y") if e["date"] else ""
            out.append(
                f'<li><span class="oss-badge oss-badge--{e["status"]}">{e["status"]}</span>'
                f'<a class="oss-title" href="{get_relative_url(e["file"].url, here)}">{html.escape(str(e["title"]))}</a>'
                f'<a class="oss-writeup" href="{html.escape(e["url"])}">PR #{num} ↗</a>'
                f'<span class="oss-meta">{date}</span></li>')
        out.append("</ul></section>")
    return "\n".join(out)


def on_page_markdown(markdown: str, page, config, files):
    if page.file.src_uri == PAGE:
        return markdown.replace(MARKER, _render(page.url))
    url = page.meta.get("pr")
    parsed = _parse(url) if isinstance(url, str) else None
    if parsed:
        return f'!!! abstract "Pull request"\n    [{parsed[0]}#{parsed[1]}]({url})\n\n' + markdown
    return markdown
