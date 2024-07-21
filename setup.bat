@echo off
echo Installing the required components...

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and add it to the PATH.
    pause
    exit /b
)

:: Check if pip is installed
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip is not installed. Please install pip.
    pause
    exit /b
)

:: Install required Python packages
echo Installing required Python packages...
pip install selenium

:: Download ChromeDriver
echo Downloading ChromeDriver...
SET chromedriver_version=126.0.6478.182
powershell -command "Invoke-WebRequest https://chromedriver.storage.googleapis.com/%chromedriver_version%/chromedriver_win32.zip -OutFile chromedriver.zip"
powershell -command "Expand-Archive chromedriver.zip -DestinationPath ."
del chromedriver.zip

echo Adding ChromeDriver to PATH...
SET PATH=%PATH%;%CD%

echo Setup is complete.
pause
