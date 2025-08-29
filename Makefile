
test:
	pytest

black:
	python -m black src/ tests/

lint:
	python -m flake8 --config=.flake8 src/ tests/