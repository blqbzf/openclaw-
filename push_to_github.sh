#!/bin/bash
# P1时光WoW登录器 - GitHub上传脚本

echo "=== P1时光WoW登录器 - 推送到GitHub ==="
echo ""

cd /Users/mac/Documents/bobo/boboai/test_1_openclaw/wow_launcher

echo "1. 检查Git状态..."
git status
echo ""

echo "2. 添加远程仓库..."
echo ""
echo "请选择："
echo "  1. 创建新仓库（p1-wow-launcher）"
echo "  2. 使用现有仓库（openclaw-）"
echo ""
read -p "选择 (1或2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "请在GitHub网页创建新仓库："
    echo "  访问: https://github.com/new"
    echo "  仓库名: p1-wow-launcher"
    echo "  描述: P1时光WoW私服登录器"
    echo "  设置: Public"
    echo "  不要勾选: README、.gitignore、license"
    echo ""
    read -p "创建完成后按回车继续..."

    git remote add origin https://github.com/blqbzf/p1-wow-launcher.git
    git branch -M main
    git push -u origin main

    echo ""
    echo "3. 创建发布标签..."
    git tag -a v1.0.0 -m "P1时光WoW登录器 v1.0.0

功能：
- 自动修改realmlist.wtf
- 一键启动游戏
- 服务器状态显示
- 新闻公告系统
- 账号注册链接
- 跨平台支持（Windows + Mac）"

    git push origin v1.0.0

elif [ "$choice" = "2" ]; then
    echo ""
    echo "使用现有仓库..."
    git remote add origin https://github.com/blqbzf/openclaw-.git
    git branch -M launcher
    git push -u origin launcher

    echo ""
    echo "3. 创建发布标签..."
    git tag -a launcher-v1.0.0 -m "P1时光WoW登录器 v1.0.0"
    git push origin launcher-v1.0.0
fi

echo ""
echo "========================================"
echo "✅ 推送完成！"
echo "========================================"
echo ""
echo "📦 GitHub Actions正在自动打包..."
echo ""
echo "查看进度："
echo "  https://github.com/blqbzf/p1-wow-launcher/actions"
echo "  或"
echo "  https://github.com/blqbzf/openclaw-/actions"
echo ""
echo "下载exe（约5分钟后）："
echo "  Actions → 最新的workflow → Artifacts → windows-launcher"
echo ""
echo "按任意键打开浏览器..."
read -n 1 -s
open "https://github.com/blqbzf?tab=repositories"
