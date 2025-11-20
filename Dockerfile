# Используем multistage билд для минимизации размера финального образа
FROM python:3.11-slim as builder

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="/app/.venv/bin:$PATH"

# Установить необходимое для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установить Poetry
RUN pip install --upgrade pip setuptools wheel
RUN pip install poetry

WORKDIR /app

# Копируем зависимости
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости
RUN poetry install --no-root --without dev

# Копируем весь проект
COPY . .

# Добавляем переменную для SECRET_KEY (замените на свой реальный ключ или секрет CI)
ENV SECRET_KEY="change_this_to_your_secret_key"

# Собираем статику внутри poetry run
RUN poetry run python manage.py collectstatic --noinput


# Минималистичный продакшн-образ
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# Устанавливаем runtime зависимости
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем виртуальное окружение и код из builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

# Перед запуском Gunicorn также задайте SECRET_KEY
ENV SECRET_KEY="change_this_to_your_secret_key"

# Собираем статику (если нужно)
RUN poetry run python manage.py collectstatic --noinput

# Запуск Gunicorn через poetry run, чтобы использовать виртуальное окружение
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
