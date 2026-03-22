#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1时光WoW私服登录器
功能：修改realmlist、启动客户端、显示服务器信息
作者：波波AI
版本：v1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import sys
import json
from pathlib import Path
import shutil
from datetime import datetime

class WoWLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("P1时光WoW私服登录器 v1.0")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # 设置图标（如果有）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # 服务器配置
        self.config = {
            "server_name": "P1时光WoW",
            "server_ip": "1.14.59.54",
            "realmlist": "set realmlist 1.14.59.54",
            "patch_url": "",
            "register_url": "http://1.14.59.54/register",
            "website_url": "http://1.14.59.54",
            "discord_url": "",
            "version": "3.3.5a"
        }
        
        # 加载配置
        self.load_config()
        
        # 创建GUI
        self.create_widgets()
        
        # 检测客户端路径
        self.detect_client_path()
        
    def load_config(self):
        """加载配置文件"""
        config_file = "launcher_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except:
                pass
    
    def save_config(self):
        """保存配置文件"""
        config_file = "launcher_config.json"
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败：{e}")
    
    def create_widgets(self):
        """创建GUI组件"""
        
        # 顶部Logo区域
        logo_frame = tk.Frame(self.root, bg="#1a1a2e", height=120)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        title_label = tk.Label(
            logo_frame,
            text="⚔️ P1时光WoW私服 ⚔️",
            font=("微软雅黑", 24, "bold"),
            fg="#ffd700",
            bg="#1a1a2e"
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            logo_frame,
            text="3.3.5a 巫妖王之怒",
            font=("微软雅黑", 12),
            fg="#c0c0c0",
            bg="#1a1a2e"
        )
        subtitle_label.pack()
        
        # 服务器信息区域
        info_frame = tk.LabelFrame(
            self.root,
            text="📊 服务器信息",
            font=("微软雅黑", 10, "bold"),
            padx=10,
            pady=10
        )
        info_frame.pack(fill="x", padx=20, pady=10)
        
        # 服务器状态
        status_frame = tk.Frame(info_frame)
        status_frame.pack(fill="x", pady=5)
        
        tk.Label(status_frame, text="服务器状态:", font=("微软雅黑", 9)).pack(side="left")
        self.status_label = tk.Label(
            status_frame,
            text="🟢 在线",
            font=("微软雅黑", 9, "bold"),
            fg="green"
        )
        self.status_label.pack(side="left", padx=5)
        
        # 在线人数
        players_frame = tk.Frame(info_frame)
        players_frame.pack(fill="x", pady=5)
        
        tk.Label(players_frame, text="在线玩家:", font=("微软雅黑", 9)).pack(side="left")
        self.players_label = tk.Label(
            players_frame,
            text="检查中...",
            font=("微软雅黑", 9)
        )
        self.players_label.pack(side="left", padx=5)
        
        # 服务器IP
        ip_frame = tk.Frame(info_frame)
        ip_frame.pack(fill="x", pady=5)
        
        tk.Label(ip_frame, text="服务器IP:", font=("微软雅黑", 9)).pack(side="left")
        tk.Label(
            ip_frame,
            text=self.config["server_ip"],
            font=("微软雅黑", 9),
            fg="blue"
        ).pack(side="left", padx=5)
        
        # 客户端路径区域
        path_frame = tk.LabelFrame(
            self.root,
            text="📁 客户端设置",
            font=("微软雅黑", 10, "bold"),
            padx=10,
            pady=10
        )
        path_frame.pack(fill="x", padx=20, pady=10)
        
        # 客户端路径
        path_input_frame = tk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        tk.Label(path_input_frame, text="WoW路径:", font=("微软雅黑", 9)).pack(side="left")
        self.path_entry = tk.Entry(path_input_frame, font=("微软雅黑", 9), width=40)
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        browse_btn = tk.Button(
            path_input_frame,
            text="浏览",
            font=("微软雅黑", 9),
            command=self.browse_client
        )
        browse_btn.pack(side="left", padx=5)
        
        # 新闻/公告区域
        news_frame = tk.LabelFrame(
            self.root,
            text="📢 服务器公告",
            font=("微软雅黑", 10, "bold"),
            padx=10,
            pady=10
        )
        news_frame.pack(fill="both", padx=20, pady=10, expand=True)
        
        news_text = tk.Text(
            news_frame,
            font=("微软雅黑", 9),
            wrap="word",
            height=8
        )
        news_text.pack(fill="both", expand=True)
        news_text.insert("1.0", """🎉 欢迎来到P1时光WoW私服！

✨ 服务器特色：
• 机器人系统（单人也能玩！）
• 幻化系统
• 时光副本
• 稳定运行

📝 最新更新：
• 2026-03-22: 服务器已上线
• 机器人系统已优化
• 新增自定义物品

⚠️ 注意事项：
• 请使用3.3.5a客户端
• 首次登录需要注册账号
• 有问题请联系管理员

祝游戏愉快！""")
        news_text.config(state="disabled")
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # 左侧按钮
        left_btn_frame = tk.Frame(button_frame)
        left_btn_frame.pack(side="left", fill="x", expand=True)
        
        register_btn = tk.Button(
            left_btn_frame,
            text="📝 注册账号",
            font=("微软雅黑", 10),
            width=12,
            command=self.open_register
        )
        register_btn.pack(side="left", padx=5)
        
        website_btn = tk.Button(
            left_btn_frame,
            text="🌐 官网",
            font=("微软雅黑", 10),
            width=10,
            command=self.open_website
        )
        website_btn.pack(side="left", padx=5)
        
        # 右侧按钮
        right_btn_frame = tk.Frame(button_frame)
        right_btn_frame.pack(side="right")
        
        settings_btn = tk.Button(
            right_btn_frame,
            text="⚙️ 设置",
            font=("微软雅黑", 10),
            width=10,
            command=self.open_settings
        )
        settings_btn.pack(side="left", padx=5)
        
        # 底部启动按钮
        launch_frame = tk.Frame(self.root, bg="#1a1a2e", height=80)
        launch_frame.pack(fill="x", side="bottom")
        launch_frame.pack_propagate(False)
        
        self.launch_btn = tk.Button(
            launch_frame,
            text="🎮 启动游戏",
            font=("微软雅黑", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            command=self.launch_game
        )
        self.launch_btn.pack(pady=20, ipadx=50, ipady=5)
        
        # 底部版权信息
        footer_label = tk.Label(
            launch_frame,
            text="© 2026 P1时光WoW | Powered by AzerothCore",
            font=("微软雅黑", 8),
            fg="#808080",
            bg="#1a1a2e"
        )
        footer_label.pack(side="bottom", pady=5)
    
    def detect_client_path(self):
        """自动检测WoW客户端路径"""
        possible_paths = [
            "C:/Program Files (x86)/World of Warcraft",
            "C:/Program Files/World of Warcraft",
            "D:/World of Warcraft",
            "E:/World of Warcraft",
            "C:/Games/World of Warcraft",
            "D:/Games/World of Warcraft",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                wow_exe = os.path.join(path, "Wow.exe")
                if os.path.exists(wow_exe):
                    self.path_entry.delete(0, tk.END)
                    self.path_entry.insert(0, path)
                    self.config["client_path"] = path
                    self.save_config()
                    return
        
        # 如果没找到，检查配置文件
        if "client_path" in self.config:
            if os.path.exists(self.config["client_path"]):
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, self.config["client_path"])
    
    def browse_client(self):
        """浏览选择WoW客户端路径"""
        folder = filedialog.askdirectory(title="选择WoW客户端目录")
        if folder:
            wow_exe = os.path.join(folder, "Wow.exe")
            if os.path.exists(wow_exe):
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, folder)
                self.config["client_path"] = folder
                self.save_config()
            else:
                messagebox.showwarning("警告", "未找到Wow.exe，请确认是否为WoW客户端目录")
    
    def update_realmlist(self, client_path):
        """更新realmlist.wtf文件"""
        realmlist_path = os.path.join(client_path, "realmlist.wtf")
        
        try:
            # 备份原文件
            if os.path.exists(realmlist_path):
                backup_path = realmlist_path + ".backup"
                if not os.path.exists(backup_path):
                    shutil.copy(realmlist_path, backup_path)
            
            # 写入新配置
            with open(realmlist_path, 'w', encoding='utf-8') as f:
                f.write(self.config["realmlist"])
            
            return True
        except Exception as e:
            messagebox.showerror("错误", f"更新realmlist失败：\n{e}")
            return False
    
    def launch_game(self):
        """启动游戏"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("警告", "请先设置WoW客户端路径")
            return
        
        wow_exe = os.path.join(client_path, "Wow.exe")
        
        if not os.path.exists(wow_exe):
            messagebox.showerror("错误", f"未找到Wow.exe：\n{wow_exe}")
            return
        
        # 更新realmlist
        if not self.update_realmlist(client_path):
            return
        
        # 启动游戏
        try:
            os.chdir(client_path)
            subprocess.Popen([wow_exe])
            
            # 记录启动日志
            log_file = "launcher.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: 游戏启动成功\n")
            
            messagebox.showinfo("成功", "游戏启动成功！\n\n享受P1时光WoW吧！")
            
            # 可选：关闭登录器
            # self.root.quit()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败：\n{e}")
    
    def open_register(self):
        """打开注册页面"""
        import webbrowser
        if self.config["register_url"]:
            webbrowser.open(self.config["register_url"])
        else:
            messagebox.showinfo("提示", "请联系管理员获取注册地址")
    
    def open_website(self):
        """打开官网"""
        import webbrowser
        if self.config["website_url"]:
            webbrowser.open(self.config["website_url"])
        else:
            messagebox.showinfo("提示", "暂无官网")
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("登录器设置")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # 服务器名称
        tk.Label(settings_window, text="服务器名称:").pack(pady=5)
        name_entry = tk.Entry(settings_window, width=40)
        name_entry.insert(0, self.config["server_name"])
        name_entry.pack(pady=5)
        
        # 服务器IP
        tk.Label(settings_window, text="服务器IP:").pack(pady=5)
        ip_entry = tk.Entry(settings_window, width=40)
        ip_entry.insert(0, self.config["server_ip"])
        ip_entry.pack(pady=5)
        
        # 注册URL
        tk.Label(settings_window, text="注册网址:").pack(pady=5)
        reg_entry = tk.Entry(settings_window, width=40)
        reg_entry.insert(0, self.config["register_url"])
        reg_entry.pack(pady=5)
        
        # 官网URL
        tk.Label(settings_window, text="官网网址:").pack(pady=5)
        web_entry = tk.Entry(settings_window, width=40)
        web_entry.insert(0, self.config["website_url"])
        web_entry.pack(pady=5)
        
        def save_settings():
            self.config["server_name"] = name_entry.get()
            self.config["server_ip"] = ip_entry.get()
            self.config["realmlist"] = f"set realmlist {ip_entry.get()}"
            self.config["register_url"] = reg_entry.get()
            self.config["website_url"] = web_entry.get()
            self.save_config()
            messagebox.showinfo("成功", "设置已保存！")
            settings_window.destroy()
        
        # 保存按钮
        tk.Button(
            settings_window,
            text="保存",
            command=save_settings
        ).pack(pady=20)

def main():
    root = tk.Tk()
    
    # 设置主题颜色
    style = ttk.Style()
    style.theme_use('clam')
    
    app = WoWLauncher(root)
    
    # 居中窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
