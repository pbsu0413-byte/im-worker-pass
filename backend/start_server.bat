@echo off
cd /d %~sdp0
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)
.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
pause
