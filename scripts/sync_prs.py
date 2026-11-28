#!/usr/bin/env python3
"""Sync PR pages with GitHub.

Looks up every pull request USER has opened on repositories they don't own, then:
  * updates the `status:` line of each page in docs/ whose `pr:` matches;
  * lists PRs that have no page yet;
  * with --create, adds a draft page (released: false) for each of those.

Your own writing is never touched; only `status:` is rewritten.
Set GITHUB_TOKEN to avoid the unauthenticated rate limit (60 requests/hour).

    python3 scripts/sync_prs.py            # update statuses, list missing
    python3 scripts/sync_prs.py --create   # also create draft pages
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

USER = "jatinarora30"
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "templates" / "post.md"


def fetch_prs() -> list[dict]:
    q = f"type:pr author:{USER} -user:{USER}"
    prs, page = [], 1
    while True:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if tok := os.environ.get("GITHUB_TOKEN"):
            req.add_header("Authorization", f"Bearer {tok}")
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.load(r)
        for i in data["items"]:
            if i["pull_request"].get("merged_at"):
                status = "merged"
            elif i["state"] == "closed":
                status = "closed"
            elif i.get("draft"):
                status = "draft"
            else:
                status = "open"
            prs.append({"url": i["html_url"], "title": i["title"], "status": status,
                        "date": i["created_at"][:10]})
        if len(data["items"]) < 100 or page * 100 >= data["total_count"]:
            return prs
        page += 1


def norm(url: str) -> str:
    return url.strip().rstrip("/").lower()


def front_matter(text: str) -> str:
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def slugify(pr: dict) -> str:
    owner_repo, num = pr["url"].split("github.com/")[1].split("/pull/")
    return re.sub(r"[^a-z0-9]+", "-", f"{owner_repo.split('/')[1]}-{num}".lower()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--create", action="store_true", help="create draft pages for PRs without one")
    args = ap.parse_args()

    try:
        prs = fetch_prs()
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"sync_prs: could not reach GitHub ({e}); nothing changed", file=sys.stderr)
        return 1

    by_url = {norm(p["url"]): p for p in prs}
    have: set[str] = set()

    for f in sorted(DOCS.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = front_matter(text)
        m = re.search(r"^pr:\s*(\S+)", fm, re.M)
        if not m or norm(m.group(1)) not in by_url:
            continue
        have.add(norm(m.group(1)))
        new = by_url[norm(m.group(1))]["status"]
        cur = re.search(r"^status:\s*(\w+)", fm, re.M)
        if cur and cur.group(1) == new:
            continue
        if cur:
            fm2 = fm[:cur.start(1)] + new + fm[cur.end(1):]
        else:
            fm2 = fm + f"\nstatus: {new}"
        f.write_text(text.replace(fm, fm2, 1), encoding="utf-8")
        print(f"updated  {f.relative_to(ROOT)}: status -> {new}")

    missing = [p for p in prs if norm(p["url"]) not in have]
    print(f"{len(prs)} PRs on GitHub, {len(have)} with a page, {len(missing)} without")
    for p in missing:
        line = f"  [{p['status']:6}] {p['url']}  {p['title']}"
        if args.create:
            dest = DOCS / f"{slugify(p)}.md"
            if dest.exists():
                line += f"  ({dest.name} exists but has a different pr:, skipped)"
            else:
                title = p["title"].replace('"', "'")
                body = TEMPLATE.read_text(encoding="utf-8").replace("{{TITLE}}", title)
                body = body.replace("{{DATE}}", p["date"])
                body = re.sub(r"^pr:.*$", f"pr: {p['url']}", body, count=1, flags=re.M)
                body = re.sub(r"^status:\s*\w+", f"status: {p['status']}", body, count=1, flags=re.M)
                dest.write_text(body, encoding="utf-8")
                (DOCS / "assets" / dest.stem).mkdir(parents=True, exist_ok=True)
                line += f"  -> created {dest.relative_to(ROOT)} (draft)"
        print(line)
    if missing and not args.create:
        print("run `make prs-new` to create draft pages for these")
    return 0


if __name__ == "__main__":
    sys.exit(main())
