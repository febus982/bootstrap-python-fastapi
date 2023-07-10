FROM python:3.11-slim as base
ARG UID=2000
ARG GID=2000
RUN addgroup --gid $GID nonroot && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot
WORKDIR /app

# Creating a separate directory for venvs allows to easily
# copy them from the builder and to mount the application
# for local development
RUN mkdir /poetryvenvs && chown nonroot:nonroot /poetryvenvs

# Install necessary runtime libraries (e.g. libmysql)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Update pip and install poetry
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U poetry

FROM base as base_builder
# Install build system requirements (gcc, library headers, etc.)
# for compiled Python requirements like psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

# From here we shouldn't need anymore a root user
# Switch to nonroot and config poetry
USER nonroot
RUN poetry config virtualenvs.path /poetryvenvs

COPY --chown=nonroot:nonroot pyproject.toml .
COPY --chown=nonroot:nonroot poetry.lock .

# Test image, contains all files and dependencies
FROM base_builder as test
RUN poetry install --with http,grpc,dev
COPY --chown=nonroot:nonroot . .

# Installs requirements to run production http application
FROM base_builder as http_builder
RUN poetry install --no-root --with http

# Installs requirements to run production grpc application
FROM base_builder as grpc_builder
RUN poetry install --no-root --with grpc

# Copy the shared python packages
FROM base as base_app
USER nonroot
RUN poetry config virtualenvs.path /poetryvenvs
COPY --chown=nonroot:nonroot pyproject.toml .
COPY --chown=nonroot:nonroot poetry.lock .
COPY --chown=nonroot:nonroot alembic ./alembic
COPY --chown=nonroot:nonroot domains ./domains
COPY --chown=nonroot:nonroot storage ./storage
COPY --chown=nonroot:nonroot config.py .
COPY --chown=nonroot:nonroot di_container.py .
COPY --chown=nonroot:nonroot alembic.ini .
COPY --chown=nonroot:nonroot Makefile .
ENTRYPOINT ["poetry", "run"]

# Copy the http python package and requirements from relevant builder
FROM base_app as http_app
COPY --from=http_builder /poetryvenvs /poetryvenvs
COPY --chown=nonroot:nonroot http_app ./http_app
# opentelemetry-instrument will spawn a subprocess, therefore we use exec
# to make sure the app runs on PID 1 and receives correctly system signals
CMD opentelemetry-instrument uvicorn http_app:create_app --host 0.0.0.0 --port 8000 --factory

# Copy the grpc python package and requirements from relevant builder
FROM base_app as grpc_app
COPY --from=grpc_builder /poetryvenvs /poetryvenvs
COPY --chown=nonroot:nonroot grpc_app ./grpc_app
# opentelemetry-instrument will spawn a subprocess, therefore we use exec
# to make sure the app runs on PID 1 and receives correctly system signals
CMD exec opentelemetry-instrument python3 -m grpc_app
