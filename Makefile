install:
	pip install -r requirements.txt
	pip install -e .

run:
	lambda-explorer

run-cli:
	lambda-explorer-cli

format:
	black lambda_explorer

lint:
	pre-commit run --files $(shell git ls-files "*.py")
