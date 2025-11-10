FROM python:3.11-slim

WORKDIR /app

# Установка netcat для проверки доступности базы в entrypoint.sh
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем pyproject.toml и poetry.lock для кеширования зависимостей
COPY pyproject.toml poetry.lock* /app/

# Конфигурируем Poetry не создавать виртуальное окружение и устанавливаем зависимости (без установки текущего пакета)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь исходный код проекта
COPY . /app/

# Копируем и даем права на запуск entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# expose порт 8000
EXPOSE 8000

# Используем entrypoint.sh как точку входа
ENTRYPOINT ["/app/entrypoint.sh"]

# Команда запуска gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
