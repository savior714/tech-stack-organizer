@echo off

echo ======================================================
echo  Tech-Stack-Organizer: Documentation Pipeline Starting
echo ======================================================

if not exist .venv (
    echo [ERROR] .venv found.
    echo Please run: uv venv
    pause
    exit /b 1
)

echo [1/1] Running Doc-Fetcher...
echo ------------------------------------------------------
.venv\Scripts\python.exe tools/automation/update-docs.py
if errorlevel 1 (
    echo [ERROR] Failed to run update-docs.py
) else (
    echo [SUCCESS] Sync completed.
)
echo ------------------------------------------------------

echo ======================================================
pause
