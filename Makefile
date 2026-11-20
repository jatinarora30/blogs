.PHONY: setup serve serve-live build status new section

setup:    ## create venv and install deps
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

serve:    ## local preview with drafts: http://127.0.0.1:8000/blogs/
	.venv/bin/mkdocs serve

serve-live: ## preview exactly what will be published (drafts hidden)
	SHOW_DRAFTS=0 .venv/bin/mkdocs serve

build:    ## production build into site/ (drafts excluded)
	.venv/bin/mkdocs build --strict

status:   ## list every post and whether it is released
	@grep -H '^released:' docs/*/*.md | grep -v '/index.md' | sed -e 's/released: *//' -e 's/ *#.*//' | column -t -s:

new:      ## make new section=cpp slug=my-post title="My Post"
	@test -n "$(section)" -a -n "$(slug)" || (echo 'usage: make new section=cpp slug=my-post title="My Post"' && exit 1)
	@test -d docs/$(section) || (echo "no section docs/$(section) — create it with: make section name=$(section) title=..." && exit 1)
	@sed -e "s/{{TITLE}}/$(title)/g" -e "s/{{DATE}}/$$(date +%F)/" templates/post.md > docs/$(section)/$(slug).md
	@echo "created docs/$(section)/$(slug).md (draft)"

section:  ## make section name=systems title="Systems"
	@test -n "$(name)" -a -n "$(title)" || (echo 'usage: make section name=systems title="Systems"' && exit 1)
	@mkdir -p docs/$(name)
	@printf 'title: %s\n' "$(title)" > docs/$(name)/.pages
	@printf '# %s\n\nShort description of this section.\n\n<!-- posts -->\n' "$(title)" > docs/$(name)/index.md
	@echo "created section docs/$(name)/"
