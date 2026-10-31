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

type:
    uv run ty check
    uv run pyrefly check
