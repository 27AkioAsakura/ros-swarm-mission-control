$ErrorActionPreference = "Stop"

Write-Host "Checking Python..."
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed. Please install Python 3.8+ and add it to PATH."
    exit 1
}

Write-Host "Installing ROS 2 build tools (colcon, etc)..."
pip install -U colcon-common-extensions vcstool lxml
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install python dependencies."
    exit 1
}

$ros2_url = "https://github.com/ros2/ros2/releases/download/release-humble-20230614/ros2-humble-20230614-windows-release-amd64.zip"
$zip_path = "ros2_install\ros2.zip"
$dest_path = "ros2_install"

if (-not (Test-Path $dest_path)) {
    New-Item -ItemType Directory -Force -Path $dest_path
}

if (-not (Test-Path "$dest_path\ros2-windows\local_setup.bat")) {
    Write-Host "Downloading ROS 2 Humble (this may take a while)..."
    Invoke-WebRequest -Uri $ros2_url -OutFile $zip_path
    
    Write-Host "Extracting ROS 2..."
    Expand-Archive -Path $zip_path -DestinationPath $dest_path -Force
    
    Remove-Item $zip_path
}
else {
    Write-Host "ROS 2 already downloaded."
}

Write-Host "ROS 2 Installed locally in $dest_path\ros2-windows"
