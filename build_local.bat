@echo off
setlocal

set "ROS2_PATH=%~dp0ros2_install\ros2-windows"

if not exist "%ROS2_PATH%\local_setup.bat" (
    echo ROS 2 not found at %ROS2_PATH%
    echo Please run install_ros2.ps1 first.
    exit /b 1
)

echo Sourcing ROS 2 from %ROS2_PATH%...
call "%ROS2_PATH%\local_setup.bat"

echo Running colcon build...
colcon build --symlink-install --merge-install

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b %errorlevel%
)

echo Build successful!
echo To run the simulation, use:
echo call "%ROS2_PATH%\local_setup.bat"
echo call install\setup.bat
echo ros2 launch multi_robot_system multi_robot_simulation.launch.py
endlocal
