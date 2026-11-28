"""Homepage PR list, built from prs.yml.

Every entry in prs.yml is listed on the homepage in place of the `<!-- OSS_PRS -->`
marker, grouped by repository, newest first. Each title links straight to the PR on
GitHub, with its description underneath. Nothing is fetched during the build.
"""

from __future__ import annotations

import datetime as dt
import html
import logging
from pathlib import Path

import yaml

log = logging.getLogger("mkdocs.hooks.open_source")

PAGE = "index.md"
MARKER = "<!-- OSS_PRS -->"
STATUSES = ("merged", "open", "draft", "closed")


def _parse(url: str) -> tuple[str, str] | None:
    """https://github.com/owner/repo/pull/123 -> ("owner/repo", "123")"""
    parts = url.strip().rstrip("/").split("/")
    if len(parts) >= 7 and parts[-2] == "pull":
        return f"{parts[-4]}/{parts[-3]}", parts[-1]
    return None


def _load(config) -> list[dict]:
    path = Path(config.config_file_path).parent / "prs.yml"
    if not path.exists():
        return []
    entries = []
    for e in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
        url = e.get("url")
        if not isinstance(url, str) or not _parse(url):
            log.warning("prs.yml: skipping entry without a valid PR url: %r", e)
            continue
        status = str(e.get("status", "open")).lower()
        if status not in STATUSES:
            log.info("prs.yml: %s has unknown status %r, showing as open", url, status)
            status = "open"
        date = e.get("date")
        entries.append({
            "url": url, "status": status,
            "title": str(e.get("title") or url),
            "description": str(e.get("description") or "").strip(),
            "date": date if isinstance(date, (dt.date, dt.datetime)) else None,
        })
    entries.sort(key=lambda e: e["date"] or dt.date.min, reverse=True)
    return entries


def _render(entries: list[dict]) -> str:
    if not entries:
        return '<div class="oss-empty">No pull requests here yet. First contributions are in progress.</div>'

    counts: dict[str, int] = {}
    repos: dict[str, list[dict]] = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        repos.setdefault(_parse(e["url"])[0], []).append(e)

    stats = "".join(f'<span class="oss-stat"><b>{counts[s]}</b> {s}</span>' for s in STATUSES if s in counts)
    out = [f'<div class="oss-stats"><span class="oss-stat"><b>{len(entries)}</b> PRs</span>'
           f'<span class="oss-stat"><b>{len(repos)}</b> repos</span>{stats}</div>']

    for repo, items in repos.items():
        r = html.escape(repo)
        out.append(f'<section class="oss-repo"><h2 id="{r.replace("/", "-")}">'
                   f'<a href="https://github.com/{r}">{r}</a></h2><ul class="oss-list">')
        for e in items:
            num = _parse(e["url"])[1]
            date = e["date"].strftime("%b %Y") if e["date"] else ""
            desc = f'<p class="oss-desc">{html.escape(e["description"])}</p>' if e["description"] else ""
            out.append(
                f'<li><span class="oss-badge oss-badge--{e["status"]}">{e["status"]}</span>'
                f'<a class="oss-title" href="{html.escape(e["url"])}">{html.escape(e["title"])} ↗</a>'
                f'<span class="oss-num">#{num}</span>'
                f'<span class="oss-meta">{date}</span>{desc}</li>')
        out.append("</ul></section>")
    return "\n".join(out)


def on_page_markdown(markdown: str, page, config, files):
    if page.file.src_uri == PAGE:
        return markdown.replace(MARKER, _render(_load(config)))
    return markdown
