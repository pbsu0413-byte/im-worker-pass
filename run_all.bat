@echo off
setlocal
set "ROOT=%~sdp0"
start cmd /k "cd /d %ROOT%기관서버\server && call start_server.bat"
start cmd /k "cd /d %ROOT%심사자\web && call start_web.bat"
echo Services started.
pause
endlocal
