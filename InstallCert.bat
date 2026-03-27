@echo off
REM Install certificate to Trusted Root CA store
REM Run this script as Administrator

echo ============================================
echo  NolanWoW Launcher - Certificate Installer
echo ============================================
echo.

REM Check if certificate file exists
if not exist NolanWoW.cer (
    echo Error: NolanWoW.cer not found.
    echo Please run CreateCert.bat first.
    echo.
    pause
    exit /b 1
)

REM Install certificate to Trusted Root CA
certutil -addstore -f "Root" NolanWoW.cer

if %ERRORLEVEL% NEQ 0 (
    echo Error installing certificate
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Certificate installed successfully!
echo ============================================
echo.
echo The launcher will now run without Windows
echo SmartScreen warnings.
echo.
pause
