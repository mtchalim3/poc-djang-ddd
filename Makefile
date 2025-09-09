
test:
	pytest

black:
	python -m black src/

lint:
	python -m flake8 --config=.flake8 src/ tests/