#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺兰时光魔兽登录器 v3.6.1 - 超级极简版
完全移除所有可能导致卡顿的功能
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import json
import sys

class UltraSimpleWoWLauncher:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("诺兰时光魔兽 v3.6.1")
            self.root.geometry("800x600")
            self.root.configure(bg="#1a1a2e")
            
            # 加载配置
            self.config = self.load_config()
            
            # 创建界面
            self.create_widgets()
            
            print("[INFO] 登录器已启动")
        except Exception as e:
            print(f"[FATAL] 启动失败: {e}")
            sys.exit(1)
    
    def load_config(self):
        """加载配置文件"""
        config = {
            "server_name": "诺兰时光魔兽",
            "server_ip": "1.14.59.54",
            "realmlist": "set realmlist 1.14.59.54",
            "client_path": "",
            "register_url": "http://1.14.59.54:5000",
            "launcher_version": "3.6.1"
        }
        
        try:
            config_file = "launcher_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    config.update(loaded)
                    print(f"[INFO] 配置加载成功")
        except Exception as e:
            print(f"[WARN] 配置加载失败，使用默认配置: {e}")
        
        return config
    
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
            text=f"版本: 3.3.5a (12340)",
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
        try:
            with open("launcher_config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] 保存配置失败: {e}")
    
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
            print(f"[INFO] realmlist 已更新")
        except Exception as e:
            print(f"[WARN] 更新realmlist失败: {e}")
            messagebox.showwarning("警告", f"更新realmlist失败:\n{e}")
        
        # 启动游戏
        try:
            os.chdir(client_path)
            subprocess.Popen([wow_exe])
            self.status_label.config(text="游戏已启动")
            print(f"[INFO] 游戏已启动: {wow_exe}")
            messagebox.showinfo("成功", "游戏启动成功！\n\n请等待游戏加载...")
        except Exception as e:
            print(f"[ERROR] 启动游戏失败: {e}")
            messagebox.showerror("错误", f"启动游戏失败:\n{e}")
    
    def open_register(self):
        """打开注册页面"""
        try:
            import webbrowser
            url = self.config.get("register_url", "http://1.14.59.54:5000")
            webbrowser.open(url)
            print(f"[INFO] 已打开注册页面: {url}")
        except Exception as e:
            print(f"[ERROR] 打开注册页面失败: {e}")
    
    def run(self):
        """运行登录器"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"[FATAL] 运行失败: {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        app = UltraSimpleWoWLauncher()
        app.run()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("启动错误", f"登录器启动失败:\n{str(e)}")
        sys.exit(1)
