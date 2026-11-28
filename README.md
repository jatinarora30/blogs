# Upstreamed

My open-source work: every pull request I've opened on other people's projects. The homepage lists them, grouped by repo, each with a status badge and a short description. The title links straight to the PR on GitHub. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages at **https://jatinarora30.github.io/blogs/**.

Profile: https://jatinarora30.github.io/jatin-arora.github.io/

## Layout

```
prs.yml                    # the PR list: one entry per PR
docs/index.md              # homepage: intro + PR list (replaces <!-- OSS_PRS -->)
hooks/open_source.py       # renders prs.yml onto the homepage
scripts/sync_prs.py        # updates status: in prs.yml from GitHub
overrides/partials/nav.html  # profile card in the left sidebar
```

## Adding a PR

Add an entry to `prs.yml`. The file starts with a template entry (`OWNER/REPO#123`) that shows on the site as an example. Copy it for each real PR:

```yaml
- url: https://github.com/OWNER/REPO/pull/123
  title: Short title of what the PR does
  status: open        # merged | open | draft | closed
  date: 2026-11-20
  description: One or two sentences on what was wrong and what the PR changed.
```

Or run `make prs-new` to add every PR missing from the file, then fill in the descriptions.

## Commands

```bash
make setup        # create .venv and install deps (once)
make serve        # sync statuses, then preview at http://127.0.0.1:8000/blogs/
make prs          # update status: in prs.yml from GitHub, list PRs missing from it
make prs-new      # same, and add the missing PRs to prs.yml
make build        # production build into site/
```

A GitHub Action (`.github/workflows/sync-prs.yml`) also updates statuses every Monday and redeploys.

## Publishing

Edit `prs.yml` → `make serve` → `git push`. The GitHub Actions workflow builds and deploys to Pages.
