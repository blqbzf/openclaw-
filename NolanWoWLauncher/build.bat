@echo off
REM 构建脚本 - Windows 单文件版本

echo ========================================
echo 诺兰时光 WoW 登录器 - 构建脚本
echo ========================================
echo.

REM 清理旧文件
if exist "bin\Release" rmdir /s /q "bin\Release"
if exist "obj" rmdir /s /q "obj"

echo [1/3] 还原 NuGet 包...
dotnet restore
if errorlevel 1 (
    echo ❌ 还原失败
    pause
    exit /b 1
)

echo.
echo [2/3] 构建项目...
dotnet build -c Release
if errorlevel 1 (
    echo ❌ 构建失败
    pause
    exit /b 1
)

echo.
echo [3/3] 发布单文件可执行程序...
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -p:PublishTrimmed=true

if errorlevel 1 (
    echo ❌ 发布失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 构建成功！
echo ========================================
echo.
echo 输出文件: bin\Release\net8.0-windows\win-x64\publish\NolanWoWLauncher.exe
echo.
explorer "bin\Release\net8.0-windows\win-x64\publish"
pause
