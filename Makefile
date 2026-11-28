.PHONY: setup serve build prs prs-new

setup:      ## create venv and install deps
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

serve:      ## sync PR statuses, then local preview: http://127.0.0.1:8000/blogs/
	-python3 scripts/sync_prs.py
	.venv/bin/mkdocs serve

build:      ## production build into site/
	.venv/bin/mkdocs build --strict

prs:        ## update status: in prs.yml from GitHub and list PRs missing from it
	python3 scripts/sync_prs.py

prs-new:    ## same as prs, and add the missing PRs to prs.yml
	python3 scripts/sync_prs.py --create
