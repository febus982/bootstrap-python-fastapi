FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

COPY . .

CMD ["make", "run"]
