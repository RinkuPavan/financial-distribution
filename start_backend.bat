@echo off
echo Starting Financial Distribution Backend...
cd /d "%~dp0"
start "" dist\run_server.exe
echo Backend running at http://localhost:8080
pause
