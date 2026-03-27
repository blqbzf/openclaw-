@echo off
setlocal
REM === 诺兰时光魔兽启动脚本 ===
REM 直接启动游戏， 无需登录器

echo ========================================
echo   诺兰时光魔兽 - 直接启动
echo ========================================
echo.

REM 检查客户端路径
if not exist "Wow.exe" (
    echo [错误] 未找到 Wow.exe
    echo 请确保此脚本放在WoW客户端目录中
    pause
    exit /b 1
)

REM 更新 realmlist
echo [1/3] 更新 realmlist...
echo set realmlist 1.14.59.54 > realmlist.wtf

REM 清理缓存
echo [2/3] 清理缓存...
if exist "Cache" rd /s /q Cache
if exist "WDB" rd /s /q WDB
if exist "Errors" rd /s /q Errors

REM 启动游戏
echo [3/3] 启动游戏...
start Wow.exe

echo ========================================
echo   游戏已启动！
echo ========================================
echo.
echo 提示： 
echo - 如提示版本错误， 请确保使用 3.3.5a (12340) 客户端
echo - 如提示缺少补丁
 请下载：http://1.14.59.54:8080/patches/patch-A.MPQ
echo - 将 patch-A.MPQ 放到 Data 目录
echo.
pause
