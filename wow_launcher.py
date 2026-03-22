#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1时光WoW私服登录器 v3.0
设计理念：魔兽风格异形窗口 + 完善的反作弊系统
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import json
import shutil
import psutil
import hashlib
import threading
import time
from datetime import datetime
from pathlib import Path


class WoWLauncherV3:
    def __init__(self, root):
        self.root = root
        self.root.title("P1时光WoW - 登录器")
        
        # 窗口设置 - 异形窗口
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # 无边框窗口
        
        # 服务器配置
        self.config = self.load_config()
        
        # 反作弊监控相关
        self.monitoring_active = False
        self.game_process = None
        self.monitor_thread = None
        
        # 创建魔兽风格UI
        self.create_wow_style_ui()
        
        # 自动检测客户端
        self.auto_detect_client()
        
        # 绑定窗口拖动
        self.bind_window_drag()
        
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
    
    def bind_window_drag(self):
        """绑定窗口拖动事件"""
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
    
    def start_move(self, event):
        """开始移动"""
        self.x = event.x
        self.y = event.y
    
    def do_move(self, event):
        """移动窗口"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def create_wow_style_ui(self):
        """创建魔兽风格UI"""
        
        # 主画布 - 用于绘制魔兽风格边框
        self.canvas = tk.Canvas(
            self.root,
            width=800,
            height=600,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 绘制魔兽风格边框
        self.draw_wow_frame()
        
        # 创建内容区域
        self.create_content()
    
    def draw_wow_frame(self):
        """绘制魔兽风格边框"""
        
        # 外边框 - 金色装饰线
        border_color = "#c9a030"
        
        # 绘制装饰性边框（8个角的花纹）
        corner_size = 60
        
        # 四个角的装饰
        corners = [
            (10, 10, corner_size, corner_size),  # 左上
            (730, 10, 790, corner_size),  # 右上
            (10, 540, corner_size, 590),  # 左下
            (730, 540, 790, 590),  # 右下
        ]
        
        for x1, y1, x2, y2 in corners:
            # 外框
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=border_color,
                width=2,
                fill=""
            )
            # 内部装饰
            self.canvas.create_rectangle(
                x1+5, y1+5, x2-5, y2-5,
                outline=border_color,
                width=1,
                fill=""
            )
        
        # 上下边框装饰线
        self.canvas.create_line(70, 15, 730, 15, fill=border_color, width=2)
        self.canvas.create_line(70, 585, 730, 585, fill=border_color, width=2)
        
        # 左右边框装饰线
        self.canvas.create_line(15, 70, 15, 530, fill=border_color, width=2)
        self.canvas.create_line(785, 70, 785, 530, fill=border_color, width=2)
        
        # 顶部标题栏背景
        self.canvas.create_rectangle(
            20, 20, 780, 80,
            fill="#2a2a2a",
            outline=border_color,
            width=1
        )
        
        # 标题文字
        self.canvas.create_text(
            400, 50,
            text="⚔️ P1 时光WoW ⚔️",
            font=("华文行楷", 28, "bold"),
            fill="#ffd700"
        )
        
        # 副标题
        self.canvas.create_text(
            400, 70,
            text="Wrath of the Lich King 3.3.5a",
            font=("Arial", 10, "italic"),
            fill="#8b8b8b"
        )
        
        # 关闭按钮（右上角X）
        close_btn = tk.Button(
            self.root,
            text="✕",
            font=("Arial", 12, "bold"),
            bg="#2a2a2a",
            fg="#c9a030",
            activebackground="#ff4444",
            activeforeground="white",
            bd=0,
            width=3,
            height=1,
            command=self.root.quit
        )
        close_btn.place(x=745, y=25)
        
        # 最小化按钮
        min_btn = tk.Button(
            self.root,
            text="─",
            font=("Arial", 12, "bold"),
            bg="#2a2a2a",
            fg="#c9a030",
            activebackground="#555555",
            activeforeground="white",
            bd=0,
            width=3,
            height=1,
            command=self.minimize_window
        )
        min_btn.place(x=710, y=25)
    
    def minimize_window(self):
        """最小化窗口"""
        self.root.iconify()
    
    def create_content(self):
        """创建内容区域"""
        
        # 左侧面板 - 公告区
        left_frame = tk.Frame(self.root, bg="#1a1a1a")
        left_frame.place(x=30, y=100, width=500, height=380)
        
        # 公告标题
        tk.Label(
            left_frame,
            text="📜 服务器公告",
            font=("微软雅黑", 14, "bold"),
            fg="#ffd700",
            bg="#1a1a1a"
        ).pack(anchor="w", pady=(0,10))
        
        # 公告内容
        news_text = tk.Text(
            left_frame,
            font=("微软雅黑", 10),
            bg="#2a2a2a",
            fg="#d0d0d0",
            wrap="word",
            bd=0,
            highlightthickness=1,
            highlightcolor="#c9a030",
            highlightbackground="#3a3a3a"
        )
        news_text.pack(fill="both", expand=True)
        
        news_content = """🎮 欢迎来到P1时光WoW！

