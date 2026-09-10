@echo off
pushd "%~dp0"
py -m http.server 5500
pause
