ARG PYTHON_VERSION=3.13
FROM python:$PYTHON_VERSION-slim AS base
ARG UID=2000
ARG GID=2000
RUN addgroup --gid $GID nonroot && \
    adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot
WORKDIR /app
RUN chown nonroot:nonroot /app

# Creating a separate directory for venvs allows to easily
# copy them from the builder and to mount the application
# for local development
RUN mkdir /venv && chown nonroot:nonroot /venv
ENV PATH="/venv/bin:$PATH"

# Install necessary runtime libraries (e.g. libmysql)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

FROM base AS base_builder
ENV UV_PROJECT_ENVIRONMENT=/venv
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Install build system requirements (gcc, library headers, etc.)
# for compiled Python requirements like psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.5.15 /uv /uvx /bin/

# From here we shouldn't need anymore a root user
# Switch to nonroot and config uv
USER nonroot

COPY --chown=nonroot:nonroot pyproject.toml .
COPY --chown=nonroot:nonroot uv.lock .
COPY --chown=nonroot:nonroot Makefile .

# Dev image, contains all files and dependencies
FROM base_builder AS dev
COPY --chown=nonroot:nonroot . .
RUN --mount=type=cache,target=~/.cache/uv \
    make dev-dependencies

# Note that opentelemetry doesn't play well together with uvicorn reloader
# when signals are propagated, we disable it in dev image default CMD
CMD ["uvicorn", "http_app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory", "--reload"]

# Installs requirements to run production dramatiq application
FROM base_builder AS dramatiq_builder
RUN --mount=type=cache,target=~/.cache/uv \
    uv sync --no-dev --no-install-project --frozen --no-editable

# Installs requirements to run production http application
FROM base_builder AS http_builder
RUN --mount=type=cache,target=~/.cache/uv \
    uv sync --no-dev --group http --no-install-project --frozen --no-editable

# Create the base app with the common python packages
FROM base AS base_app
USER nonroot
COPY --chown=nonroot:nonroot src/alembic ./alembic
COPY --chown=nonroot:nonroot src/domains ./domains
COPY --chown=nonroot:nonroot src/gateways ./gateways
COPY --chown=nonroot:nonroot src/common ./common
COPY --chown=nonroot:nonroot src/alembic.ini .

# Copy the http python package and requirements from relevant builder
FROM base_app AS http_app
COPY --from=http_builder /venv /venv
COPY --chown=nonroot:nonroot src/http_app ./http_app
# Run CMD using array syntax, so it's uses `exec` and runs as PID1
CMD ["opentelemetry-instrument", "uvicorn", "http_app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]

# Copy the dramatiq python package and requirements from relevant builder
FROM base_app AS dramatiq_app
COPY --from=dramatiq_builder /venv /venv
COPY --chown=nonroot:nonroot src/dramatiq_worker ./dramatiq_worker
# Run CMD using array syntax, so it's uses `exec` and runs as PID1
# TODO: Review processes/threads
CMD ["opentelemetry-instrument", "dramatiq", "-p", "1", "-t", "1", "dramatiq_worker"]
