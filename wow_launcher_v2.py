#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1时光WoW私服登录器 v2.0
设计理念：参考优秀WoW私服登录器，提供专业美观的UI体验
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import json
from pathlib import Path
import shutil
from datetime import datetime

class WoWLauncherPro:
    def __init__(self, root):
        self.root = root
        self.root.title("P1时光WoW - 登录器")
        
        # 窗口设置
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0e1a")
        
        # 移除标题栏边框
        self.root.overrideredirect(False)
        
        # 服务器配置
        self.config = self.load_config()
        
        # 创建主界面
        self.create_ui()
        
        # 自动检测客户端
        self.detect_client()
        
    def load_config(self):
        """加载配置"""
        config_file = "launcher_config.json"
        default_config = {
            "server_name": "P1时光WoW",
            "server_ip": "1.14.59.54",
            "register_url": "http://1.14.59.54:5000",
            "website_url": "",
            "client_path": "",
            "version": "3.3.5a"
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass
        
        return default_config
    
    def save_config(self):
        """保存配置"""
        with open("launcher_config.json", 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def create_ui(self):
        """创建专业UI"""
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#0a0e1a")
        main_frame.pack(fill="both", expand=True)
        
        # ==================== 左侧面板（主内容） ====================
        left_panel = tk.Frame(main_frame, bg="#0a0e1a", width=600)
        left_panel.pack(side="left", fill="both", expand=True)
        left_panel.pack_propagate(False)
        
        # 顶部Logo区域 - 使用渐变背景效果
        header_frame = tk.Frame(left_panel, bg="#1a2332", height=150)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # 服务器Logo/标题
        title_frame = tk.Frame(header_frame, bg="#1a2332")
        title_frame.pack(expand=True)
        
        # 主标题
        tk.Label(
            title_frame,
            text="P1 时光WoW",
            font=("华文行楷", 42, "bold"),
            fg="#ffd700",
            bg="#1a2332"
        ).pack()
        
        # 副标题
        tk.Label(
            title_frame,
            text=" Wrath of the Lich King 3.3.5a",
            font=("Arial", 12, "italic"),
            fg="#8b9dc3",
            bg="#1a2332"
        ).pack(pady=(5,0))
        
        # 分隔线
        separator = tk.Frame(left_panel, bg="#3a7bd5", height=2)
        separator.pack(fill="x")
        
        # 新闻/公告区域
        news_container = tk.Frame(left_panel, bg="#0a0e1a")
        news_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # 新闻标题
        news_header = tk.Frame(news_container, bg="#0a0e1a")
        news_header.pack(fill="x")
        
        tk.Label(
            news_header,
            text="📰 服务器公告",
            font=("微软雅黑", 14, "bold"),
            fg="#ffd700",
            bg="#0a0e1a"
        ).pack(side="left")
        
        # 新闻内容（带滚动条）
        news_frame = tk.Frame(news_container, bg="#1a2332", bd=0)
        news_frame.pack(fill="both", expand=True, pady=(10,0))
        
        # 添加内边距
        news_inner = tk.Frame(news_frame, bg="#1a2332")
        news_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        # 新闻文本
        news_content = tk.Text(
            news_inner,
            font=("微软雅黑", 10),
            bg="#1a2332",
            fg="#d0d0d0",
            wrap="word",
            bd=0,
            highlightthickness=0,
            cursor="arrow"
        )
        news_content.pack(fill="both", expand=True)
        
        news_content.insert("1.0", """🎮 欢迎来到P1时光WoW！

━━━━━━━━━━━━━━━━━━━━━━━━━

✨ 服务器特色

• 🤖 智能机器人系统 - 单人也能体验团队副本
• 👔 幻化系统 - 自定义角色外观
• ⏳ 时光漫游 - 重温经典副本
• 🎁 自定义物品 - 独特装备等你获取

━━━━━━━━━━━━━━━━━━━━━━━━━

📅 最新动态

• 2026-03-22: 服务器正式上线
• 机器人AI系统全面优化
• 新增15件自定义传说装备
• 修复若干已知问题

━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 温馨提示

• 请使用3.3.5a (12340) 客户端
• 首次游戏请先注册账号
• 遇到问题请联系在线GM

祝你在艾泽拉斯冒险愉快！ 🗡️""")
        news_content.config(state="disabled")
        
        # 底部启动按钮
        launch_frame = tk.Frame(left_panel, bg="#0a0e1a", height=100)
        launch_frame.pack(fill="x", padx=25, pady=20)
        launch_frame.pack_propagate(False)
        
        # 启动按钮（大号醒目）
        self.launch_btn = tk.Button(
            launch_frame,
            text="⚔️ 进  入  游  戏 ⚔️",
            font=("微软雅黑", 18, "bold"),
            bg="#3a7bd5",
            fg="white",
            activebackground="#2d6bc4",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.launch_game
        )
        self.launch_btn.pack(fill="both", expand=True)
        
        # 鼠标悬停效果
        self.launch_btn.bind("<Enter>", lambda e: self.launch_btn.config(bg="#4a8be5"))
        self.launch_btn.bind("<Leave>", lambda e: self.launch_btn.config(bg="#3a7bd5"))
        
        # ==================== 右侧面板（信息&设置） ====================
        right_panel = tk.Frame(main_frame, bg="#141922", width=300)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # 右侧顶部 - 服务器状态
        status_section = tk.Frame(right_panel, bg="#141922")
        status_section.pack(fill="x", padx=20, pady=20)
        
        tk.Label(
            status_section,
            text="服务器状态",
            font=("微软雅黑", 12, "bold"),
            fg="#ffd700",
            bg="#141922"
        ).pack(anchor="w", pady=(0,10))
        
        # 状态信息框
        status_box = tk.Frame(status_section, bg="#1a2332", bd=0)
        status_box.pack(fill="x")
        
        status_inner = tk.Frame(status_box, bg="#1a2332")
        status_inner.pack(fill="x", padx=15, pady=15)
        
        # 在线状态
        status_row1 = tk.Frame(status_inner, bg="#1a2332")
        status_row1.pack(fill="x", pady=5)
        
        tk.Label(
            status_row1,
            text="状态:",
            font=("微软雅黑", 10),
            fg="#8b9dc3",
            bg="#1a2332"
        ).pack(side="left")
        
        tk.Label(
            status_row1,
            text="  🟢 在线",
            font=("微软雅黑", 10, "bold"),
            fg="#4caf50",
            bg="#1a2332"
        ).pack(side="left")
        
        # 在线人数
        status_row2 = tk.Frame(status_inner, bg="#1a2332")
        status_row2.pack(fill="x", pady=5)
        
        tk.Label(
            status_row2,
            text="在线:",
            font=("微软雅黑", 10),
            fg="#8b9dc3",
            bg="#1a2332"
        ).pack(side="left")
        
        tk.Label(
            status_row2,
            text="  127 玩家",
            font=("微软雅黑", 10),
            fg="#ffd700",
            bg="#1a2332"
        ).pack(side="left")
        
        # 服务器IP
        status_row3 = tk.Frame(status_inner, bg="#1a2332")
        status_row3.pack(fill="x", pady=5)
        
        tk.Label(
            status_row3,
            text="IP:",
            font=("微软雅黑", 10),
            fg="#8b9dc3",
            bg="#1a2332"
        ).pack(side="left")
        
        tk.Label(
            status_row3,
            text=f"  {self.config['server_ip']}",
            font=("微软雅黑", 10),
            fg="#3a7bd5",
            bg="#1a2332"
        ).pack(side="left")
        
        # 客户端设置区域
        settings_section = tk.Frame(right_panel, bg="#141922")
        settings_section.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            settings_section,
            text="客户端设置",
            font=("微软雅黑", 12, "bold"),
            fg="#ffd700",
            bg="#141922"
        ).pack(anchor="w", pady=(0,10))
        
        # 路径输入框
        path_frame = tk.Frame(settings_section, bg="#1a2332")
        path_frame.pack(fill="x")
        
        self.path_entry = tk.Entry(
            path_frame,
            font=("微软雅黑", 9),
            bg="#1a2332",
            fg="#d0d0d0",
            insertbackground="#d0d0d0",
            bd=0,
            highlightthickness=1,
            highlightcolor="#3a7bd5",
            highlightbackground="#2d3e50"
        )
        self.path_entry.pack(fill="x", padx=10, pady=10)
        
        # 浏览按钮
        browse_btn = tk.Button(
            path_frame,
            text="浏览...",
            font=("微软雅黑", 9),
            bg="#3a7bd5",
            fg="white",
            activebackground="#2d6bc4",
            bd=0,
            cursor="hand2",
            command=self.browse_client
        )
        browse_btn.pack(padx=10, pady=(0,10))
        
        # 功能按钮区域
        buttons_section = tk.Frame(right_panel, bg="#141922")
        buttons_section.pack(fill="x", padx=20, pady=20)
        
        # 注册按钮
        register_btn = tk.Button(
            buttons_section,
            text="📝 注册账号",
            font=("微软雅黑", 11),
            bg="#3a7bd5",
            fg="white",
            activebackground="#2d6bc4",
            bd=0,
            cursor="hand2",
            width=20,
            height=2,
            command=self.open_register
        )
        register_btn.pack(fill="x", pady=5)
        
        # 官网按钮
        website_btn = tk.Button(
            buttons_section,
            text="🌐 访问官网",
            font=("微软雅黑", 11),
            bg="#1a2332",
            fg="#d0d0d0",
            activebackground="#2d3e50",
            bd=1,
            relief="solid",
            cursor="hand2",
            width=20,
            height=2,
            command=self.open_website
        )
        website_btn.pack(fill="x", pady=5)
        
        # 清除缓存按钮
        cache_btn = tk.Button(
            buttons_section,
            text="🗑️ 清除缓存",
            font=("微软雅黑", 11),
            bg="#1a2332",
            fg="#d0d0d0",
            activebackground="#2d3e50",
            bd=1,
            relief="solid",
            cursor="hand2",
            width=20,
            height=2,
            command=self.clear_cache
        )
        cache_btn.pack(fill="x", pady=5)
        
        # 底部版权
        footer_frame = tk.Frame(right_panel, bg="#141922")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        
        tk.Label(
            footer_frame,
            text="© 2026 P1时光WoW",
            font=("Arial", 8),
            fg="#5a6a7a",
            bg="#141922"
        ).pack()
        
        tk.Label(
            footer_frame,
            text="Powered by AzerothCore",
            font=("Arial", 8),
            fg="#5a6a7a",
            bg="#141922"
        ).pack()
    
    def detect_client(self):
        """自动检测客户端"""
        if self.config.get("client_path"):
            self.path_entry.insert(0, self.config["client_path"])
            return
        
        possible_paths = [
            "C:/Program Files (x86)/World of Warcraft",
            "C:/Program Files/World of Warcraft",
            "D:/World of Warcraft",
            "D:/Games/World of Warcraft",
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.path.exists(os.path.join(path, "Wow.exe")):
                self.path_entry.insert(0, path)
                self.config["client_path"] = path
                self.save_config()
                return
    
    def browse_client(self):
        """浏览选择客户端"""
        folder = filedialog.askdirectory(title="选择WoW 3.3.5a客户端目录")
        if folder:
            if os.path.exists(os.path.join(folder, "Wow.exe")):
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, folder)
                self.config["client_path"] = folder
                self.save_config()
            else:
                messagebox.showwarning("警告", "未找到Wow.exe文件")
    
    def update_realmlist(self, client_path):
        """更新realmlist"""
        realmlist_path = os.path.join(client_path, "realmlist.wtf")
        
        try:
            # 备份
            if os.path.exists(realmlist_path):
                backup = realmlist_path + ".backup"
                if not os.path.exists(backup):
                    shutil.copy(realmlist_path, backup)
            
            # 写入
            with open(realmlist_path, 'w', encoding='utf-8') as f:
                f.write(f"set realmlist {self.config['server_ip']}")
            
            return True
        except Exception as e:
            messagebox.showerror("错误", f"更新realmlist失败：\n{e}")
            return False
    
    def launch_game(self):
        """启动游戏"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("提示", "请先设置WoW客户端路径")
            return
        
        wow_exe = os.path.join(client_path, "Wow.exe")
        
        if not os.path.exists(wow_exe):
            messagebox.showerror("错误", f"未找到Wow.exe：\n{wow_exe}")
            return
        
        # 更新realmlist
        if not self.update_realmlist(client_path):
            return
        
        # 启动
        try:
            os.chdir(client_path)
            subprocess.Popen([wow_exe])
            
            # 记录日志
            with open("launcher.log", 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: 游戏启动成功\n")
            
            messagebox.showinfo("成功", "游戏启动成功！\n\n愿圣光与你同在！ ⚔️")
            
        except Exception as e:
            messagebox.showerror("错误", f"启动失败：\n{e}")
    
    def open_register(self):
        """打开注册页"""
        import webbrowser
        if self.config.get("register_url"):
            webbrowser.open(self.config["register_url"])
        else:
            messagebox.showinfo("提示", "请联系管理员获取注册地址")
    
    def open_website(self):
        """打开官网"""
        import webbrowser
        if self.config.get("website_url"):
            webbrowser.open(self.config["website_url"])
        else:
            messagebox.showinfo("提示", "暂无官网地址")
    
    def clear_cache(self):
        """清除缓存"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("提示", "请先设置客户端路径")
            return
        
        # 删除缓存文件夹
        cache_folders = ["Cache", "WDB"]
        deleted = []
        
        for folder in cache_folders:
            folder_path = os.path.join(client_path, folder)
            if os.path.exists(folder_path):
                try:
                    shutil.rmtree(folder_path)
                    deleted.append(folder)
                except:
                    pass
        
        if deleted:
            messagebox.showinfo("成功", f"已清除缓存：\n{', '.join(deleted)}")
        else:
            messagebox.showinfo("提示", "未找到缓存文件")


def main():
    root = tk.Tk()
    
    # 设置DPI感知（Windows）
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = WoWLauncherPro(root)
    
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
