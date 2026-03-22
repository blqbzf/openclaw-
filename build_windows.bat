@echo off
chcp 65001 >nul
echo ========================================
echo P1时光WoW登录器打包脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [2/4] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [3/4] 开始打包...
pyinstaller --clean ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "P1时光WoW登录器" ^
    --add-data "launcher_config.json;." ^
    --icon=icon.ico ^
    wow_launcher.py

if %errorlevel% neq 0 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [4/4] 复制配置文件...
copy launcher_config.json dist\ >nul 2>&1

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 输出目录: dist\
echo 可执行文件: dist\P1时光WoW登录器.exe
echo 配置文件: dist\launcher_config.json
echo.
echo 使用说明：
echo 1. 将 dist\ 目录中的所有文件复制给玩家
echo 2. 玩家首次运行需要设置WoW客户端路径
echo 3. 修改 launcher_config.json 可以自定义配置
echo.
pause
