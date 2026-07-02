@echo off
setlocal
title PrintLab Launcher
cd /d "%~dp0"

echo Starting Docker Desktop...
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
  start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
)

echo Waiting for Docker to become ready...
:wait_docker
docker info >nul 2>&1
if errorlevel 1 (
  timeout /t 3 /nobreak >nul
  goto wait_docker
)

echo Starting PostgreSQL and Redis...
docker compose up -d postgres redis
if errorlevel 1 goto failed

echo Waiting for PostgreSQL...
:wait_postgres
docker exec altprint_postgres pg_isready -U altprint -d altprint_db >nul 2>&1
if errorlevel 1 (
  timeout /t 2 /nobreak >nul
  goto wait_postgres
)

echo Enabling local access...
docker exec altprint_postgres psql -U altprint -d altprint_db -c "UPDATE feature_flags SET enabled = true WHERE feature_name = 'login_register'; UPDATE system_config SET login_enabled = true, app_enabled = true, maintenance_mode = false, emergency_lock = false WHERE id = 1;" >nul

echo Starting PrintLab on port 8001...
start "PrintLab Backend" cmd /k "cd /d ""%~dp0"" && set ""PYTHONPATH=."" && set ""DATABASE_URL=postgresql+asyncpg://altprint:altprint_secure_password@localhost:5433/altprint_db"" && set ""REDIS_URL=redis://localhost:6379/0"" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"

echo Waiting for the backend...
:wait_backend
powershell -NoProfile -Command "try { if ((Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://127.0.0.1:8001/health).StatusCode -eq 200) { exit 0 } } catch {}; exit 1" >nul 2>&1
if errorlevel 1 (
  timeout /t 2 /nobreak >nul
  goto wait_backend
)

start "" "http://127.0.0.1:8001/full"
start "" "http://127.0.0.1:8001/shop"

echo.
echo PrintLab is ready.
echo Admin panel : http://127.0.0.1:8001/full
echo Outlet panel: http://127.0.0.1:8001/shop
echo Login       : admin@altprint.in / AltPrint2024!
echo.
pause
exit /b 0

:failed
echo.
echo PrintLab could not start. Check Docker Desktop and try again.
pause
exit /b 1