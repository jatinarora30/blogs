"""Release gate + section indexes for the blog book.

Rules
-----
* Every folder under docs/ is a *section* (title comes from its `.pages` file).
* Every .md file inside a section (except index.md) is a *post*.
* A post is published only when its front matter says `released: true`.
  Anything else (missing, false) is a draft: it is dropped from `mkdocs build`
  (what GitHub Actions runs), so pushing a draft never puts it online.
* `mkdocs serve` (local preview) shows drafts with a banner so you can work on them.
  Set SHOW_DRAFTS=1 to include drafts in a build, or SHOW_DRAFTS=0 to hide them in serve.
* `<!-- posts -->` in a section's index.md is replaced by that section's post list.
* `<!-- sections -->` in docs/index.md is replaced by the table of contents.
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import posixpath
import re

import yaml
from mkdocs.structure.files import Files
from mkdocs.utils.meta import get_data

log = logging.getLogger("mkdocs.hooks.release")

SHOW_DRAFTS = False
SECTIONS: dict[str, dict] = {}   # section dir -> {"title": str, "posts": [post, ...]}
HIDDEN: set[str] = set()         # src_uri of drafts removed from the build
DRAFTS: set[str] = set()         # src_uri of drafts kept (preview mode)


def on_startup(command, dirty):
    global SHOW_DRAFTS
    env = os.environ.get("SHOW_DRAFTS")
    SHOW_DRAFTS = env == "1" if env is not None else command == "serve"


def _section_title(docs_dir: str, section: str) -> str:
    try:
        with open(os.path.join(docs_dir, section, ".pages"), encoding="utf-8") as fh:
            return (yaml.safe_load(fh) or {}).get("title") or section.title()
    except FileNotFoundError:
        return section.replace("-", " ").title()


def _post_title(meta: dict, body: str, fallback: str) -> str:
    if meta.get("title"):
        return str(meta["title"])
    m = re.search(r"^#\s+(.+)$", body, re.M)
    return m.group(1).strip() if m else fallback


def on_files(files: Files, config):
    SECTIONS.clear(); HIDDEN.clear(); DRAFTS.clear()
    docs_dir = config["docs_dir"]
    kept = []
    for f in files:
        parts = f.src_uri.split("/")
        is_post = f.src_uri.endswith(".md") and len(parts) == 2 and parts[1] != "index.md"
        if not is_post:
            kept.append(f)
            continue

        with open(f.abs_src_path, encoding="utf-8") as fh:
            body, meta = get_data(fh.read())
        released = meta.get("released") is True

        if not released and not SHOW_DRAFTS:
            HIDDEN.add(f.src_uri)
            log.info("draft (not published): %s", f.src_uri)
            continue
        if not released:
            DRAFTS.add(f.src_uri)

        kept.append(f)
        section = SECTIONS.setdefault(
            parts[0], {"title": _section_title(docs_dir, parts[0]), "posts": []}
        )
        date = meta.get("date")
        section["posts"].append({
            "file": parts[1],
            "title": _post_title(meta, body, parts[1][:-3]),
            "date": date if isinstance(date, (dt.date, dt.datetime)) else None,
            "draft": not released,
        })

    for s in SECTIONS.values():
        s["posts"].sort(key=lambda p: (p["date"] or dt.date.min), reverse=True)

    # A section with nothing published is hidden entirely (index + assets stay out of nav).
    kept = [f for f in kept
            if not (f.src_uri.endswith("/index.md") and f.src_uri.count("/") == 1
                    and f.src_uri.split("/")[0] not in SECTIONS)]

    log.info("published %d post(s), %d draft(s) %s",
             sum(not p["draft"] for s in SECTIONS.values() for p in s["posts"]),
             len(HIDDEN) + len(DRAFTS),
             "shown (preview)" if SHOW_DRAFTS else "hidden")
    return Files(kept)


def _post_line(p: dict, prefix: str = "") -> str:
    date = f" <small>· {p['date']:%d %b %Y}</small>" if p["date"] else ""
    draft = " <small>· **DRAFT**</small>" if p["draft"] else ""
    return f"- [{p['title']}]({prefix}{p['file']}){date}{draft}"


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s#]+\.md)(#[^)]*)?\)")


def on_page_markdown(markdown: str, page, config, files):
    src = page.file.src_uri
    here = posixpath.dirname(src)

    # Links to unpublished posts become plain text instead of dead links.
    def unlink(m):
        target = posixpath.normpath(posixpath.join(here, m.group(2)))
        return m.group(1) if target in HIDDEN else m.group(0)
    markdown = LINK_RE.sub(unlink, markdown)

    if src in DRAFTS:
        markdown = re.sub(
            r"^(---.*?---\s*)?",
            lambda m: (m.group(0) or "")
            + '!!! warning "Draft — not released"\n'
              "    Only visible in local preview. Set `released: true` to publish.\n\n",
            markdown, count=1, flags=re.S,
        )

    if src.endswith("/index.md") and "<!-- posts -->" in markdown:
        posts = SECTIONS.get(here, {}).get("posts", [])
        listing = "\n".join(_post_line(p) for p in posts) or "_Nothing published here yet._"
        markdown = markdown.replace("<!-- posts -->", listing)

    if src == "index.md" and "<!-- sections -->" in markdown:
        # Index appears only once something is released (or drafts are being previewed).
        out = []
        for key in sorted(SECTIONS, key=lambda k: SECTIONS[k]["title"].lower()):
            s = SECTIONS[key]
            if not s["posts"]:
                continue
            out.append(f"### [{s['title']}]({key}/index.md)\n")
            out += [_post_line(p, f"{key}/") for p in s["posts"]]
            out.append("")
        if out:
            out = ["---\n", "## Posts\n"] + out
        markdown = markdown.replace("<!-- sections -->", "\n".join(out))
    return markdown
