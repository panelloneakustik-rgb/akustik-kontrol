@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Akustik Kontrol — gelistirici

echo.
echo  ========================================================
echo   AKUSTIK KONTROL  —  yerel gelistirme
echo  ========================================================
echo   Bu dosyaya cift tikla. frontend icinde npm run dev YAZMA.
echo  ========================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  where py >nul 2>&1
  if errorlevel 1 (
    echo [HATA] Python yok.
    echo   https://www.python.org/downloads/
    echo   Kurarken "Add python.exe to PATH" isaretle.
    pause
    exit /b 1
  )
  set "PY=py -3"
) else (
  set "PY=python"
)

where node >nul 2>&1
if errorlevel 1 (
  echo [HATA] Node.js yok. https://nodejs.org/  — LTS kur.
  pause
  exit /b 1
)

if not exist "backend\.env" (
  copy /Y "backend\.env.example" "backend\.env" >nul
  echo [OK] backend\.env olusturuldu ^(sablon^).
)
if not exist "frontend\.env.local" (
  copy /Y "frontend\.env.local.example" "frontend\.env.local" >nul
  echo [OK] frontend\.env.local olusturuldu.
)

set "NEED_SETUP=0"
if not exist "backend\venv\Scripts\python.exe" set "NEED_SETUP=1"
if not exist "frontend\node_modules\" set "NEED_SETUP=1"

if "%NEED_SETUP%"=="1" (
  echo [1/4] Ilk kurulum — birkac dakika surebilir.
  if not exist "backend\venv\Scripts\python.exe" (
    %PY% -m venv backend\venv
    if errorlevel 1 (
      echo venv olusmadi.
      pause
      exit /b 1
    )
  )
  echo [2/4] Python paketleri...
  backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
  if errorlevel 1 (
    echo pip install basarisiz.
    pause
    exit /b 1
  )
  echo [3/4] npm install...
  pushd frontend
  call npm install
  if errorlevel 1 (
    popd
    echo npm install basarisiz.
    pause
    exit /b 1
  )
  popd
) else (
  echo [OK] Kurulum var — hizli acilis. Yeni paket eklediysen:
  echo      backend:  venv\Scripts\pip install -r backend\requirements.txt
  echo      frontend: cd frontend ^&^& npm install
  echo.
)

echo [migrate]
backend\venv\Scripts\python.exe backend\manage.py migrate
if errorlevel 1 (
  echo migrate basarisiz.
  pause
  exit /b 1
)

echo.
echo  --------------------------------------------------------
echo   Site:   http://localhost:3000
echo   API:    http://127.0.0.1:8000
echo   Admin:  http://127.0.0.1:8000/admin
echo.
echo   Canli:  git add / commit / push  origin main
echo           Frontend = Cloudflare Pages otomatik
echo           API     = VM'de git pull + systemctl restart akustik
echo   .env dosyalarini GitHub'a KOYMA.
echo  --------------------------------------------------------
echo.

start "Akustik API" cmd /k "cd /d "%~dp0backend" && venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000"
timeout /t 4 /nobreak >nul
start "Akustik Site" cmd /k "cd /d "%~dp0frontend" && call npm run dev"

echo Iki siyah pencere acik kalsin. Durdurmak icin o pencereleri kapat.
echo.
pause
