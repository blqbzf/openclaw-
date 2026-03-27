@echo off
REM Create self-signed certificate for NolanWoW Launcher
REM Run this script as Administrator

echo ============================================
echo  NolanWoW Launcher - Certificate Creator
echo ============================================
echo.

REM Check if makecert is available
where makecert >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: makecert not found.
    echo Please install Windows SDK or Visual Studio.
    echo.
    pause
    exit /b 1
)

REM Create certificate
makecert -r -pe -sha256 -len 2048 -sky exchange -n "CN=NolanWoW Launcher" -ss My -sr CurrentUser NolanWoW.cer

if %ERRORLEVEL% NEQ 0 (
    echo Error creating certificate
    pause
    exit /b 1
)

echo.
echo Certificate created successfully: NolanWoW.cer
echo.
echo Next step: Run InstallCert.bat as Administrator
echo.
pause
