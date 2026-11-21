# Loose Notes

Long-form posts on whatever I'm building, breaking and learning. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages at **https://jatinarora30.github.io/blogs/**.

Profile: https://jatinarora30.github.io/jatin-arora.github.io/

## Layout

```
docs/
  index.md                 # homepage (one-line intro)
  my-post.md               # one file per post, all at this level (no sections)
  assets/my-post/          # images for that post
hooks/release.py           # release gate + sidebar ordering (newest first)
overrides/partials/        # profile card (left) and contributors box (right)
templates/post.md          # new-post template
```

## Writing a post

```bash
make new slug=my-post title="My Post"     # creates docs/my-post.md and docs/assets/my-post/
make serve                                # http://127.0.0.1:8000/blogs/ (drafts visible)
```

```yaml
---
title: "My Post"
date: 2026-11-20
released: false                 # true removes the Draft banner
tags: []
contributors: [jatinarora30]    # GitHub usernames, shown in the right sidebar
---
```

- **Drafts:** posts without `released: true` still go online, with a "Draft" banner at the top. Set `released: true` to remove the banner.
- **Images:** `![alt](assets/my-post/diagram.png)`
- **Commands and output:** fenced blocks with titles, e.g. ```` ```bash title="Command" ````
- **Also supported:** math (`\( \)`, `\[ \]`), ` ```mermaid ` diagrams, and callouts (`!!! note`)

## Commands

```bash
make setup        # create .venv and install deps (once)
make serve        # preview with drafts
make serve-live   # preview only released posts
make status       # released / draft for each post
make build        # production build into site/
```

## Contributions

Each post's right sidebar lists its contributors and has a **Raise a request** button, which opens an issue using `.github/ISSUE_TEMPLATE/contribution.md`. It also links to editing the page on GitHub, which leads to a PR. When you accept a contribution, add the contributor's username to `contributors:`.

## Publishing

Write → `make serve` → set `released: true` → `git push`. The GitHub Actions workflow builds and deploys to Pages.

One-time setup:
1. Create a public repo `jatinarora30/blogs`. If you use a different name, update `site_url` and `repo_url` in `mkdocs.yml`.
2. `git remote add origin git@github.com:jatinarora30/blogs.git && git push -u origin main`
3. In the repo, go to **Settings → Pages → Source** and choose **GitHub Actions**.
