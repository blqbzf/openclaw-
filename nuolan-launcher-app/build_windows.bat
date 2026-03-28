@echo off
setlocal
cd /d %~dp0

echo [1/4] Checking Python...
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher ^(py^) not found.
  exit /b 1
)

echo [2/4] Creating virtual environment if missing...
if not exist .venv (
  py -3 -m venv .venv
)

echo [3/4] Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo [4/4] Building launcher...
python build_exe.py

if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo.
echo Build success.
echo Output: dist\NuolanWoWLauncher\
endlocal
