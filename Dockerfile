# Используем multistage билд для минимизации размера финального образа
FROM python:3.11-slim as builder

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --upgrade pip setuptools wheel && \
    pip install poetry

WORKDIR /app

# Копируем зависимости файлы
COPY poetry.lock pyproject.toml ./
# Установка зависимостей в изолированный каталог
RUN poetry install --no-root --without dev

# Копируем весь проект
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Создаем финальный имедж на базе slim образа Python
FROM python:3.11-slim

# Указываем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости необходимых runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости из билд-образа
COPY --from=builder /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=builder /app /app

# Устанавливаем зависимости
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Настраиваем переменные
ENV PYTHONPATH=/app

# Собираем статику для production
RUN python manage.py collectstatic --noinput

# Запуск сервера Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
