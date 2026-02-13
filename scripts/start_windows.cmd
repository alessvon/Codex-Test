@echo off
setlocal

if exist ".venv\Scripts\python.exe" goto :run

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -m venv .venv
) else (
  python -m venv .venv
)

:run
.venv\Scripts\python.exe -m pip install -e .[dev]
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