━━━━━━━━━━━━━━━━━━━━━━━━

✨ 服务器特色

• 🤖 智能机器人系统 - 单人也能体验团队副本
• 👔 幻化系统 - 自定义角色外观
• ⏳ 时光漫游 - 重温经典副本
• 🎁 自定义物品 - 独特装备等你获取

━━━━━━━━━━━━━━━━━━━━━━━━

📅 最新动态

• 2026-03-22: 服务器正式上线
• 机器人AI系统全面优化
• 新增15件自定义传说装备

━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 反作弊提示

本服已启用严格的反作弊系统：
• 实时检测非法脚本
• 自动扫描外挂程序
• 违规将永久封禁

━━━━━━━━━━━━━━━━━━━━━━━━

愿圣光与你同在！ 🗡️"""
        
        news_text.insert("1.0", news_content)
        news_text.config(state="disabled")
        
        # 右侧面板 - 功能区
        right_frame = tk.Frame(self.root, bg="#1a1a1a")
        right_frame.place(x=550, y=100, width=220, height=380)
        
        # 服务器状态
        status_frame = tk.LabelFrame(
            right_frame,
            text=" 服务器状态 ",
            font=("微软雅黑", 10, "bold"),
            fg="#ffd700",
            bg="#2a2a2a",
            bd=2,
            relief="solid"
        )
        status_frame.pack(fill="x", pady=(0,10))
        
        # 状态信息
        tk.Label(
            status_frame,
            text="状态: 🟢 在线",
            font=("微软雅黑", 9),
            fg="#4caf50",
            bg="#2a2a2a"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text="在线: 127 玩家",
            font=("微软雅黑", 9),
            fg="#ffd700",
            bg="#2a2a2a"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text=f"IP: {self.config['server_ip']}",
            font=("微软雅黑", 9),
            fg="#64b5f6",
            bg="#2a2a2a"
        ).pack(anchor="w", padx=10, pady=5)
        
        # 客户端设置
        settings_frame = tk.LabelFrame(
            right_frame,
            text=" 客户端设置 ",
            font=("微软雅黑", 10, "bold"),
            fg="#ffd700",
            bg="#2a2a2a",
            bd=2,
            relief="solid"
        )
        settings_frame.pack(fill="x", pady=(0,10))
        
        # 路径输入
        self.path_entry = tk.Entry(
            settings_frame,
            font=("微软雅黑", 9),
            bg="#1a1a1a",
            fg="#d0d0d0",
            insertbackground="#d0d0d0",
            bd=0,
            highlightthickness=1,
            highlightcolor="#c9a030",
            highlightbackground="#3a3a3a"
        )
        self.path_entry.pack(fill="x", padx=10, pady=5)
        
        # 按钮框架
        btn_frame = tk.Frame(settings_frame, bg="#2a2a2a")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        # 自动搜索按钮
        auto_btn = tk.Button(
            btn_frame,
            text="🔍 自动搜索",
            font=("微软雅黑", 9),
            bg="#3a7bd5",
            fg="white",
            activebackground="#2d6bc4",
            bd=0,
            cursor="hand2",
            command=self.auto_detect_client
        )
        auto_btn.pack(side="left", padx=(0,5))
        
        # 浏览按钮
        browse_btn = tk.Button(
            btn_frame,
            text="📁 浏览",
            font=("微软雅黑", 9),
            bg="#3a7bd5",
            fg="white",
            activebackground="#2d6bc4",
            bd=0,
            cursor="hand2",
            command=self.browse_client
        )
        browse_btn.pack(side="left")
        
        # 功能按钮
        button_commands = [
            ("📝 注册账号", self.open_register),
            ("🌐 访问官网", self.open_website),
            ("🛡️ 安全检测", self.run_security_check),
            ("🗑️ 清除缓存", self.clear_cache),
        ]
        
        for text, command in button_commands:
            btn = tk.Button(
                right_frame,
                text=text,
                font=("微软雅黑", 10),
                bg="#2a2a2a",
                fg="#ffd700",
                activebackground="#3a3a3a",
                activeforeground="#ffd700",
                bd=1,
                relief="solid",
                cursor="hand2",
                command=command
            )
            btn.pack(fill="x", pady=5)
        
        # 底部启动按钮区域
        launch_frame = tk.Frame(self.root, bg="#1a1a1a")
        launch_frame.place(x=30, y=500, width=740, height=70)
        
        # 启动按钮（魔兽风格大按钮）
        self.launch_btn = tk.Button(
            launch_frame,
            text="⚔️  进  入  艾  泽  拉  斯  ⚔️",
            font=("华文行楷", 20, "bold"),
            bg="#c9a030",
            fg="#1a1a1a",
            activebackground="#ffd700",
            activeforeground="#1a1a1a",
            bd=0,
            cursor="hand2",
            command=self.launch_game_with_check
        )
        self.launch_btn.pack(fill="both", expand=True, pady=10)
        
        # 悬停效果
        self.launch_btn.bind("<Enter>", lambda e: self.launch_btn.config(bg="#ffd700"))
        self.launch_btn.bind("<Leave>", lambda e: self.launch_btn.config(bg="#c9a030"))
        
        # 底部版权
        self.canvas.create_text(
            400, 575,
            text="© 2026 P1时光WoW | Powered by AzerothCore | 反作弊系统已启用",
            font=("Arial", 8),
            fill="#5a5a5a"
        )
    
    def auto_detect_client(self):
        """自动搜索WoW客户端"""
        possible_paths = [
            # Windows常见路径
            "C:/Program Files (x86)/World of Warcraft",
            "C:/Program Files/World of Warcraft",
            "D:/World of Warcraft",
            "D:/Games/World of Warcraft",
            "E:/World of Warcraft",
            "E:/Games/World of Warcraft",
            # 添加更多可能的路径
            "C:/Games/WoW",
            "D:/Games/WoW",
            "C:/WoW",
            "D:/WoW",
        ]
        
        # 如果有配置的路径，优先检查
        if self.config.get("client_path"):
            if os.path.exists(self.config["client_path"]):
                wow_exe = os.path.join(self.config["client_path"], "Wow.exe")
                if os.path.exists(wow_exe):
                    self.path_entry.delete(0, tk.END)
                    self.path_entry.insert(0, self.config["client_path"])
                    return
        
        # 搜索所有可能路径
        for path in possible_paths:
            if os.path.exists(path):
                wow_exe = os.path.join(path, "Wow.exe")
                if os.path.exists(wow_exe):
                    self.path_entry.delete(0, tk.END)
                    self.path_entry.insert(0, path)
                    self.config["client_path"] = path
                    self.save_config()
                    messagebox.showinfo("成功", f"已自动找到客户端：\n{path}")
                    return
        
        # 搜索所有驱动器
        for drive in ['C:', 'D:', 'E:', 'F:']:
            search_path = os.path.join(drive, "\\")
            if os.path.exists(search_path):
                # 简单搜索（避免耗时太长）
                for root, dirs, files in os.walk(search_path):
                    if "Wow.exe" in files:
                        client_path = root
                        self.path_entry.delete(0, tk.END)
                        self.path_entry.insert(0, client_path)
                        self.config["client_path"] = client_path
                        self.save_config()
                        messagebox.showinfo("成功", f"已自动找到客户端：\n{client_path}")
                        return
                    
                    # 只搜索前3层目录
                    if root.count('\\') > 3:
                        del dirs[:]
        
        messagebox.showwarning("未找到", "未找到WoW客户端，请手动选择")
    
    def browse_client(self):
        """浏览选择客户端"""
        folder = filedialog.askdirectory(title="选择WoW 3.3.5a客户端目录")
        if folder:
            wow_exe = os.path.join(folder, "Wow.exe")
            if os.path.exists(wow_exe):
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, folder)
                self.config["client_path"] = folder
                self.save_config()
            else:
                messagebox.showwarning("警告", "未找到Wow.exe文件")
    
    def check_cheats(self):
        """检测外挂和脚本"""
        cheats_found = []
        
        # 常见WoW外挂进程名
        cheat_processes = [
            "WoWEmuHacker.exe",
            "WoWHack.exe",
            "CheatEngine.exe",
            "WPE PRO.exe",
            "WpeSpy.dll",
            "speedhack.exe",
            "WoWSpeedHack.exe",
            "TeleportHack.exe",
            "FlyHack.exe",
            "wallhack.exe",
            "inject.exe",
            "dllinject.exe",
        ]
        
        # 检测运行中的进程
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                if proc_name.lower() in [c.lower() for c in cheat_processes]:
                    cheats_found.append(f"进程: {proc_name}")
            except:
                continue
        
        # 检测客户端目录中的可疑文件
        client_path = self.path_entry.get().strip()
        if client_path and os.path.exists(client_path):
            suspicious_files = [
                "inject.dll",
                "hack.dll",
                "cheat.dll",
                "speedhack.dll",
                "teleport.dll",
                "flyhack.dll",
                "wpe.dll",
            ]
            
            for root, dirs, files in os.walk(client_path):
                for file in files:
                    if file.lower() in suspicious_files:
                        file_path = os.path.join(root, file)
                        cheats_found.append(f"文件: {file_path}")
        
        return cheats_found
    
    def check_scripts(self):
        """检测非法脚本"""
        scripts_found = []
        
        client_path = self.path_entry.get().strip()
        if not client_path or not os.path.exists(client_path):
            return scripts_found
        
        # 检测Interface/AddOns目录
        addons_path = os.path.join(client_path, "Interface", "AddOns")
        if os.path.exists(addons_path):
            # 允许的插件列表（白名单）
            allowed_addons = [
                "blizzard_",
                "dbm-",
                "bigwigs",
                "omen",
                "recount",
                "skada",
                "atlasloot",
                "questie",
                "leatrix",
            ]
            
            for addon in os.listdir(addons_path):
                addon_path = os.path.join(addons_path, addon)
                if os.path.isdir(addon_path):
                    # 检查是否在白名单中
                    is_allowed = any(
                        addon.lower().startswith(allowed.lower())
                        for allowed in allowed_addons
                    )
                    
                    if not is_allowed:
                        # 检查可疑的Lua文件
                        for root, dirs, files in os.walk(addon_path):
                            for file in files:
                                if file.endswith('.lua'):
                                    file_path = os.path.join(root, file)
                                    try:
                                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                            content = f.read().lower()
                                            
                                            # 检测可疑关键词
                                            suspicious_keywords = [
                                                'speedhack',
                                                'teleporthack',
                                                'flyhack',
                                                'wallhack',
                                                'injection',
                                                'memory edit',
                                                'lua unlock',
                                            ]
                                            
                                            for keyword in suspicious_keywords:
                                                if keyword in content:
                                                    scripts_found.append(
                                                        f"可疑插件: {addon} ({keyword})"
                                                    )
                                                    break
                                    except:
                                        pass
        
        return scripts_found
    
    def run_security_check(self):
        """运行安全检测"""
        cheats = self.check_cheats()
        scripts = self.check_scripts()
        
        result = "🛡️ 安全检测结果\n\n"
        
        if cheats or scripts:
            result += "❌ 发现可疑项目：\n\n"
            
            if cheats:
                result += "外挂检测：\n"
                for cheat in cheats:
                    result += f"  • {cheat}\n"
            
            if scripts:
                result += "\n脚本检测：\n"
                for script in scripts:
                    result += f"  • {script}\n"
            
            result += "\n⚠️ 请删除以上文件后再启动游戏！"
            messagebox.showwarning("检测失败", result)
            return False
        else:
            result += "✅ 未检测到外挂或非法脚本\n\n"
            result += "✅ 客户端安全\n"
            result += "✅ 可以正常游戏"
            messagebox.showinfo("检测通过", result)
            return True
    
    def launch_game_with_check(self):
        """启动游戏（带安全检测）"""
        # 先运行安全检测
        cheats = self.check_cheats()
        scripts = self.check_scripts()
        
        if cheats or scripts:
            error_msg = "❌ 检测到外挂或非法脚本！\n\n"
            
            if cheats:
                error_msg += "外挂：\n"
                for cheat in cheats[:3]:  # 只显示前3个
                    error_msg += f"  • {cheat}\n"
            
            if scripts:
                error_msg += "\n非法脚本：\n"
                for script in scripts[:3]:
                    error_msg += f"  • {script}\n"
            
            error_msg += "\n⚠️ 请删除以上文件后再启动游戏！\n"
            error_msg += "违规使用外挂将永久封禁账号！"
            
            messagebox.showerror("安全警告", error_msg)
            return
        
        # 检查客户端路径
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
        
        # 启动游戏
        try:
            os.chdir(client_path)
            self.game_process = subprocess.Popen([wow_exe])
            
            # 记录日志
            with open("launcher.log", 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: 游戏启动成功 (安全检测通过)\n")
            
            # 启动反作弊实时监控
            self.start_anti_cheat_monitor()
            
            messagebox.showinfo(
                "成功",
                "✅ 安全检测通过！\n\n"
                "游戏启动成功！\n"
                "🛡️ 反作弊系统已启动实时监控\n"
                "愿圣光与你同在！ ⚔️"
            )
            
        except Exception as e:
            messagebox.showerror("错误", f"启动失败：\n{e}")
    
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
    
    def start_anti_cheat_monitor(self):
        """启动反作弊实时监控"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # 记录日志
        with open("launcher.log", 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()}: 反作弊实时监控已启动\n")
    
    def monitor_loop(self):
        """监控循环（每5秒检测一次）"""
        while self.monitoring_active:
            try:
                # 检查游戏是否还在运行
                if self.game_process:
                    if self.game_process.poll() is not None:
                        # 游戏已退出
                        self.monitoring_active = False
                        with open("launcher.log", 'a', encoding='utf-8') as f:
                            f.write(f"{datetime.now()}: 游戏已退出，停止监控\n")
                        break
                
                # 检测外挂进程
                cheats = self.check_cheats()
                if cheats:
                    # 发现外挂，立即退出游戏
                    self.stop_game(cheats)
                    break
                
                # 检测非法脚本
                scripts = self.check_scripts()
                if scripts:
                    # 发现脚本，立即退出游戏
                    self.stop_game(scripts)
                    break
                
                # 等待5秒
                time.sleep(5)
                
            except Exception as e:
                # 记录错误
                with open("launcher.log", 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now()}: 监控错误 - {str(e)}\n")
                time.sleep(5)
    
    def stop_game(self, violations):
        """强制退出游戏并记录违规"""
        try:
            # 终止游戏进程
            if self.game_process:
                self.game_process.terminate()
                try:
                    self.game_process.wait(timeout=5)
                except:
                    self.game_process.kill()
            
            # 同时搜索并终止所有Wow.exe进程
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and 'wow.exe' in proc.info['name'].lower():
                        proc.terminate()
                except:
                    pass
            
            # 停止监控
            self.monitoring_active = False
            
            # 记录违规日志
            with open("violation.log", 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"{datetime.now()} - 检测到违规行为\n")
                f.write(f"{'='*60}\n")
                for violation in violations:
                    f.write(f"  • {violation}\n")
                f.write(f"{'='*60}\n\n")
            
            # 显示警告（需要在主线程）
            self.root.after(0, lambda: messagebox.showerror(
                "⚠️ 检测到违规行为",
                f"检测到外挂/脚本运行！\n\n"
                f"违规项目：\n{chr(10).join(violations[:5])}\n\n"
                f"游戏已强制退出！\n"
                f"违规行为已记录到 violation.log\n\n"
                f"使用外挂将导致永久封禁！"
            ))
            
        except Exception as e:
            with open("launcher.log", 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: 强制退出游戏失败 - {str(e)}\n")


def main():
    root = tk.Tk()
    
    # 设置DPI感知（Windows）
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = WoWLauncherV3(root)
    
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
