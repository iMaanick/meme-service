FROM python:3.10-slim

WORKDIR /app

# Устанавливаем Poetry и зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

COPY . .

RUN rm -f .env test.db

ENV DATABASE_URI=sqlite+aiosqlite:///./test.db

RUN poetry run alembic upgrade head

CMD ["poetry", "run", "uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
