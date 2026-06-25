@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  Kabi-Chemie — lokalny podglad strony
echo  Otwieram http://localhost:8124/ w przegladarce...
echo  (To okno musi pozostac otwarte. Zamknij je, aby zatrzymac serwer.)
echo.
start "" http://localhost:8124/
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0preview-server.ps1"
