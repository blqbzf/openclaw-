#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v3.3.1 → v4.0.0 升级脚本
添加远程账号注册功能
"""

import os
import shutil

# 1. 更新主程序（添加注册对话框)
print("更新主程序...")
with open('wow_launcher.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 添加导入
if 'from register_dialog import RegisterDialog' not in content:
    content = content.replace(
        'from tkinter import messagebox, filedialog, ttk',
        'from tkinter import messagebox, filedialog, ttk\nfrom register_dialog import RegisterDialog'
        1
    )
    
# 修改 open_register 函数
print("修改注册函数...")
content = content.replace(
    '''def open_register(self):
        """打开注册页面"""
        import webbrowser
        if self.config.get("register_url"):
            webbrowser.open(self.config["register_url"])
        else:
            messagebox.showinfo("提示", "请联系管理员获取注册地址")''',
    '''def open_register(self):
        """打开注册对话框"""
        RegisterDialog(self.root, self.config)'''
)

# 写回文件
with open('wow_launcher.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 更新完成！ v4.0.0")
print("新增功能:")
print("  • 远程账号注册（无需网页）")
print("  • 直接连接服务器 API")
print("  • 自动填写服务器 IP")
