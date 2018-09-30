help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help"
	@echo "    to show this message"
	@echo "  all"
	@echo "    to run the following targets"
	@echo "  docs-clean"
	@echo "    to remove HTML documentation"
	@echo "  docs-html"
	@echo "    to generate HTML documentation"
	@echo "  lint"
	@echo "    to run all linters"
	@echo "  lint-flake8"
	@echo "    to run the flake8 linter"
	@echo "  lint-pylint"
	@echo "    to run the pylint linter"
	@echo "  test"
	@echo "    to run unit tests"

all: test lint docs-clean docs-html

docs-clean:
	@cd docs; $(MAKE) clean

docs-html:
	rm -rf docs/api/*
	scripts/gen-api-docs.sh
	@cd docs; $(MAKE) html

lint: lint-flake8 lint-pylint

# E501 and F401 are ignored because Pylint performs similar checks.
lint-flake8:
	flake8 . --ignore E501,F401 --exclude docs/_build

lint-pylint:
	pylint docs/conf.py movie_recommender setup.py tests

test:
	python3 -m unittest discover --start-directory tests --top-level-directory .

.PHONY: help \
	all \
	docs-clean \
	docs-html \
	lint \
	lint-flake8 \
	lint-pylint \
	test \
