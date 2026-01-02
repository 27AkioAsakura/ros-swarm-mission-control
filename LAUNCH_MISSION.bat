@echo off
echo ---------------------------------------------------
echo  NASA-GRADE MISSION CONTROL SYSTEM
echo  Initializing Swarm Intelligence ^& Mission Control...
echo ---------------------------------------------------

:: Set PYTHONPATH to current directory so backend module is found
set PYTHONPATH=%CD%

:: Start Backend in a new window
echo [INFO] Starting Backend API (FastAPI)...
start "Mission Control Backend" cmd /k python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

:: Wait for backend to initialize
timeout /t 3 > nul

:: Start Frontend Server
echo [INFO] Starting Frontend Server...
start "Mission Control Frontend" cmd /k "cd mission_control_web && python -m http.server 8080"

:: Wait for frontend server to start
timeout /t 2 > nul

:: Open Dashboard in Browser
echo [INFO] Opening Mission Control Dashboard...
start http://localhost:8080

echo ---------------------------------------------------
echo  SYSTEM INITIALIZED
echo  Backend: http://localhost:8000
echo  Frontend: http://localhost:8080
echo  Login: admin / password
echo ---------------------------------------------------
pause
