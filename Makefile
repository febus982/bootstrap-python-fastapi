build:
	docker compose build

dev:
	docker compose up dev

test:
	docker compose run --rm dev pytest --cov

format:
	black app domains storage tests alembic