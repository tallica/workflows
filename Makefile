.PHONY: check lint test fmt fmt-check

PRETTIER := npx --yes prettier@3.9.10

# The gate before every commit; CI runs it as is.
check: lint test

# Prettier: Markdown, YAML, JSON and JS; CI runs fmt-check.
fmt:
	$(PRETTIER) --write --log-level warn .

fmt-check:
	$(PRETTIER) --check --log-level warn .

# actionlint checks workflow syntax, expressions and (with shellcheck
# installed) the run: scripts; CI has no actionlint, so it is built there.
ACTIONLINT := $(shell command -v actionlint 2>/dev/null || echo go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12)

lint:
	$(ACTIONLINT)

test:
	python3 tests/workflows.py
	python3 -m unittest discover -s tests
