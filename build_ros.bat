@echo off
setlocal

echo Checking for ROS 2 installation...

if exist "C:\dev\ros2_humble\local_setup.bat" (
    echo Found ROS 2 Humble in C:\dev\ros2_humble
    call "C:\dev\ros2_humble\local_setup.bat"
    goto :build
)

if exist "C:\opt\ros\humble\x64\setup.bat" (
    echo Found ROS 2 Humble in C:\opt\ros\humble
    call "C:\opt\ros\humble\x64\setup.bat"
    goto :build
)

if exist "C:\dev\ros2_iron\local_setup.bat" (
    echo Found ROS 2 Iron in C:\dev\ros2_iron
    call "C:\dev\ros2_iron\local_setup.bat"
    goto :build
)

if exist "C:\opt\ros\iron\x64\setup.bat" (
    echo Found ROS 2 Iron in C:\opt\ros\iron
    call "C:\opt\ros\iron\x64\setup.bat"
    goto :build
)

echo ROS 2 installation not found in standard locations.
echo Please ensure ROS 2 is installed and sourced.
exit /b 1

:build
echo Sourcing complete. Running colcon build...
colcon build --symlink-install
if %errorlevel% neq 0 (
    echo Build failed!
    exit /b %errorlevel%
)
echo Build successful!
endlocal
