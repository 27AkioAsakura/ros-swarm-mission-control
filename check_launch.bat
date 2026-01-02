@echo off
set "PYTHONPATH=%~dp0ros2_install\ros2-windows\Lib\site-packages;%PYTHONPATH%"
python -c "import launch; import launch_ros; print('Launch modules found')"
