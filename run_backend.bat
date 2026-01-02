@echo off
set PYTHONPATH=%CD%
echo Starting Mission Control Backend...
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
if %errorlevel% neq 0 (
    echo Backend failed to start.
    pause
)
