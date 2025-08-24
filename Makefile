.PHONY: all

readme:
	quarto render docs/README.qmd --output-dir ..

coverage:
	uv run coverage run --source=bumplot -m pytest
	uv run coverage report -m
	uv run coverage xml
	uv run genbadge coverage -i coverage.xml
	rm coverage.xml

preview:
	uv run mkdocs serve

test:
	uv run pytest
