flake8:
	flake8 seki/

install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

freeze:
	pip-compile --output-file requirements.txt setup.py
