@echo off

echo ======================================================
echo  Tech-Stack-Organizer: Documentation Pipeline Starting
echo ======================================================

rem [1/5] Virtual Environment Setup
if not exist .venv (
    echo [1/5] .venv not found. Creating virtual environment...
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
    echo [1/5] Virtual environment created successfully.
) else (
    if not exist .venv\Scripts\python.exe (
        echo [WARNING] .venv folder exists but Scripts\python.exe is missing.
        echo Re-creating virtual environment...
        rd /s /q .venv
        uv venv
    ) else (
        echo [1/5] Virtual environment found and valid.
    )
)

rem [2/5] Installing Dependencies
echo [2/5] Installing dependencies from requirements.txt...
uv pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [2/5] Dependencies ready.

rem [3/5] Bootstrapping Rules
echo [3/5] Bootstrapping Senior Architect rules...
.venv\Scripts\python.exe tools/automation/bootstrap-rules.py
if errorlevel 1 (
    echo [WARNING] Bootstrapping failed.
)

rem [4/5] Auto-Discovery
echo [4/5] Checking config/sources.json...
if not exist config\sources.json (
    echo [4/5] config/sources.json not found. Running Auto-Discovery...
    .venv\Scripts\python.exe tools/automation/discover-stack.py
    if errorlevel 1 (
        echo [WARNING] Auto-Discovery failed. Please create config/sources.json manually.
    )
) else (
    echo [4/5] config/sources.json found. Skipping discovery.
)

rem [5/5] Running Doc-Fetcher
echo [5/5] Running Doc-Fetcher...
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
