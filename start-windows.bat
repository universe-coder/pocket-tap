@echo off
rem First run creates a local Python environment and installs dependencies.
cd /d "%~dp0"
if not exist .venv (
    py -3 -m venv .venv || python -m venv .venv || (echo Install Python 3.9+ from https://www.python.org/downloads/ & pause & exit /b 1)
    .venv\Scripts\python -m pip install -r requirements.txt || (pause & exit /b 1)
)
.venv\Scripts\python -m pc_remote %*
pause
