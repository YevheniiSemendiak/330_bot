.PHONY: setup init
setup init:
	pip install -r requirements/dev.txt
	pre-commit install

.PHONY: lint
lint:
ifdef CI_LINT_RUN
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif
