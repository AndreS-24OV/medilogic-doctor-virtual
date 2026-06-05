@echo off
cd /d %~dp0\django_web
python manage.py migrate
python manage.py runserver 8000
pause
