.PHONY: update_requirements
update_requirements:
	rm -f requirements.txt requirements-dev.txt
	pip-compile --generate-hashes --resolver=backtracking --strip-extras --no-header -o requirements.txt pyproject.toml
	pip-compile --generate-hashes --resolver=backtracking --strip-extras --no-header --extra dev -o requirements-dev.txt pyproject.toml
.PHONY: format
format:
	ruff check app/ core/ tests/
	ruff format app/ core/ tests/
	mypy app/ core/ tests/
cov:
	coverage run -m pytest
	coverage html

test:
	ENV=test pytest tests -s
