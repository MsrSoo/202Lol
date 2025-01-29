.PHONY: install lint format test run

install:
	pip install -r requirements.txt
	pip install black mypy

lint:
	mypy . --ignore-missing-imports
	black --check .

format:
	black .

test:
	pytest

run:
	python main.py
