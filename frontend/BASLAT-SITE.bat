@echo off
cd /d "%~dp0"
echo Paketler kuruluyor (bir kez, 1-2 dk)...
call npm install
if errorlevel 1 (
  echo npm install basarisiz. Node.js kurulu mu?
  pause
  exit /b 1
)
echo Site aciliyor: http://localhost:3000
call npm run dev
