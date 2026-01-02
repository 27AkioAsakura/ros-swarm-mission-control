@echo off
set "ROS2_SCRIPTS=%~dp0ros2_install\ros2-windows\Scripts"
set "PATH=%ROS2_SCRIPTS%;%PATH%"
echo [DEBUG] PATH: %PATH%
echo [DEBUG] Testing ros2 command...
ros2 --help
