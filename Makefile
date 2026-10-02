.DEFAULT_GOAL := check

.PHONY: check validate test smoke

check: validate test smoke

validate:
	uv run --locked python scripts/validate_skills.py

test:
	uv run --locked python -m unittest discover -s tests -v

smoke:
	uv run --locked python scripts/smoke_install.py
