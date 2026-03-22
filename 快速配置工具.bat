@echo off
chcp 65001 >nul
echo ========================================
echo P1时光WoW - 一键修改realmlist工具
echo ========================================
echo.
echo 此工具将修改你的WoW客户端连接到P1时光服务器
echo.
echo 服务器IP: 1.14.59.54
echo 端口: 3724 (登录), 8085 (游戏)
echo.
echo ========================================
echo.

REM 检查是否有管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 建议以管理员身份运行
    echo.
)

REM 提示用户输入WoW客户端路径
set /p wow_path="请输入WoW客户端目录路径（例如 C:\World of Warcraft）: "

REM 检查路径是否存在
if not exist "%wow_path%" (
    echo.
    echo [错误] 路径不存在: %wow_path%
    pause
    exit /b 1
)

REM 检查是否有Wow.exe
if not exist "%wow_path%\Wow.exe" (
    echo.
    echo [警告] 未找到Wow.exe，可能不是WoW客户端目录
    set /p continue="是否继续？(y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo [1/3] 备份原realmlist.wtf...
if exist "%wow_path%\realmlist.wtf" (
    copy "%wow_path%\realmlist.wtf" "%wow_path%\realmlist.wtf.backup" >nul
    echo       已备份到: realmlist.wtf.backup
) else (
    echo       原文件不存在，跳过备份
)

echo.
echo [2/3] 修改realmlist.wtf...
echo set realmlist 1.14.59.54 > "%wow_path%\realmlist.wtf"
echo       已修改为: set realmlist 1.14.59.54

echo.
echo [3/3] 创建启动快捷方式...
(
echo @echo off
echo cd /d "%wow_path%"
echo start Wow.exe
) > "%wow_path%\启动P1时光WoW.bat"

echo       快捷方式已创建: 启动P1时光WoW.bat

echo.
echo ========================================
echo ✅ 配置完成！
echo ========================================
echo.
echo 📋 下一步：
echo.
echo 1. 注册账号
echo    访问: http://1.14.59.54:5000
echo    或联系管理员
echo.
echo 2. 启动游戏
echo    方式1: 双击 "启动P1时光WoW.bat"
echo    方式2: 运行Wow.exe
echo.
echo 3. 登录游戏
echo    输入注册的账号密码
echo.
echo ========================================
echo 恢复原始设置：
echo ========================================
echo.
echo 如果需要切换回其他服务器：
echo    重命名 realmlist.wtf.backup 为 realmlist.wtf
echo.
pause
