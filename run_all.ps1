$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$server = (Get-ChildItem -LiteralPath $root -Recurse -Filter main.py | Select-Object -First 1).Directory.FullName
$serverCmd = "if (!(Test-Path '.venv\Scripts\python.exe')) { py -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements.txt }; .venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"
Start-Process powershell -WorkingDirectory $server -ArgumentList '-NoProfile','-NoExit','-ExecutionPolicy','Bypass','-Command',$serverCmd
Write-Host 'Institution server: http://127.0.0.1:8000/health'
Write-Host 'Reviewer web: http://127.0.0.1:8000/issue.html'
