FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем pyproject.toml и poetry.lock в рабочую папку
COPY pyproject.toml poetry.lock* /app/

# Конфигурируем Poetry не создавать виртуальное окружение и устанавливаем зависимости (без установки текущего пакета)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь исходный код проекта (предполагается, что проект в этой же папке)
COPY . /app/

EXPOSE 8000

# Запуск Gunicorn с указанием wsgi-модуля
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]
