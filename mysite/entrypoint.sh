#!/bin/sh

# Простая пауза для ожидания базы (если netcat не установлен)
echo "Подождем 10 секунд, чтобы база успела подняться..."
sleep 10

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Сборка статики..."
python manage.py collectstatic --noinput

echo "Запуск Gunicorn..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
