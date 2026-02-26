@echo off

echo ======================================================
echo  Tech-Stack-Organizer: Documentation Pipeline Starting
echo ======================================================

:: [1/3] 가상환경 생성 (없을 경우 자동 설치)
if not exist .venv (
    echo [1/3] .venv not found. Creating virtual environment...
    where uv >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] 'uv' is not installed or not in PATH.
        echo Please install uv first: https://github.com/astral-sh/uv
        pause
        exit /b 1
    )
    uv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [1/3] Virtual environment created successfully.
) else (
    echo [1/3] Virtual environment found. Skipping creation.
)

:: [2/3] 의존성 설치
echo [2/3] Installing dependencies from requirements.txt...
uv pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [2/3] Dependencies ready.

:: [3/4] 자동 기술 탐지 (config/sources.json이 없을 경우)
if not exist config\sources.json (
    echo [3/4] config/sources.json not found. Running Auto-Discovery...
    .venv\Scripts\python.exe tools/automation/discover-stack.py
    if errorlevel 1 (
        echo [WARNING] Auto-Discovery failed. Please create config/sources.json manually.
    )
) else (
    echo [3/4] config/sources.json found. Skipping discovery.
)

:: [4/4] Doc-Fetcher 실행
echo [4/4] Running Doc-Fetcher...
echo ------------------------------------------------------
.venv\Scripts\python.exe tools/automation/update-docs.py %*
if errorlevel 1 (
    echo [ERROR] Failed to run update-docs.py
    pause
    exit /b 1
) else (
    echo [SUCCESS] Sync completed.
)
echo ------------------------------------------------------

echo ======================================================
pause
