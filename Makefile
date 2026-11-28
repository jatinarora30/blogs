.PHONY: setup serve serve-live build status new prs prs-new

setup:      ## create venv and install deps
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

serve:      ## sync PR statuses, then local preview with drafts: http://127.0.0.1:8000/blogs/
	-python3 scripts/sync_prs.py
	.venv/bin/mkdocs serve

serve-live: ## preview with drafts hidden
	SHOW_DRAFTS=0 .venv/bin/mkdocs serve

build:      ## production build into site/ (drafts shown with a Draft banner)
	.venv/bin/mkdocs build --strict

status:     ## list every post and whether it is released
	@grep -H '^released:' docs/*.md | sed -e 's/released: *//' -e 's/ *#.*//' | column -t -s:

new:        ## make new slug=my-post title="My Post"
	@test -n "$(slug)" || (echo 'usage: make new slug=my-post title="My Post"' && exit 1)
	@test ! -e docs/$(slug).md || (echo "docs/$(slug).md already exists" && exit 1)
	@sed -e "s/{{TITLE}}/$(title)/g" -e "s/{{DATE}}/$$(date +%F)/" templates/post.md > docs/$(slug).md
	@mkdir -p docs/assets/$(slug)
	@echo "created docs/$(slug).md (draft) — images go in docs/assets/$(slug)/"

prs:        ## update status: of PR pages from GitHub and list PRs with no page yet
	python3 scripts/sync_prs.py

prs-new:    ## same as prs, and create a draft page for each PR with no page
	python3 scripts/sync_prs.py --create
