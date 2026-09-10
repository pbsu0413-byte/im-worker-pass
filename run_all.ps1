# iM Worker Pass - 로컬 실행 스크립트
$ErrorActionPreference = 'Stop'

$root    = Split-Path -Parent $MyInvocation.MyCommand.Path
$server  = Join-Path $root 'backend'
$py      = Join-Path $server '.venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $server)) {
    Write-Host "[오류] backend 폴더를 찾을 수 없습니다: $server" -ForegroundColor Red
    Read-Host '엔터를 누르면 종료합니다'
    exit 1
}

Set-Location -LiteralPath $server

if (-not (Test-Path -LiteralPath $py)) {
    Write-Host '[1/3] 가상환경(.venv)을 만드는 중...' -ForegroundColor Cyan
    py -m venv .venv
    if (-not (Test-Path -LiteralPath $py)) {
        Write-Host '[오류] 가상환경 생성 실패. Python이 설치되어 있는지 확인하세요 (py --version).' -ForegroundColor Red
        Read-Host '엔터를 누르면 종료합니다'
        exit 1
    }
}

Write-Host '[2/3] 의존성 확인/설치 중...' -ForegroundColor Cyan
& $py -m pip install --disable-pip-version-check -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host '[오류] pip 설치 실패. 위 메시지를 확인하세요.' -ForegroundColor Red
    Read-Host '엔터를 누르면 종료합니다'
    exit 1
}

Write-Host ''
Write-Host '[3/3] 서버 시작' -ForegroundColor Cyan
Write-Host '  헬스체크 : http://127.0.0.1:8000/health'
Write-Host '  발급 화면 : http://127.0.0.1:8000/issue.html'
Write-Host '  검증 화면 : http://127.0.0.1:8000/scan.html'
Write-Host '  (이 창을 닫으면 서버도 종료됩니다. 중지: Ctrl+C)'
Write-Host ''

& $py -m uvicorn main:app --reload --port 8000

Write-Host ''
Write-Host '서버가 종료되었습니다. 위에 빨간 오류 메시지가 있으면 그대로 복사해 주세요.' -ForegroundColor Yellow
Read-Host '엔터를 누르면 창을 닫습니다'
