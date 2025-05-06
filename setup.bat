@echo off
REM setup.bat - Windows version of setup script for SenseBridge

echo Installing required Python packages...
pip install -r requirements.txt

echo Setting up environment variables...
set SENSEBRIDGE_HOME=%CD%
setx SENSEBRIDGE_HOME "%CD%"

echo Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "data" mkdir data
if not exist "models\yamnet_model" mkdir models\yamnet_model

echo Creating empty __init__.py files where needed...
echo. > models\yamnet_model\__init__.py

echo Setup completed successfully!
exit /b 0