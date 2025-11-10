#!/bin/sh

echo "Ожидание готовности базы данных..."

while ! nc -z ${DB_HOST:-localhost} ${DB_PORT:-5432}; do
  echo "База данных недоступна, ждем 1 секунду..."
  sleep 1
done

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Сборка статики..."
python manage.py collectstatic --noinput

echo "Запуск Gunicorn..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
