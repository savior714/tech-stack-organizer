<#
.SYNOPSIS
    공통 Nuitka 단일 빌드 스크립트
.DESCRIPTION
    sources.json에서 Python 버전을 읽어 검증하고, UAC 관리자 권한 옵션을 추가하여 Windows 11 최적화된 방법으로 Nuitka 빌드를 수행합니다.
#>

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# sources.json에서 Python 버전 읽기
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$sourcesJsonPath = Join-Path $scriptDir "..\..\config\sources.json"
$requiredPyMinor = "3.14"  # 기본값 (sources.json 파싱 실패 시 사용)

if (Test-Path $sourcesJsonPath) {
    $sourcesConfig = Get-Content $sourcesJsonPath -Raw | ConvertFrom-Json
    $pythonStack = $sourcesConfig.tech_stacks | Where-Object { $_.name -eq "python" } | Select-Object -First 1
    if ($pythonStack -and $pythonStack.version -match "^(\d+\.\d+)") {
        $requiredPyMinor = $Matches[1]
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Nuitka Build Automation (Python $requiredPyMinor.x)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. 파이썬 버전 검증 (patch 버전은 무시하고 minor 버전만 확인)
Write-Host "[1/4] Python $requiredPyMinor.x 버전 검증 확인 중..."
$pyVerRaw = python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" 2>&1
$escapedMinor = [regex]::Escape($requiredPyMinor)
if ($pyVerRaw -notmatch "^$escapedMinor\.") {
    Write-Error "Python $requiredPyMinor.x 환경이 아닙니다. 현재 감지된 버전: $pyVerRaw"
}
Write-Host "  -> Python $pyVerRaw 확인 완료." -ForegroundColor Green

# 2. 대상 경로 입력값
Write-Host "[2/4] 대상 파일 준비..."
$targetFile = Read-Host "빌드 대상 스크립트 경로 입력 (예: src/app.py)"
if (-not (Test-Path $targetFile)) {
    Write-Error "대상 파일을 찾을 수 없습니다: $targetFile"
}

# 3. Nuitka 프로세스 시작
Write-Host "[3/4] Nuitka 컴파일 수행 파라미터 구성 및 시작..." -ForegroundColor Yellow
$nuitkaArgs = @(
    "--standalone",
    "--onefile",
    "--windows-disable-console",
    "--windows-uac-admin",       # Windows 11 권한 요청 대응 및 UAC
    "--show-progress",           # 진행 간 정체 파악
    "--output-dir=dist",
    $targetFile
)

try {
    Write-Host " [실행명령] python -m nuitka $($nuitkaArgs -join ' ')" -ForegroundColor DarkGray
    python -m nuitka @nuitkaArgs
} catch {
    Write-Error "빌드 중 오류가 발생했습니다. 메시지: $_"
}

# 4. 결과 물리적 확인
Write-Host "[4/4] 결과물 확인..."
$distPath = "dist"
if (Test-Path $distPath) {
    $exeFiles = Get-ChildItem -Path $distPath -Filter "*.exe" -Recurse
    if ($exeFiles.Count -gt 0) {
        Write-Host "빌드 결과물 감지 성공." -ForegroundColor Green
        foreach ($exe in $exeFiles) {
            $mbSize = [math]::Round($exe.Length / 1MB, 2)
            Write-Host "  -> $($exe.Name) ($mbSize MB) - $($exe.FullName)"
        }
    } else {
        Write-Warning "dist 폴더가 있으나 .exe 파일이 존재하지 않습니다."
    }
} else {
    Write-Error "dist 디렉토리 생성 실패."
}
Write-Host "========================================" -ForegroundColor Cyan
