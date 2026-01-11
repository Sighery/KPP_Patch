.PHONY: sync_readme
sync_readme:
	@PYTHONPATH=. ./scripts/update_readme.py
