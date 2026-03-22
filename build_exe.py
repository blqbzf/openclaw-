#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1时光WoW登录器打包脚本
支持跨平台打包Windows exe
"""

import os
import sys
import shutil
import subprocess

def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_exe():
    """打包成exe"""
    print("\n🔨 开始打包P1时光WoW登录器...")
    
    # 检查PyInstaller
    if not check_pyinstaller():
        print("❌ PyInstaller安装失败")
        return False
    
    # 清理旧文件
    if os.path.exists("dist"):
        print("清理旧的打包文件...")
        shutil.rmtree("dist")
    
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller参数
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",                    # 打包成单个exe
        "--windowed",                   # 窗口模式（无控制台）
        "--name=P1时光WoW登录器",        # exe名称
        "--clean",                      # 清理临时文件
        "wow_launcher.py"
    ]
    
    # 如果有图标，添加图标参数
    if os.path.exists("icon.ico"):
        cmd.insert(3, "--icon=icon.ico")
    
    print("\n执行打包命令：")
    print(" ".join(cmd))
    print()
    
    # 执行打包
    try:
        subprocess.check_call(cmd)
        print("\n✅ 打包成功！")
        
        # 复制配置文件到dist目录
        print("\n复制配置文件...")
        if not os.path.exists("dist"):
            os.makedirs("dist")
        
        if os.path.exists("launcher_config.json"):
            shutil.copy("launcher_config.json", "dist/")
            print("✅ 配置文件已复制")
        
        # 创建使用说明
        readme = """P1时光WoW登录器 使用说明
================================

1. 首次运行：
   - 双击 P1时光WoW登录器.exe
   - 点击"浏览"选择WoW客户端目录
   - 确保目录下有 Wow.exe 文件

2. 启动游戏：
   - 设置好路径后，点击"启动游戏"
   - 登录器会自动修改 realmlist.wtf
   - 然后启动WoW客户端

3. 自定义配置（可选）：
   - 编辑 launcher_config.json
   - 可以修改服务器信息、网址等
   - 保存后重启登录器即可

4. 注册账号：
   - 点击"注册账号"按钮
   - 在网页上完成注册

5. 注意事项：
   - 确保使用3.3.5a客户端
   - 防火墙可能需要允许
   - 杀毒软件可能误报，添加信任即可

有问题请联系管理员

祝游戏愉快！
"""
        
        with open("dist/使用说明.txt", "w", encoding="utf-8") as f:
            f.write(readme)
        
        print("✅ 使用说明已创建")
        
        print("\n" + "="*50)
        print("📦 打包完成！")
        print("="*50)
        print("\n输出文件位置：")
        print(f"  可执行文件: {os.path.abspath('dist/P1时光WoW登录器.exe')}")
        print(f"  配置文件: {os.path.abspath('dist/launcher_config.json')}")
        print(f"  使用说明: {os.path.abspath('dist/使用说明.txt')}")
        print("\n请将 dist 目录中的所有文件打包分发！")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败：{e}")
        return False

def main():
    print("="*50)
    print("P1时光WoW登录器 - 打包工具")
    print("="*50)
    
    if build_exe():
        print("\n✅ 所有步骤完成！")
    else:
        print("\n❌ 打包过程出错")
        sys.exit(1)

if __name__ == "__main__":
    main()
