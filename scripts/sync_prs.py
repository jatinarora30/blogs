#!/usr/bin/env python3
"""Sync prs.yml with GitHub.

Looks up every pull request USER has opened on repositories they don't own, then:
  * updates the `status:` line of each entry in prs.yml whose `url:` matches;
  * lists PRs that are not in prs.yml yet;
  * with --create, appends an entry for each of those (description left empty).

Your own writing is never touched; only `status:` is rewritten.
Set GITHUB_TOKEN to avoid the unauthenticated rate limit (60 requests/hour).

    python3 scripts/sync_prs.py            # update statuses, list missing
    python3 scripts/sync_prs.py --create   # also add missing PRs to prs.yml
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
from pathlib import Path

USER = "jatinarora30"
ROOT = Path(__file__).resolve().parent.parent
PRS = ROOT / "prs.yml"


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


ENTRY_RE = re.compile(r"^- url:\s*(\S+)\n((?:[ \t]+.*\n?|\n)*)", re.M)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--create", action="store_true", help="add PRs missing from prs.yml")
    args = ap.parse_args()

    try:
        prs = fetch_prs()
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"sync_prs: could not reach GitHub ({e}); nothing changed", file=sys.stderr)
        return 1

    by_url = {norm(p["url"]): p for p in prs}
    text = PRS.read_text(encoding="utf-8") if PRS.exists() else ""
    have: set[str] = set()

    def update(m: re.Match) -> str:
        url, body = m.group(1), m.group(2)
        have.add(norm(url))
        p = by_url.get(norm(url))
        if not p:
            return m.group(0)
        cur = re.search(r"^(\s+status:\s*)(\w+)", body, re.M)
        if cur and cur.group(2) == p["status"]:
            return m.group(0)
        if cur:
            body = body[:cur.start(2)] + p["status"] + body[cur.end(2):]
        else:
            body = f"  status: {p['status']}\n" + body
        print(f"updated  {url}: status -> {p['status']}")
        return f"- url: {url}\n{body}"

    text = ENTRY_RE.sub(update, text)

    missing = [p for p in prs if norm(p["url"]) not in have]
    print(f"{len(prs)} PRs on GitHub, {len(have & by_url.keys())} in prs.yml, {len(missing)} missing")
    for p in missing:
        print(f"  [{p['status']:6}] {p['url']}  {p['title']}")
    if missing and args.create:
        text = re.sub(r"^\[\]\s*$", "", text, flags=re.M).rstrip("\n") + "\n"
        for p in missing:
            title = p["title"].replace('"', "'")
            text += (f"\n- url: {p['url']}\n  title: \"{title}\"\n  status: {p['status']}\n"
                     f"  date: {p['date']}\n  description: \"\"\n")
        print(f"added {len(missing)} to prs.yml; fill in their descriptions")
    elif missing:
        print("run `make prs-new` to add these to prs.yml")

    if text != (PRS.read_text(encoding="utf-8") if PRS.exists() else ""):
        PRS.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
