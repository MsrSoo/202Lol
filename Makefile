.PHONY: install lint format test run security clean coverage bandit safety

PYTHON := python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install black mypy pytest pytest-mock pytest-cov requests stem whois halo rich tqdm bandit safety flake8 pylint
	$(PYTHON) -m pip install --upgrade pip

lint:
	mypy . --ignore-missing-imports
	black --check .
	flake8 .
	pylint *.py

format:
	black .

test:
	pytest ./test_main.py -vs

coverage:
	pytest --cov=. --cov-report=term-missing --cov-report=html -s ./test_main.py

security:
	bandit -r .
	safety check
	pip-audit

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf *.log

run:
	$(PYTHON) main.py

requirements:
	pip freeze > requirements.txt

precommit: lint security test coverage
	@echo "All checks passed!"
