#!/bin/sh
echo "Применение миграций..."
python manage.py migrate --noinput
echo "Запуск Gunicorn..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
