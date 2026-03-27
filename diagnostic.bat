@echo off
chcp 65001 >nul
echo ========================================
echo  诺兰时光魔兽 - 诊断工具 v1.0
echo ========================================
echo.

echo [1] 检查客户端版本...
if exist "Wow.exe" (
    echo     √ Wow.exe 存在
    echo     注意: 请右键 Wow.exe -^> 属性 -^> 详细信息
    echo     确认文件版本是: 3.3.5.12340
) else (
    echo     × 未找到 Wow.exe
    echo     请确认你在 WoW 客户端目录中运行此工具
    pause
    exit /b 1
)

echo.
echo [2] 检查 realmlist.wtf...
if exist "realmlist.wtf" (
    type realmlist.wtf | find "1.14.59.54" >nul
    if %errorlevel% equ 0 (
        echo     √ realmlist 正确
    ) else (
        echo     × realmlist 错误，正在修复...
        echo set realmlist 1.14.59.54 > realmlist.wtf
        echo     √ 已修复
    )
) else (
    echo     × realmlist.wtf 不存在，正在创建...
    echo set realmlist 1.14.59.54 > realmlist.wtf
    echo     √ 已创建
)

echo.
echo [3] 检查 patch-A.MPQ...
if exist "Data\patch-A.MPQ" (
    echo     √ patch-A.MPQ 存在
) else (
    echo     × patch-A.MPQ 缺失
    echo     请下载: http://1.14.59.54:8080/patches/current/patch-A.MPQ
    echo     大小: 199MB
    echo     放置位置: Data\patch-A.MPQ
)

echo.
echo [4] 检查缓存目录...
if exist "Cache" (
    echo     发现 Cache 目录，建议删除
    choice /C YN /M "    是否删除 Cache 目录"
    if %errorlevel% equ 1 (
        rd /s /q Cache 2>nul
        echo     √ 已删除 Cache
    )
)

if exist "WDB" (
    echo     发现 WDB 目录，建议删除
    choice /C YN /M "    是否删除 WDB 目录"
    if %errorlevel% equ 1 (
        rd /s /q WDB 2>nul
        echo     √ 已删除 WDB
    )
)

if exist "Errors" (
    echo     发现 Errors 目录，建议删除
    choice /C YN /M "    是否删除 Errors 目录"
    if %errorlevel% equ 1 (
        rd /s /q Errors 2>nul
        echo     √ 已删除 Errors
    )
)

echo.
echo [5] 测试服务器连接...
ping -n 1 1.14.59.54 >nul 2>&1
if %errorlevel% equ 0 (
    echo     √ 服务器可达
) else (
    echo     × 无法连接服务器
    echo     请检查网络连接
)

echo.
echo [6] 检查端口...
powershell -Command "Test-NetConnection -ComputerName 1.14.59.54 -Port 3724 -InformationLevel Quiet" >nul 2>&1
if %errorlevel% equ 0 (
    echo     √ 登录端口 3724 开放
) else (
    echo     × 登录端口 3724 无法访问
)

powershell -Command "Test-NetConnection -ComputerName 1.14.59.54 -Port 8085 -InformationLevel Quiet" >nul 2>&1
if %errorlevel% equ 0 (
    echo     √ 游戏端口 8085 开放
) else (
    echo     × 游戏端口 8085 无法访问
)

echo.
echo ========================================
echo  诊断完成
echo ========================================
echo.
echo 如果所有检查都通过，但仍然无法登录：
echo 1. 确认客户端版本是 3.3.5a (12340)
echo 2. 确认已下载并安装 patch-A.MPQ
echo 3. 确认已注册账号 (http://1.14.59.54:5000)
echo 4. 尝试使用管理员权限运行登录器
echo.
pause
