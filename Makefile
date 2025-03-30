.PHONY: install lint format test run security clean coverage bandit safety

PYTHON := python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install black mypy pytest pytest-mock pytest-cov requests stem whois halo rich tqdm bandit safety flake8 pylint
	mypy --install-types
	$(PYTHON) -m pip install --upgrade pip

lint:
	mypy . --ignore-missing-imports
	black .
	pylint *.py | tee >(sed '$d' > linting.log) | grep "rated"

security:
	bandit -r .
	safety scan # you need a safety account for this one, so go create one
	pip-audit

test:
	$(PYTHON) -m unittest tests/test_poke.py

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf *.log


precommit: lint security test
	@echo "All checks passed!"
