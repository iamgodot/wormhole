.PHONY: help venv lint test clean

help:
	@echo "Use 'make target' of which target is from the following:"
	@echo "  install	to install via requirements.txt"
	@echo "  test 		to test through all test cases"

install:
	pip install -r requirements.txt

clean:
	find . -iname "*__pycache__" | xargs rm -rf
	find . -iname "*.pyc" | xargs rm -rf
	rm -rf .pytest_cache

format:
	black .

lint:
	flake8 --format=pylint --count

test: clean lint
	pytest -v --cov=src/py_tldr tests
