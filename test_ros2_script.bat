@echo off
set "ROS2_ROOT=%~dp0ros2_install\ros2-windows"
set "PYTHONPATH=%ROS2_ROOT%\Lib\site-packages;%PYTHONPATH%"
set "PATH=%ROS2_ROOT%\bin;%PATH%"
echo [DEBUG] Testing ros2-script.py with current python...
python "%ROS2_ROOT%\Scripts\ros2-script.py" --help
