dev:
	poetry run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory --reload

run:
	poetry run uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

grpc:
	poetry run python3 -m grpc_app

test:
	poetry run pytest --cov

migrate:
	poetry run alembic upgrade heads

format:
	poetry run black http_app domains storage tests alembic

# There are issues on how python imports are generated when using nested
# packages. The following setup appears to work, however it might need
# to be reviewed. https://github.com/protocolbuffers/protobuf/issues/1491
generate-proto:
	rm -rf ./grpc_app/generated/*.p*
	touch ./grpc_app/generated/__init__.py
	poetry run python -m grpc_tools.protoc \
	-I grpc_app.generated=./grpc_app/proto/ \
	--python_out=. \
	--mypy_out=. \
	grpc_app/proto/*.proto
	poetry run python -m grpc_tools.protoc \
	-I grpc_app/generated=./grpc_app/proto/ \
	--grpc_python_out=. \
	grpc_app/proto/*.proto
	git add ./grpc_app/generated
