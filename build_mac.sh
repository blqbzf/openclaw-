#!/bin/bash
# P1时光WoW登录器 - 一键打包脚本（Mac/Linux）

echo "========================================"
echo "P1时光WoW登录器 - 打包工具"
echo "========================================"
echo ""

# 检查Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi

echo "✅ Python版本："
python3 --version
echo ""

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt
echo ""

# 执行打包
echo "🔨 开始打包..."
python3 build_exe.py

echo ""
echo "按任意键退出..."
read -n 1 -s
