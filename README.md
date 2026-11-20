# Blogs

A Markdown book of long-form posts on **C++ performance** and **robotics**, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages at **https://jatinarora30.github.io/blogs/**.

Profile: https://jatinarora30.github.io/jatin-arora.github.io/

## How it works

```
docs/
  index.md               # home page; table of contents is generated
  .pages                 # top-level nav (Home, sections…, Profile link)
  cpp/                   # a section = a folder
    .pages               #   title: C++
    index.md             #   section page; post list is generated
    caches-and-cpp.md    #   a post
  robotics/
    ...
hooks/release.py         # release gate + generated listings
templates/post.md        # new-post template
```

- **Sections:** every folder in `docs/` is a chapter. Drop a `.md` file into a folder and it appears in that section's sidebar, its section page and the home page.
- **Release gate:** a post is published only when its front matter has `released: true`. Drafts can be committed and pushed freely. The GitHub Actions build leaves them out, and a section with no released posts is hidden. Links from a published post to an unreleased one show as plain text until that post is released.

```yaml
---
title: "Error-State Kalman Filter from Scratch"
date: 2026-11-20
released: false   # set to true to publish
tags: [state-estimation]
---
```

## Commands

```bash
make setup                                        # create .venv, install deps (once)
make serve                                        # preview with drafts → http://127.0.0.1:8000/blogs/
make serve-live                                   # preview only what will be published
make status                                       # which posts are released
make new section=robotics slug=my-post title="My Post"
make section name=systems title="Systems"          # add a new chapter
make build                                        # production build into site/
```

## Writing

- Math: `\( inline \)` and `\[ display \]`
- Diagrams: ` ```mermaid ` code blocks
- Callouts: `!!! note`, `!!! warning`, `??? tip "Collapsible"`
- Images: store them next to the post or in `docs/assets/images/`, then use relative links

## Publishing

Workflow: write the post → `make serve` to check it → set `released: true` → `git push`.

On every push to `main`, `.github/workflows/deploy.yml` builds the site with `--strict` and deploys it to GitHub Pages.

### One-time setup

1. Create a GitHub repository named **`blogs`** under `jatinarora30`. The repository name becomes the URL path, so if you choose a different name, update `site_url` in `mkdocs.yml` to match.
2. `git remote add origin git@github.com:jatinarora30/blogs.git && git push -u origin main`
3. In the repository, go to **Settings → Pages → Source** and select **GitHub Actions**.
4. Add a link on your home site: `<a href="https://jatinarora30.github.io/blogs/">Blog</a>`
