#!/usr/bin/env bash
set -e

export DEBUG=${DEBUG:-False}
export API_URL=${API_URL:-http://127.0.0.1:8001/consulta}
export PORT=${PORT:-8000}

cd /app/django_web
python manage.py migrate --noinput
python manage.py collectstatic --noinput

cd /app/api_service
uvicorn main:app --host 127.0.0.1 --port 8001 &

cd /app/django_web
exec gunicorn doctor_web.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --timeout 120
