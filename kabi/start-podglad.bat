@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  Kabi-Chemie - lokalny podglad strony
echo  Uruchamiam serwer i otwieram http://localhost:8124/ w przegladarce...
echo  (To okno musi pozostac otwarte. Zamknij je, aby zatrzymac serwer.)
echo.
start "" /b node "%~dp0preview-server.mjs"
timeout /t 2 /nobreak >nul
start "" http://localhost:8124/
