@echo off
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo Python yok. https://www.python.org/downloads/  -- kurarken Add Python to PATH isaretle.
  pause
  exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
  echo Node.js yok. https://nodejs.org/
  pause
  exit /b 1
)

if not exist "backend\.env" copy /Y "backend\.env.example" "backend\.env" >nul
if not exist "frontend\.env.local" copy /Y "frontend\.env.local.example" "frontend\.env.local" >nul

if not exist "backend\venv\Scripts\python.exe" (
  echo venv olusturuluyor...
  python -m venv backend\venv
)

echo Python paketleri...
backend\venv\Scripts\python.exe -m pip install -q -r backend\requirements.txt
backend\venv\Scripts\python.exe backend\manage.py migrate

echo npm install...
pushd frontend
call npm install
popd

echo.
echo Site: http://localhost:3000
echo API:  http://127.0.0.1:8000
echo Admin: http://127.0.0.1:8000/admin
echo.

start "Akustik API" cmd /k "cd /d "%~dp0backend" && venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000"
timeout /t 3 /nobreak >nul
start "Akustik Site" cmd /k "cd /d "%~dp0frontend" && npm run dev"
