FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

CMD ["uvicorn", "app:create_app", "--factory","--host", "0.0.0.0", "--port", "8000"]
