SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

format:
	isort --recursive .
	black .

lint: isort-lint black-lint flake8-lint

isort-lint:
	isort --check-only --recursive .

black-lint:
	black --check .

flake8-lint:
	flake8 seki/

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-index --output-file requirements.txt setup.py

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-index --upgrade --output-file requirements.txt setup.py

.PHONY: install install-dev format lint isort-lint black-lint flake8-lint freeze freeze-upgrade