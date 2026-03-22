@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo P1时光WoW登录器 - Windows打包工具
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python已安装
python --version
echo.

REM 检查是否在正确的目录
if not exist "wow_launcher.py" (
    echo [错误] 未找到wow_launcher.py
    echo 请在wow_launcher目录下运行此脚本
    pause
    exit /b 1
)

echo [1/6] 升级pip...
python -m pip install --upgrade pip --quiet
echo      完成
echo.

echo [2/6] 安装依赖...
pip install pyinstaller pillow --quiet
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo      完成
echo.

echo [3/6] 清理旧文件...
if exist build rmdir /s /q build >nul 2>&1
if exist dist rmdir /s /q dist >nul 2>&1
if exist __pycache__ rmdir /s /q __pycache__ >nul 2>&1
if exist *.spec del /q *.spec >nul 2>&1
echo      完成
echo.

echo [4/6] 开始打包...
echo      这可能需要1-2分钟...
echo.

pyinstaller --clean --noconfirm ^
    --onefile ^
    --windowed ^
    --name "P1时光WoW登录器" ^
    --add-data "launcher_config.json;." ^
    --hidden-import=PIL._tkinter_finder ^
    wow_launcher.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败
    echo 请查看上面的错误信息
    pause
    exit /b 1
)

echo.
echo [✓] 打包成功
echo.

echo [5/6] 创建发布包...
if not exist dist\发布包 mkdir dist\发布包

copy "dist\P1时光WoW登录器.exe" "dist\发布包\" >nul
copy "launcher_config.json" "dist\发布包\" >nul
copy "README.md" "dist\发布包\" >nul 2>&1

REM 创建使用说明
(
echo P1时光WoW登录器 使用说明
echo ================================
echo.
echo 📋 服务器信息：
echo    服务器IP: 1.14.59.54
echo    登录端口: 3724
echo    游戏端口: 8085
echo    注册地址: http://1.14.59.54:5000
echo.
echo 🚀 使用步骤：
echo    1. 双击运行 "P1时光WoW登录器.exe"
echo    2. 首次运行点击"浏览"选择WoW客户端目录
echo    3. 点击"注册账号"按钮创建账号
echo    4. 返回登录器，点击"启动游戏"
echo    5. 输入账号密码登录游戏
echo.
echo ⚠️ 注意事项：
echo    • 必须使用WoW 3.3.5a (12340) 客户端
echo    • 确保客户端目录有Wow.exe文件
echo    • 防火墙可能需要允许
echo    • 杀毒软件可能误报，添加信任即可
echo.
echo 🔧 自定义配置：
echo    编辑 launcher_config.json 可以修改：
echo    - 服务器名称
echo    - 注册网址
echo    - 官网地址
echo.
echo 📞 技术支持：
echo    如有问题请联系管理员
echo.
echo 🎮 祝游戏愉快！
) > "dist\发布包\使用说明.txt"

REM 创建realmlist备份说明
(
echo realmlist.wtf 原始内容备份
echo ================================
echo 如果你需要切换回其他服务器，
echo 请将WoW客户端目录下的realmlist.wtf改回以下内容：
echo.
echo set realmlist cn.logon.worldofwarcraft.com
echo set patchlist cn.version.worldofwarcraft.com
) > "dist\发布包\realmlist备份说明.txt"

echo      完成
echo.

echo [6/6] 计算文件大小...
for %%A in ("dist\发布包\P1时光WoW登录器.exe") do (
    set size=%%~zA
    set /a sizeMB=!size! / 1048576
)
echo      登录器大小: !sizeMB! MB
echo.

echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 📂 输出目录: %cd%\dist\发布包\
echo.
echo 📦 文件列表:
dir /b "dist\发布包"
echo.
echo 💽 总大小:
for /f "tokens=3" %%a in ('dir /-c "dist\发布包" ^| find "个文件"') do set total=%%a
echo    !total! 字节
echo.
echo ========================================
echo 下一步：
echo ========================================
echo.
echo 1. 测试登录器
echo    运行: dist\发布包\P1时光WoW登录器.exe
echo.
echo 2. 分发给玩家
echo    将 "发布包" 目录打包成ZIP
echo    上传到网盘或服务器供玩家下载
echo.
echo 3. 部署注册网页
echo    参考: 注册网页部署完整指南.md
echo.
pause
