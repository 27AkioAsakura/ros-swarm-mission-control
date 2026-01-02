@echo off
echo ========================================
echo  NASA SWARM MISSION CONTROL - LAUNCHER
echo ========================================
echo.
echo Starting Backend Server...
start "Mission Control Backend" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Mission Control Frontend" cmd /k "python -m http.server 5173 --directory mission_control_web"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo  SERVERS STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Login Credentials:
echo   Username: admin
echo   Password: password
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo Press any key to stop all servers...
pause >nul

echo.
echo Stopping servers...
taskkill /FI "WINDOWTITLE eq Mission Control Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Mission Control Frontend*" /T /F >nul 2>&1

echo.
echo All servers stopped.
echo.
pause
