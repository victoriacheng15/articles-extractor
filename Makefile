.PHONY: install update format run up logs down

install:
	python -m pip install -r requirements.txt

update:
	pur -r requirements.txt

format:
	ruff format main.py utils

run:
	python main.py 2>&1

up:
	docker compose up --build

logs:
	docker logs extractor > logs.txt

down:
	docker compose down
