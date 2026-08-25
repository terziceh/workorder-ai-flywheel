.PHONY: install generate-sample format lint test check

install:
	python -m pip install -e ".[dev]"

generate-sample:
	python scripts/generate_synthetic_data.py --rows 1000 --seed 42 --output sample_data/synthetic_workorders.csv

format:
	python -m ruff format .
	python -m ruff check . --fix

lint:
	python -m ruff format . --check
	python -m ruff check .

test:
	python -m unittest discover -s tests -p 'test_*.py' -v

check: lint test
