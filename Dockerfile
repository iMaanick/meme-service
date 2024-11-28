FROM python:3.10-slim

WORKDIR /app

# Устанавливаем Poetry и зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

# Копируем оставшиеся файлы проекта
COPY . .

CMD ["poetry", "run", "uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
