$ErrorActionPreference = "Stop"

$dest_path = "python38_portable"
if (-not (Test-Path $dest_path)) {
    New-Item -ItemType Directory -Path $dest_path
}

$url = "https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip"
$zip = "python38.zip"

Write-Host "Downloading Portable Python 3.8..."
Invoke-WebRequest -Uri $url -OutFile $zip

Write-Host "Extracting Python 3.8..."
Expand-Archive -Path $zip -DestinationPath $dest_path -Force

Remove-Item $zip

Write-Host "Portable Python 3.8 ready in $dest_path"
