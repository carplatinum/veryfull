# Базовый образ
FROM python:3.11-slim AS base

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV PATH=$POETRY_HOME/bin:$PATH
ENV PYTHONPATH=/app

# Установка зависимостей для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --only main

# Копируем весь проект
COPY . .

# Собираем статические файлы (можно отключить в продакшене)
RUN poetry run python manage.py collectstatic --noinput

# Финальный слой - минимальный образ для запуска
FROM python:3.11-slim

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV SECRET_KEY=your-secret-key-here # Замените на свой секретный ключ или передавайте через env

# Установка зависимостей для базы данных и runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение и код
COPY --from=base /app/.venv /app/.venv
COPY --from=base /app /app

# Добавляем виртуальное окружение в PATH
ENV PATH=/app/.venv/bin:$PATH

# Назначение рабочего каталога
WORKDIR /app

# Собираем статические файлы для продакшена (опционально)
RUN poetry run python manage.py collectstatic --noinput

# Команда запуска - запуск Gunicorn через Poetry
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
