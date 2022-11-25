build:
	docker compose build

dev:
	docker compose up dev

test:
	docker compose run --rm dev poetry run pytest
