# Loose Notes

My open-source work. Each pull request gets its own page in `docs/`, written by hand. The homepage lists them, grouped by repo with a status badge, built by `hooks/open_source.py` from each page's `pr:` and `status:` front matter. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages at **https://jatinarora30.github.io/blogs/**.

Profile: https://jatinarora30.github.io/jatin-arora.github.io/

## Layout

```
docs/
  index.md                 # homepage: intro + PR list (replaces <!-- OSS_PRS -->)
  my-pr.md                 # one page per PR
  assets/my-pr/            # images for that page
hooks/release.py           # release gate + sidebar ordering (newest first)
overrides/partials/        # profile card (left) and contributors box (right)
hooks/open_source.py       # homepage PR list from pages' `pr:` / `status:`
templates/post.md          # PR write-up template
```

## Adding a PR

```bash
make new slug=my-pr title="My PR"         # creates docs/my-pr.md and docs/assets/my-pr/
make serve                                # http://127.0.0.1:8000/blogs/ (drafts visible)
```

```yaml
---
title: "My PR"
date: 2026-11-20
released: false                 # true removes the Draft banner
pr: https://github.com/OWNER/REPO/pull/123   # the PR this page is about
status: merged                  # merged | open | draft | closed
tags: []
contributors: [jatinarora30]    # GitHub usernames, shown in the right sidebar
---
```

- **Drafts:** pages without `released: true` still go online, with a "Draft" banner at the top. Set `released: true` to remove the banner.
- **Images:** `![alt](assets/my-pr/diagram.png)`
- **Commands and output:** fenced blocks with titles, e.g. ```` ```bash title="Command" ````
- **Also supported:** math (`\( \)`, `\[ \]`), ` ```mermaid ` diagrams, and callouts (`!!! note`)

## Commands

```bash
make setup        # create .venv and install deps (once)
make serve        # preview with drafts
make serve-live   # preview only released pages
make status       # released / draft for each PR page
make build        # production build into site/
```

## Contributions

Each PR page's right sidebar lists its contributors and has a **Raise a request** button, which opens an issue using `.github/ISSUE_TEMPLATE/contribution.md`. It also links to editing the page on GitHub, which leads to a PR. When you accept a contribution, add the contributor's username to `contributors:`.

## Publishing

Write → `make serve` → set `released: true` → `git push`. The GitHub Actions workflow builds and deploys to Pages.

One-time setup:
1. Create a public repo `jatinarora30/blogs`. If you use a different name, update `site_url` and `repo_url` in `mkdocs.yml`.
2. `git remote add origin git@github.com:jatinarora30/blogs.git && git push -u origin main`
3. In the repo, go to **Settings → Pages → Source** and choose **GitHub Actions**.
