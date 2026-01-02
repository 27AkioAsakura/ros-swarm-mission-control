import sys
try:
    from ros2cli.cli import main
    print("ROS2CLI Found!")
except ImportError as e:
    print(f"ImportError: {e}")
    print(sys.path)
