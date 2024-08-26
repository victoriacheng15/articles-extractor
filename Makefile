.PHONY: init format run start

init:
	@pip install -r requirements.txt

format:
	@ruff format main.py utils

run:
	@python3 main.py

start:
	@docker compose up --force-recreate && docker compose down