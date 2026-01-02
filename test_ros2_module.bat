@echo off
set "ROS2_ROOT=%~dp0ros2_install\ros2-windows"
set "PYTHONPATH=%ROS2_ROOT%\Lib\site-packages;%PYTHONPATH%"
set "PATH=%ROS2_ROOT%\bin;%PATH%"
echo [DEBUG] PYTHONPATH: %PYTHONPATH%
echo [DEBUG] PATH: %PATH%
echo [DEBUG] Testing ros2cli...
python -m ros2cli.cli --help
if %errorlevel% neq 0 (
    echo [ERROR] ros2cli failed with errorlevel %errorlevel%
)
