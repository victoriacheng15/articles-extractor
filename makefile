.PHONY: init format run

init:
	@pip install -r requirements.txt

format:
	@ruff format main.py utils

run:
	@python3 main.py