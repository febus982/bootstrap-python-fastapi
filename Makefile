build:
	docker compose build

dev:
	docker compose up dev

test:
	docker compose run --rm dev pytest --cov

migrate:
	docker compose run --rm alembic upgrade heads

format:
	black http_app domains storage tests alembic