@echo off
setlocal
pushd "%~dp0"
start cmd /k "call 기관서버\server\start_server.bat"
start cmd /k "call 심사자\web\start_web.bat"
echo Services started.
pause
endlocal
