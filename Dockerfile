# Используем multistage билд для минимизации размера финального образа
FROM python:3.11-slim as builder

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="/app/.venv/bin:$PATH"

# Установка системных библиотек для сборки зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --upgrade pip setuptools wheel
RUN pip install poetry

WORKDIR /app

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости в локальное виртуальное окружение в /app/.venv
RUN poetry install --no-root --without dev

# Копируем весь проект
COPY . .

# Собираем статические файлы через Poetry (в виртуальном окружении)
RUN poetry run python manage.py collectstatic --noinput

# Финальный минимальный образ
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

WORKDIR /app

# Устанавливаем runtime зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из слоя builder
COPY --from=builder /app/.venv /app/.venv

# Копируем код проекта
COPY --from=builder /app /app

# Через Poetry запускаем сборку статических файлов для production (если нужно)
RUN poetry run python manage.py collectstatic --noinput

# Команда запуска Gunicorn через Poetry, чтобы использовать виртуальное окружение
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
