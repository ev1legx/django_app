FROM python:3.11-slim

WORKDIR /app

# Установка netcat для проверки готовности базы в entrypoint.sh
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем pyproject.toml и poetry.lock в рабочую папку
COPY pyproject.toml poetry.lock* /app/

# Конфигурируем Poetry не создавать виртуальное окружение и устанавливаем зависимости (без установки текущего пакета)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь исходный код проекта
COPY . /app/

# Копируем и даем права на запуск entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
