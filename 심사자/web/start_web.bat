@echo off
cd /d %~sdp0
py -m http.server 5500
pause
