.PHONY: install lint test security clean

PYTHON := python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install black mypy pytest pytest-mock pytest-cov requests stem whois halo rich tqdm bandit safety flake8 pylint
	mypy --install-types
	$(PYTHON) -m pip install --upgrade pip
	@echo "Installation "

lint:
	black .
	pylint *.py | tee >(sed '$d' > linting.log) | grep "rated"
	@echo "Linted all files."

security:
	safety scan # you need a safety account for this one, so go create one
	pip-audit
	@echo "Successfully scanned all files."

test:
	$(PYTHON) -m unittest tests/test_minor.py
	@sleep 4
	$(PYTHON) -m unittest tests/test_poke.py
	@sleep 4
	$(PYTHON) -m unittest tests/test_checker.py
	@sleep 3

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf *.log
	@echo "Deleted all cache."


precommit: lint security test clean
	@echo "All checks passed! You're ready to commit"
