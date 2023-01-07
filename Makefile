build:
	docker compose build

dev:
	docker compose up dev

test:
	docker compose run --rm dev pytest --cov

migrate:
	docker compose run --rm dev alembic upgrade heads

format:
	black http_app domains storage tests alembic

# There are issues on how python imports are generated when using nested
# packages. The following setup appears to work, however it might need
# to be reviewed. https://github.com/protocolbuffers/protobuf/issues/1491
generate-proto:
	rm -rf ./grpc_app/generated/*
	touch ./grpc_app/generated/__init__.py
	python -m grpc_tools.protoc \
	-I grpc_app.generated=./grpc_app/proto/ \
	--python_out=. \
	--mypy_out=. \
	grpc_app/proto/*.proto
	python -m grpc_tools.protoc \
	-I grpc_app/generated=./grpc_app/proto/ \
	--grpc_python_out=. \
	grpc_app/proto/*.proto
	git add ./grpc_app/generated

# Setup to be used with grpclib and betterproto libraries
generate-betterproto:
	rm -rf ./grpc_app/generated/*
	touch ./grpc_app/generated/__init__.py
	python -m grpc_tools.protoc \
	-I grpc_app.generated=./grpc_app/proto/ \
	--python_betterproto_out=./grpc_app/generated \
	--python_out=. \
	--grpclib_python_out=. \
	grpc_app/proto/*.proto
	git add ./grpc_app/generated
