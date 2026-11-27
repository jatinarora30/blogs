"""Release gate + flat, date-ordered navigation.

Rules
-----
* Every .md file directly in docs/ (except index.md) is a post. No sections, no folders.
* A post is final when its front matter says `released: true`.
  Anything else (missing, false) is a draft: it is still published, but with a
  "Draft" banner at the top of the article.
* SHOW_DRAFTS=0 hides drafts entirely (in serve or build).
* Sidebar: Pull Requests (posts, newest first, if any), then the standalone PAGES, then the Profile link.
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import posixpath
import re

from mkdocs.structure.files import Files
from mkdocs.structure.nav import Link, Section
from mkdocs.structure.pages import Page
from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.release")

SHOW_DRAFTS = True
POSTS: dict[str, dict] = {}   # src_uri -> {"date": date|None, "draft": bool}
HIDDEN: set[str] = set()      # drafts removed from the build


def on_startup(command, dirty):
    global SHOW_DRAFTS
    env = os.environ.get("SHOW_DRAFTS")
    SHOW_DRAFTS = env != "0"


PAGES: list[str] = []   # standalone pages, listed after the posts


def _is_post(src_uri: str) -> bool:
    return (src_uri.endswith(".md") and "/" not in src_uri
            and src_uri != "index.md" and src_uri not in PAGES)


def on_files(files: Files, config):
    POSTS.clear(); HIDDEN.clear()
    kept = []
    for f in files:
        if not _is_post(f.src_uri) or not f.inclusion.is_included():
            kept.append(f)
            continue
        with open(f.abs_src_path, encoding="utf-8") as fh:
            _, meta = get_data(fh.read())
        released = meta.get("released") is True
        if not released and not SHOW_DRAFTS:
            HIDDEN.add(f.src_uri)
            log.info("draft (not published): %s", f.src_uri)
            continue
        date = meta.get("date")
        POSTS[f.src_uri] = {
            "date": date if isinstance(date, (dt.date, dt.datetime)) else None,
            "draft": not released,
        }
        kept.append(f)

    log.info("published %d post(s), %d draft(s) %s",
             sum(not p["draft"] for p in POSTS.values()),
             len(HIDDEN) + sum(p["draft"] for p in POSTS.values()),
             "shown with a Draft banner" if SHOW_DRAFTS else "hidden")
    return Files(kept)


def on_nav(nav, config, files):
    def sort_key(page):
        d = POSTS[page.file.src_uri]["date"]
        return (d or dt.date.min, page.file.src_uri)

    posts = sorted(
        (i for i in nav.items if isinstance(i, Page) and i.file.src_uri in POSTS),
        key=sort_key, reverse=True,
    )
    # Book-style previous / next between posts only.
    for i, page in enumerate(posts):
        page.previous_page = posts[i - 1] if i > 0 else None
        page.next_page = posts[i + 1] if i + 1 < len(posts) else None

    notes = Section("Pull Requests", list(posts))
    for page in posts:
        page.parent = notes
    items = [notes] if posts else []
    by_uri = {i.file.src_uri: i for i in nav.items if isinstance(i, Page)}
    items += [by_uri[u] for u in PAGES if u in by_uri]
    profile = (config.extra.get("profile") or {}).get("url")
    if profile:
        items.append(Link("Profile ↗", profile))
    nav.items = items
    return nav


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s#]+\.md)(#[^)]*)?\)")


def on_page_markdown(markdown: str, page, config, files):
    src = page.file.src_uri
    here = posixpath.dirname(src)

    # Links to unpublished posts become plain text instead of dead links.
    def unlink(m):
        target = posixpath.normpath(posixpath.join(here, m.group(2)))
        return m.group(1) if target in HIDDEN else m.group(0)
    markdown = LINK_RE.sub(unlink, markdown)

    if POSTS.get(src, {}).get("draft"):
        markdown = (
            '!!! warning "Draft"\n'
            "    This article is a work in progress and may change.\n\n"
            + markdown
        )
    return markdown
