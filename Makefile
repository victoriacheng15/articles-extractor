.PHONY: init update format run up

init:
	pip install -r requirements.txt

update:
	pur -r requirements.txt

format:
	ruff format main.py utils

run:
	python3 main.py

up:
	docker compose up --build && docker logs extractor > logs.txt  && docker compose down
