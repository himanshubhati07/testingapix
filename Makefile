.PHONY: install run test lint

install:
	python3 -m pip install -r requirements.txt

run:
	PORT=56961 bash ./start.sh

test:
	pytest tests/ -v --tb=short
