FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем pyproject.toml и poetry.lock для кеширования зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь код проекта
COPY . /app/

# Копируем entrypoint.sh и даем права на запуск
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Открываем порт 8000
EXPOSE 8000

# Используем entrypoint.sh как точку входа
ENTRYPOINT ["/app/entrypoint.sh"]

# Команда запуска gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
