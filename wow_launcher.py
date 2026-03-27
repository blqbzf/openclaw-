#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺兰时光魔兽登录器 v3.6 - 极简稳定版
移除所有可能导致启动失败的功能
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import json

class SimpleWoWLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诺兰时光魔兽登录器 v3.6")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建界面
        self.create_widgets()
    
    def load_config(self):
        """加载配置文件"""
        config_file = os.path.join(os.path.dirname(__file__), "launcher_config.json")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # 默认配置
            return {
                "server_name": "诺兰时光魔兽",
                "server_ip": "1.14.59.54",
                "realmlist": "set realmlist 1.14.59.54",
                "client_path": "",
                "register_url": "http://1.14.59.54:5000",
                "launcher_version": "3.6.0"
            }
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.root,
            text=f"🎮 {self.config.get('server_name', '诺兰时光魔兽')}",
            font=("微软雅黑", 32, "bold"),
            fg="#FFD700",
            bg="#1a1a2e"
        )
        title_label.pack(pady=50)
        
        # 服务器信息
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(pady=20)
        
        tk.Label(
            info_frame,
            text=f"服务器: {self.config.get('server_ip', '1.14.59.54')}",
            font=("微软雅黑", 14),
            fg="#FFD700",
            bg="#1a1a2e"
        ).pack()
        
        tk.Label(
            info_frame,
            text=f"版本: {self.config.get('game_version', '3.3.5a')}",
            font=("微软雅黑", 12),
            fg="#999",
            bg="#1a1a2e"
        ).pack()
        
        # 客户端路径
        path_frame = tk.Frame(self.root, bg="#1a1a2e")
        path_frame.pack(pady=30)
        
        tk.Label(
            path_frame,
            text="客户端路径:",
            font=("微软雅黑", 12),
            fg="#FFD700",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=5)
        
        self.path_entry = tk.Entry(
            path_frame,
            width=50,
            font=("微软雅黑", 10),
            bg="#0a0a14",
            fg="#E0E0E0",
            insertbackground="#FFD700"
        )
        self.path_entry.pack(side=tk.LEFT, padx=5)
        self.path_entry.insert(0, self.config.get("client_path", ""))
        
        browse_btn = tk.Button(
            path_frame,
            text="浏览",
            font=("微软雅黑", 10),
            bg="#8B4513",
            fg="#FFD700",
            command=self.browse_path
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=30)
        
        # 开始游戏按钮
        start_btn = tk.Button(
            button_frame,
            text="🎮 开始游戏",
            font=("微软雅黑", 14, "bold"),
            bg="#8B4513",
            fg="#FFD700",
            width=15,
            height=2,
            command=self.start_game
        )
        start_btn.pack(pady=10)
        
        # 注册账号按钮
        register_btn = tk.Button(
            button_frame,
            text="📝 注册账号",
            font=("微软雅黑", 12),
            bg="#4a3a6a",
            fg="#FFD700",
            width=15,
            command=self.open_register
        )
        register_btn.pack(pady=5)
        
        # 状态标签
        self.status_label = tk.Label(
            self.root,
            text="就绪",
            font=("微软雅黑", 10),
            fg="#999",
            bg="#1a1a2e"
        )
        self.status_label.pack(side=tk.BOTTOM, pady=20)
    
    def browse_path(self):
        """浏览选择客户端路径"""
        path = filedialog.askdirectory(title="选择WoW客户端目录")
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
            self.config["client_path"] = path
            self.save_config()
    
    def save_config(self):
        """保存配置"""
        config_file = os.path.join(os.path.dirname(__file__), "launcher_config.json")
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def start_game(self):
        """启动游戏"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("提示", "请先选择WoW客户端路径")
            return
        
        wow_exe = os.path.join(client_path, "Wow.exe")
        
        if not os.path.exists(wow_exe):
            messagebox.showerror("错误", f"未找到Wow.exe:\n{wow_exe}")
            return
        
        # 更新 realmlist
        realmlist_file = os.path.join(client_path, "realmlist.wtf")
        try:
            with open(realmlist_file, 'w', encoding='utf-8') as f:
                f.write(self.config.get("realmlist", "set realmlist 1.14.59.54"))
        except Exception as e:
            messagebox.showwarning("警告", f"更新realmlist失败: {e}")
        
        # 启动游戏
        try:
            os.chdir(client_path)
            subprocess.Popen([wow_exe])
            self.status_label.config(text="游戏已启动")
            messagebox.showinfo("成功", "游戏启动成功！\n\n请等待游戏加载...")
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败:\n{e}")
    
    def open_register(self):
        """打开注册页面"""
        import webbrowser
        url = self.config.get("register_url", "http://1.14.59.54:5000")
        webbrowser.open(url)
    
    def run(self):
        """运行登录器"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimpleWoWLauncher()
        app.run()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("启动错误", f"登录器启动失败:\n{str(e)}")

