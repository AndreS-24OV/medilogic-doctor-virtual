@echo off
cd /d %~dp0\api_service
uvicorn main:app --reload --port 8001
pause
