ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION-slim as base
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

# We run everything by poetry run from now on, so that PATH will be handled
# for binaries installed in virtual environments
ENTRYPOINT ["poetry", "run"]

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
FROM base_builder as dev
RUN poetry install --with http,grpc,dev,celery
COPY --chown=nonroot:nonroot . .
# Note that opentelemetry doesn't play well together with uvicorn reloader
# when signals are propagated, we disable it in dev image default CMD
CMD ["uvicorn", "http_app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory", "--reload"]

# Installs requirements to run production celery application
FROM base_builder as celery_builder
RUN poetry install --no-root --with celery

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
COPY --chown=nonroot:nonroot gateways ./gateways
COPY --chown=nonroot:nonroot config.py .
COPY --chown=nonroot:nonroot di_container.py .
COPY --chown=nonroot:nonroot alembic.ini .
COPY --chown=nonroot:nonroot Makefile .

# Copy the http python package and requirements from relevant builder
FROM base_app as http_app
COPY --from=http_builder /poetryvenvs /poetryvenvs
COPY --chown=nonroot:nonroot http_app ./http_app
# Run CMD using array syntax, so it's uses `exec` and runs as PID1
CMD ["opentelemetry-instrument", "uvicorn", "http_app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]

# Copy the grpc python package and requirements from relevant builder
FROM base_app as grpc_app
COPY --from=grpc_builder /poetryvenvs /poetryvenvs
COPY --chown=nonroot:nonroot grpc_app ./grpc_app
# Run CMD using array syntax, so it's uses `exec` and runs as PID1
CMD ["opentelemetry-instrument", "python3", "-m", "grpc_app"]

# Copy the grpc python package and requirements from relevant builder
FROM base_app as celery_app
COPY --from=celery_builder /poetryvenvs /poetryvenvs
COPY --chown=nonroot:nonroot celery_worker ./celery_worker
# Run CMD using array syntax, so it's uses `exec` and runs as PID1
CMD ["opentelemetry-instrument", "celery", "-A", "celery_worker:app", "worker", "--events"]
