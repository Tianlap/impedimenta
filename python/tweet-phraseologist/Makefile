.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help"
	@echo "    to show this message"
	@echo "  all"
	@echo "    to do all of the following"
	@echo "  lint"
	@echo "    to run all linters"
	@echo "  lint-flake8"
	@echo "    to run the flake8 linter"
	@echo "  lint-mypy"
	@echo "    to run the mypy linter"
	@echo "  lint-pylint"
	@echo "    to run the pylint linter"
	@echo "  test"
	@echo "    to run all tests"
	@echo "  test-functional"
	@echo "    to run functional tests"
	@echo "  test-unit"
	@echo "    to run unit tests"

.PHONY: all
all: lint test

.PHONY: lint
lint: lint-flake8 lint-mypy lint-pylint

.PHONY: test
test: test-unit test-functional

# E501,E722,F401 ignored because Pylint performs similar checks.
.PHONY: lint-flake8
lint-flake8:
	flake8 . --ignore E501,E722,F401

.PHONY: lint-mypy
lint-mypy:
	mypy --package tp --module setup
	mypy tests

.PHONY: lint-pylint
lint-pylint:
	pylint -j 0 tests tp setup.py

.PHONY: test-unit
test-unit:
	python3 -m unittest discover --start-directory tests/unit --top-level-directory .

.PHONY: test-functional
test-functional:
	python3 -m unittest discover --start-directory tests/functional --top-level-directory .
