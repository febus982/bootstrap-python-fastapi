# Install shared system requirements (e.g. libmysql)
FROM python:3.11-slim as base
# Creating a separate directory for venvs allows to easily
# copy them from the builder and to mount the application
# for local development
RUN mkdir /poetryvenvs
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip
RUN pip install poetry
RUN poetry config virtualenvs.path /poetryvenvs

# Install shared build system requirements (gcc, library headers, etc.)
FROM base as base_builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY poetry.lock .

# Test image, contains all files and dependencies
FROM base_builder as test
RUN poetry install --no-root --with http,grpc,dev
COPY . .

# Installs requirements to run production http application
FROM base_builder as http_builder
RUN poetry install --no-root --with http

# Installs requirements to run production grpc application
FROM base_builder as grpc_builder
RUN poetry install --no-root --with grpc

# Copy the shared python packages
FROM base as base_app
COPY pyproject.toml .
COPY poetry.lock .
COPY alembic .
COPY domains .
COPY storage .
COPY config.py .
COPY di_container.py .
COPY alembic.ini .
COPY Makefile .

# Copy the http python package and requirements from relevant builder
FROM base_app as http_app
COPY --from=http_builder /poetryvenvs /poetryvenvs
COPY http_app .
CMD ["make", "run"]

# Copy the grpc python package and requirements from relevant builder
FROM base_app as grpc_app
COPY --from=grpc_builder /poetryvenvs /poetryvenvs
COPY grpc_app .
CMD ["make", "grpc"]
