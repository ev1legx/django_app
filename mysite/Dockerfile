FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы poetry
COPY pyproject.toml poetry.lock* /app/

# Конфигурируем Poetry не создавать виртуальное окружение и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем все остальное
COPY . /app/

EXPOSE 8000

# Запуск Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
