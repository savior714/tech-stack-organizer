@echo off
setlocal enabledelayedexpansion

REM ==========================================================
REM Tech-Stack-Organizer: Documentation Pipeline Starter
REM Environment: Windows 11 Native (ANSI/CP949 Encoding)
REM ==========================================================

chcp 949 >nul
echo ======================================================
echo  Tech-Stack-Organizer: 지식 수집 파이프라인 가동
echo ======================================================

REM 1. 가상환경(.venv) 존재 여부 확인
if not exist ".venv" (
    echo [ERROR] .venv 가상환경을 찾을 수 없습니다.
    echo uv를 사용하여 가상환경을 먼저 생성해주세요: uv venv
    pause
    exit /b 1
)

REM 2. 필수 라이브러리(httpx) 설치 확인 및 설치
echo [1/2] 필수 의존성 확인 중 (httpx)...
.venv\Scripts\python.exe -m pip show httpx >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] httpx가 설치되어 있지 않습니다. 설치를 시작합니다...
    .venv\Scripts\python.exe -m pip install httpx
) else (
    echo [OK] httpx 확인 완료.
)

REM 3. Python 스크립트 실행
echo [2/2] Doc-Fetcher 엔진 가동 (update-docs.py)...
echo ------------------------------------------------------
.venv\Scripts\python.exe tools/automation/update-docs.py
echo ------------------------------------------------------

if %errorlevel% neq 0 (
    echo [ERROR] 스크립트 실행 중 문제가 발생했습니다. 로그를 확인해주세요.
) else (
    echo [SUCCESS] 모든 기술 채널의 지식 동기화가 완료되었습니다.
)

echo ======================================================
pause
