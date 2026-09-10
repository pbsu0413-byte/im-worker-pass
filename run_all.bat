@echo off
setlocal
cd /d "%~dp0"
start "iM Institution Server" cmd /k call 기관서버\server\start_server.bat
start "iM Reviewer Web" cmd /k call 심사자\web\start_web.bat
echo Services started.
pause
endlocal
