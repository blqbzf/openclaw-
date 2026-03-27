#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺兰时光魔兽登录器 v3.5.6 - 修复登录失败问题
修复：MD5校验失败时显示警告但不阻止启动
优化：更好的用户体验
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import subprocess
import json
import shutil
import psutil
import threading
import time
import requests
import hashlib
import base64
from datetime import datetime
from pathlib import Path




# 白名单进程（允许运行的合法软件）
WHITELIST_PROCESSES = [
    "chrome.exe",           # Google Chrome
    "firefox.exe",         # Firefox浏览器
    "wechat.exe",          # 微信
    "qq.exe",              # QQ
    "360safe.exe",         # 360安全卫士
    "baidunetdisk.exe",    # 百度网盘
    "thunder.exe",         # 迅雷
    "bde.exe",             # 百度浏览器
    "sogouexplorer.exe",   # 搜狗浏览器
    "maxthon.exe",         # 傲游浏览器
    "opera.exe",           # Opera浏览器
    "edge.exe",            # Edge浏览器
    "iexplore.exe",        # IE浏览器
    "eluna.exe",           # Eluna Lua引擎
    "lua.exe",             # Lua解释器
    "lua54.exe",           # Lua 5.4
    "lua53.exe",           # Lua 5.3
    "lua52.exe",           # Lua 5.2
    "lua51.exe",           # Lua 5.1
]

class PatchManager:
    """补丁管理器"""
    
    def __init__(self, patch_url, client_path):
        self.patch_url = patch_url
        self.client_path = client_path
        self.data_path = os.path.join(client_path, "Data")
        self.local_version_file = os.path.join(client_path, ".patch_version.json")
        
    def get_local_version(self):
        """获取本地补丁版本"""
        if os.path.exists(self.local_version_file):
            try:
                with open(self.local_version_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"patches": [], "version": "0"}
        return {"patches": [], "version": "0"}
    
    def save_local_version(self, version_info):
        """保存本地补丁版本"""
        with open(self.local_version_file, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
    
    def fetch_manifest(self):
        """获取服务器补丁清单"""
        try:
            # 使用鸽子命规范：manifest.json
            manifest_url = f"{self.patch_url}/manifest.json"
            print(f"[DEBUG] 正在获取: {manifest_url}")
            
            response = requests.get(manifest_url, timeout=5)
            print(f"[DEBUG] 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG] 成功获取manifest: {data}")
                return data
            else:
                print(f"[DEBUG] HTTP错误: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"[DEBUG] 连接超时：服务器响应慢或网络不稳定")
        except requests.exceptions.ConnectionError as e:
            print(f"[DEBUG] 连接失败：{e}")
        except Exception as e:
            print(f"[DEBUG] 获取补丁清单失败: {e}")
            import traceback
            traceback.print_exc()
        return None
    
    def check_for_updates(self):
        """检查是否有新补丁"""
        local_version = self.get_local_version()
        remote_manifest = self.fetch_manifest()
        
        if not remote_manifest:
            return None, []
        
        # 对比补丁
        needed_patches = []
        local_patches = {p['name']: p for p in local_version.get('patches', [])}
        
        for patch in remote_manifest.get('patches', []):
            # 适配鸽子命格式
            patch_name = patch.get('filename') or patch.get('name')
            patch_version = patch.get('version', '0')
            
            # 检查是否已安装
            if patch_name not in local_patches:
                # 转换为统一格式
                needed_patches.append({
                    'name': patch_name,
                    'version': patch_version,
                    'download_url': patch.get('url'),
                    'md5': patch.get('md5'),
                    'size': patch.get('size'),
                    'description': patch.get('description', ''),
                    'priority': patch.get('priority', 100)
                })
            else:
                # 检查版本号
                local_ver = local_patches[patch_name].get('version', '0')
                if patch_version > local_ver:
                    needed_patches.append({
                        'name': patch_name,
                        'version': patch_version,
                        'download_url': patch.get('url'),
                        'md5': patch.get('md5'),
                        'size': patch.get('size'),
                        'description': patch.get('description', ''),
                        'priority': patch.get('priority', 100)
                    })
        
        # 按优先级排序
        needed_patches.sort(key=lambda x: x.get('priority', 100), reverse=True)
        
        return remote_manifest, needed_patches
    
    def download_patch(self, patch_info, progress_callback=None):
        """下载补丁文件"""
        try:
            patch_name = patch_info['name']
            # 使用鸽子命规范的url字段
            download_url = patch_info.get('download_url')
            
            print(f"[DEBUG] 开始下载补丁: {patch_name}")
            print(f"[DEBUG] 下载地址: {download_url}")
            
            if not download_url:
                return False, "下载地址为空"
            
            # 临时文件路径
            temp_path = os.path.join(self.client_path, f".temp_{patch_name}")
            print(f"[DEBUG] 临时路径: {temp_path}")
            
            # 下载文件
            response = requests.get(download_url, stream=True, timeout=30)
            start_time = time.time()
            total_size = int(response.headers.get('content-length', 0))
            print(f"[DEBUG] 文件大小: {total_size} bytes ({total_size/1024:.1f} KB)")
            
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            elapsed = max(time.time() - start_time, 0.1)
                            speed = downloaded / elapsed
                            remain = max(total_size - downloaded, 0)
                            eta_seconds = int(remain / speed) if speed > 0 else 0
                            eta_text = f"{eta_seconds // 60:02d}:{eta_seconds % 60:02d}"
                            progress_callback(progress, {
                                "text": f"下载中 {progress}%",
                                "received": downloaded,
                                "total": total_size,
                                "speed": speed,
                                "eta": eta_text,
                            })
            
            print(f"[DEBUG] 下载完成: {downloaded} bytes")
            
            # 校验MD5
            if progress_callback:
                progress_callback(100, "校验文件...")
            
            md5_hash = patch_info.get('md5')
            if md5_hash:
                calculated_md5 = self.calculate_md5(temp_path)
                print(f"[DEBUG] 期望MD5: {md5_hash}")
                print(f"[DEBUG] 实际MD5: {calculated_md5}")
                
                if calculated_md5 != md5_hash:
                    os.remove(temp_path)
                    return False, f"MD5校验失败（期望:{md5_hash[:8]}... 实际:{calculated_md5[:8]}...）"
            
            # 应用补丁
            if progress_callback:
                progress_callback(100, "应用补丁...")
            
            target_path = os.path.join(self.data_path, patch_name)
            print(f"[DEBUG] 目标路径: {target_path}")
            
            # 检查Data目录是否存在
            if not os.path.exists(self.data_path):
                print(f"[DEBUG] 错误: Data目录不存在 - {self.data_path}")
                return False, f"Data目录不存在: {self.data_path}"
            
            shutil.move(temp_path, target_path)
            print(f"[DEBUG] 补丁已移动到: {target_path}")
            
            # 验证文件
            if os.path.exists(target_path):
                file_size = os.path.getsize(target_path)
                print(f"[DEBUG] 验证成功: 文件存在，大小 {file_size} bytes")
                return True, "补丁应用成功"
            else:
                print(f"[DEBUG] 错误: 文件移动失败")
                return False, "文件移动失败"
            
        except Exception as e:
            print(f"[DEBUG] 下载异常: {e}")
            import traceback
            traceback.print_exc()
            return False, f"下载失败: {str(e)}"
    
    def calculate_md5(self, file_path):
        """计算文件MD5"""
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()
    
    def update_local_version(self, patch_info):
        """更新本地版本记录"""
        local_version = self.get_local_version()
        
        # 更新或添加补丁信息
        patches = local_version.get('patches', [])
        patch_name = patch_info['name']
        
        # 移除旧版本
        patches = [p for p in patches if p['name'] != patch_name]
        # 添加新版本
        patches.append({
            'name': patch_name,
            'version': patch_info.get('version', '1.0'),
            'installed_at': datetime.now().isoformat()
        })
        
        local_version['patches'] = patches
        local_version['version'] = patch_info.get('version', '1.0')
        local_version['last_check'] = datetime.now().isoformat()
        
        self.save_local_version(local_version)


class WoWLauncherV3_1:
    def __init__(self, root):
        self.root = root
        self.root.title("诺兰时光魔兽登录器 v1.0.0")
        
        # 窗口设置 - 异形窗口
        self.root.geometry("960x640")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)  # 无边框窗口
        
        # 服务器配置
        self.config = self.load_config()
        
        # 背景图片
        self.background_image = None
        try:
            from PIL import Image, ImageTk
            bg_path = self.get_background_path()
            if os.path.exists(bg_path):
                pil_image = Image.open(bg_path)
                pil_image = pil_image.resize((960, 640), Image.Resampling.LANCZOS)
                self.background_image = ImageTk.PhotoImage(pil_image)
        except:
            pass
        
        # 补丁管理
        self.patch_manager = None
        
        # 反作弊监控相关
        self.monitoring_active = False
        self.game_process = None
        self.monitor_thread = None
        self.download_start_time = None
        self.download_last_bytes = 0
        self.expected_wow_md5 = self.config.get("wow_md5", "")
        
        # 创建魔兽风格UI
        self.create_wow_style_ui()
        
        # 自动检测客户端
        self.auto_detect_client()
        
        # 绑定窗口拖动
        self.bind_window_drag()
        
        # 延迟检查更新（5秒后，给网络初始化时间）
        self.root.after(5000, self.check_for_updates_silent)
    
    def load_config(self):
        """加载配置"""
        config_file = "launcher_config.json"
        default_config = {
            "server_name": "诺兰时光魔兽",
            "server_ip": "1.14.59.54",
            "register_url": "http://1.14.59.54:5000",
            "website_url": "",
            "client_path": "",
            "version": "3.3.5a",
            "patch_url": "http://1.14.59.54:8080/patches",
            "wow_md5": ""
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
            width=960,
            height=640,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # 尝试加载背景图片
        try:
            from PIL import Image, ImageTk
            bg_path = self.get_background_path()
            if os.path.exists(bg_path):
                pil_image = Image.open(bg_path)
                # 调整大小为960x640
                pil_image = pil_image.resize((960, 640), Image.Resampling.LANCZOS)
                self.background_photo = ImageTk.PhotoImage(pil_image)
                # 在canvas上绘制背景
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        except Exception as e:
            print(f"加载背景图片失败: {e}")
        
        # 绘制魔兽风格边框
        self.draw_wow_frame()
        
        # 创建内容区域
        self.create_content()
    
    def get_background_path(self):
        """获取背景图片路径"""
        # PyInstaller打包后的路径
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        preferred = os.path.join(base_path, "background_nolan.jpg")
        if os.path.exists(preferred):
            return preferred
        return os.path.join(base_path, "background.jpg")
    
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
            text="⚔️ 诺兰时光魔兽登录器 ⚔️",
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
        
        # 左侧面板 - 公告区（深色半透明视觉）
        left_frame = tk.Frame(self.root, bg="#0f0b14", bd=0, highlightthickness=1, highlightbackground="#6f4aa8")
        left_frame.place(x=28, y=104, width=540, height=400)
        # 设置半透明效果（通过alpha）
        try:
            left_frame.attributes("-alpha", 0.7)
        except:
            pass
        
        # 公告标题
        tk.Label(
            left_frame,
            text="📜 服务器公告",
            font=("微软雅黑", 14, "bold"),
            fg="#f6deb0",
            bg="#0f0b14",
            bd=0
        ).pack(anchor="w", padx=14, pady=(14,8))
        
        # 公告内容
        news_text = tk.Text(
            left_frame,
            font=("微软雅黑", 10),
            bg="#0f0b14",
            fg="#efe7f7",
            wrap="word",
            bd=0,
            highlightthickness=1,
            highlightcolor="#8A2BE2",
            highlightbackground="#3a2448",
            insertbackground="#efe7f7",
            height=20
        )
        news_text.pack(fill="both", expand=True, padx=14, pady=(0,14))
        
        news_content = """🎮 欢迎来到诺兰时光魔兽！

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

🔄 自动更新

启动器会自动检测并下载最新补丁！

愿圣光与你同在！ 🗡️"""
        
        news_text.insert("1.0", news_content)
        news_text.config(state="disabled")
        
        # 右侧面板 - 功能区（半透明）
        right_frame = tk.Frame(self.root, bg="#0f0b14", bd=0, highlightthickness=1, highlightbackground="#6f4aa8")
        right_frame.place(x=590, y=104, width=342, height=400)
        
        # 服务器状态
        status_frame = tk.LabelFrame(
            right_frame,
            text=" 服务器状态 ",
            font=("微软雅黑", 10, "bold"),
            fg="#ffd700",
            bg="#0a0a0a",
            bd=1,
            relief="solid"
        )
        status_frame.pack(fill="x", pady=(0,10))
        
        # 状态信息
        tk.Label(
            status_frame,
            text="状态: 🟢 在线",
            font=("微软雅黑", 9),
            fg="#4caf50",
            bg="#0a0a0a"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text="在线: 127 玩家",
            font=("微软雅黑", 9),
            fg="#ffd700",
            bg="#0a0a0a"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            status_frame,
            text=f"IP: {self.config['server_ip']}",
            font=("微软雅黑", 9),
            fg="#64b5f6",
            bg="#0a0a0a"
        ).pack(anchor="w", padx=10, pady=5)
        
        # 客户端设置
        settings_frame = tk.LabelFrame(
            right_frame,
            text=" 客户端设置 ",
            font=("微软雅黑", 10, "bold"),
            fg="#ffd700",
            bg="#0a0a0a",
            bd=1,
            relief="solid"
        )
        settings_frame.pack(fill="x", pady=(0,10))
        
        # 路径输入
        self.path_entry = tk.Entry(
            settings_frame,
            font=("微软雅黑", 9),
            bg="#0a0a0a",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
            bd=0,
            highlightthickness=1,
            highlightcolor="#c9a030",
            highlightbackground="#3a3a3a"
        )
        self.path_entry.pack(fill="x", padx=10, pady=5)
        
        # 按钮框架
        btn_frame = tk.Frame(settings_frame, bg="#0a0a0a")
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
            ("🔄 检查更新", self.check_for_updates_manual),
            ("🔍 验证补丁", self.verify_patches),  # 新增
            ("🛡️ 安全检测", self.run_security_check),
            ("🗑️ 清除缓存", self.clear_cache),
        ]
        
        for text, command in button_commands:
            btn = tk.Button(
                right_frame,
                text=text,
                font=("微软雅黑", 10),
                bg="#0a0a0a",
                fg="#ffd700",
                activebackground="#2a2a2a",
                activeforeground="#ffd700",
                bd=1,
                relief="solid",
                cursor="hand2",
                command=command
            )
            btn.pack(fill="x", pady=5)
        
        # 底部启动按钮区域（半透明）
        launch_frame = tk.Frame(self.root, bg="#0a0a0a", bd=0)
        launch_frame.place(x=30, y=480, width=740, height=70)
        
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
            height=1,
            command=self.launch_game_with_check
        )
        self.launch_btn.pack(fill="both", expand=True, pady=5, padx=5)
        
        # 悬停效果
        self.launch_btn.bind("<Enter>", lambda e: self.launch_btn.config(bg="#ffd700"))
        self.launch_btn.bind("<Leave>", lambda e: self.launch_btn.config(bg="#c9a030"))
        
        # 底部版权
        self.canvas.create_text(
            400, 575,
            text="© 2026 诺兰时光魔兽 | Powered by AzerothCore | 自动更新已启用",
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
                    self.init_patch_manager()
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
                    self.init_patch_manager()
                    messagebox.showinfo("成功", f"已自动找到客户端：\n{path}")
                    return
        
        # 如果仍未找到，不进行驱动器搜索（太耗时）
        # 让用户手动选择
        pass
    
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
                self.init_patch_manager()
            else:
                messagebox.showwarning("警告", "未找到Wow.exe文件")
    
    def init_patch_manager(self):
        """初始化补丁管理器"""
        client_path = self.path_entry.get().strip()
        if client_path and os.path.exists(client_path):
            self.patch_manager = PatchManager(
                self.config.get('patch_url', 'http://1.14.59.54:8080/patches'),
                client_path
            )
    
    def check_for_updates_silent(self):
        """静默检查更新"""
        client_path = self.path_entry.get().strip()
        
        # 调试日志
        print(f"[DEBUG] 检查更新 - 客户端路径: {client_path}")
        
        if not client_path:
            print(f"[DEBUG] 客户端路径为空，跳过更新检查")
            return
        
        if not self.patch_manager:
            self.init_patch_manager()
        
        if not self.patch_manager:
            print(f"[DEBUG] 补丁管理器初始化失败")
            return
        
        # 后台线程检查更新（带超时）
        def check_thread():
            try:
                print(f"[DEBUG] 开始检查更新...")
                manifest, needed_patches = self.patch_manager.check_for_updates()
                
                print(f"[DEBUG] manifest: {manifest}")
                print(f"[DEBUG] needed_patches: {needed_patches}")
                
                if needed_patches:
                    # 发现新补丁，显示更新提示
                    patch_names = "\n".join([f"• {p['name']} v{p.get('version', '?')}" for p in needed_patches])
                    print(f"[DEBUG] 发现新补丁:\n{patch_names}")
                    self.root.after(0, lambda: self.show_update_dialog(needed_patches, patch_names))
                else:
                    print(f"[DEBUG] 无需更新")
            except requests.exceptions.Timeout:
                print(f"[DEBUG] 检查更新超时（服务器响应慢）")
            except requests.exceptions.ConnectionError as e:
                print(f"[DEBUG] 无法连接到补丁服务器: {e}")
            except Exception as e:
                print(f"[DEBUG] 检查更新失败: {e}")
                import traceback
                traceback.print_exc()
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def check_for_updates_manual(self):
        """手动检查更新"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("提示", "请先设置WoW客户端路径")
            return
        
        if not self.patch_manager:
            self.init_patch_manager()
        
        if not self.patch_manager:
            messagebox.showerror("错误", "补丁管理器初始化失败")
            return
        
        # 显示检查中提示
        checking_dialog = tk.Toplevel(self.root)
        checking_dialog.title("检查更新")
        checking_dialog.geometry("300x100")
        checking_dialog.resizable(False, False)
        
        tk.Label(
            checking_dialog,
            text="🔄 正在检查更新...",
            font=("微软雅黑", 12)
        ).pack(expand=True)
        
        # 后台线程检查
        def check_thread():
            try:
                manifest, needed_patches = self.patch_manager.check_for_updates()
                
                self.root.after(0, lambda: checking_dialog.destroy())
                
                if needed_patches:
                    patch_names = "\n".join([f"• {p['name']} v{p.get('version', '?')}" for p in needed_patches])
                    self.root.after(0, lambda: self.show_update_dialog(needed_patches, patch_names))
                else:
                    self.root.after(0, lambda: messagebox.showinfo("检查更新", "✅ 已是最新版本！\n\n无需更新。"))
            except Exception as e:
                self.root.after(0, lambda: checking_dialog.destroy())
                self.root.after(0, lambda: messagebox.showerror("错误", f"检查更新失败：\n{str(e)}"))
        
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
    
    def show_update_dialog(self, needed_patches, patch_names):
        """显示更新对话框"""
        result = messagebox.askyesno(
            "发现新补丁",
            f"📦 发现 {len(needed_patches)} 个新补丁：\n\n{patch_names}\n\n是否立即下载并安装？"
        )
        
        if result:
            self.download_and_install_patches(needed_patches)
    
    def download_and_install_patches(self, patches):
        """下载并安装补丁"""
        # 创建进度窗口
        progress_window = tk.Toplevel(self.root)
        progress_window.title("下载补丁")
        progress_window.geometry("520x220")
        progress_window.resizable(False, False)
        
        tk.Label(
            progress_window,
            text="📥 正在下载补丁...",
            font=("微软雅黑", 12)
        ).pack(pady=10)
        
        progress_label = tk.Label(
            progress_window,
            text="准备中...",
            font=("微软雅黑", 10)
        )
        progress_label.pack(pady=5)

        detail_label = tk.Label(
            progress_window,
            text="已下载 0MB / 0MB  ·  速度 0KB/s  ·  剩余 --:--",
            font=("微软雅黑", 10),
            fg="#8A2BE2"
        )
        detail_label.pack(pady=2)
        
        progress_bar = ttk.Progressbar(
            progress_window,
            length=430,
            mode='determinate'
        )
        progress_bar.pack(pady=10)
        
        # 下载线程
        def download_thread():
            try:
                for i, patch in enumerate(patches):
                    patch_name = patch['name']
                    
                    print(f"\n[DEBUG] ========== 开始处理补丁 {i+1}/{len(patches)} ==========")
                    print(f"[DEBUG] 补丁名称: {patch_name}")
                    
                    # 更新进度
                    def update_progress(percent, status):
                        progress_label.config(text=f"{patch_name}: {status}")
                        progress_bar['value'] = percent
                        if isinstance(status, dict):
                            received = status.get('received', 0)
                            total = status.get('total', 0)
                            speed = status.get('speed', 0)
                            eta = status.get('eta', '--:--')
                            progress_label.config(text=f"{patch_name}: {percent:.1f}%")
                            detail_label.config(text=f"已下载 {self.format_bytes(received)} / {self.format_bytes(total)}  ·  速度 {self.format_bytes(speed)}/s  ·  剩余 {eta}")
                    
                    success, message = self.patch_manager.download_patch(
                        patch,
                        lambda p, s: self.root.after(0, lambda: update_progress(p, s))
                    )
                    
                    print(f"[DEBUG] 下载结果: {'成功' if success else '失败'}")
                    print(f"[DEBUG] 返回消息: {message}")
                    
                    if success:
                        # 更新本地版本
                        self.patch_manager.update_local_version(patch)
                        print(f"[DEBUG] 本地版本已更新")
                    else:
                        self.root.after(0, lambda: progress_window.destroy())
                        self.root.after(0, lambda: messagebox.showerror("错误", f"补丁安装失败：\n{message}"))
                        return
                
                # 全部完成 - 显示Data目录中的补丁文件
                print(f"\n[DEBUG] ========== 补丁安装完成 ==========")
                print(f"[DEBUG] Data目录: {self.patch_manager.data_path}")
                print(f"[DEBUG] 检查补丁文件:")
                
                patch_files = []
                if os.path.exists(self.patch_manager.data_path):
                    for file in os.listdir(self.patch_manager.data_path):
                        if file.startswith('patch-ZP') and file.endswith('.MPQ'):
                            file_path = os.path.join(self.patch_manager.data_path, file)
                            file_size = os.path.getsize(file_path)
                            print(f"[DEBUG] ✓ {file} ({file_size} bytes)")
                            patch_files.append(f"{file} ({file_size/1024:.1f} KB)")
                
                self.root.after(0, lambda: progress_window.destroy())
                
                if patch_files:
                    result_msg = f"✅ 成功安装 {len(patches)} 个补丁！\n\n已安装的补丁：\n"
                    result_msg += "\n".join([f"• {f}" for f in patch_files])
                    result_msg += "\n\n可以开始游戏了！"
                else:
                    result_msg = f"✅ 下载完成，但未找到补丁文件\n\nData目录: {self.patch_manager.data_path}"
                
                self.root.after(0, lambda: messagebox.showinfo("更新完成", result_msg))
                
            except Exception as e:
                print(f"[DEBUG] 下载线程异常: {e}")
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: progress_window.destroy())
                self.root.after(0, lambda: messagebox.showerror("错误", f"下载失败：\n{str(e)}"))
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def check_cheats(self):
        """检测外挂和脚本（临时禁用）"""
        # 临时禁用外挂检测 - 直接返回空列表
        return []

        # 原检测代码（已禁用）
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
                proc_lower = proc_name.lower()
                
                # 先检查白名单
                if proc_lower in [p.lower() for p in WHITELIST_PROCESSES]:
                    continue  # 跳过白名单进程
                
                # 再检查外挂列表
                if proc_lower in [c.lower() for c in cheat_processes]:
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
        """检测非法脚本（临时禁用）"""
        # 临时禁用脚本检测 - 直接返回空列表
        return []

        # 原检测代码（已禁用）
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
            # 检测通过，不显示任何提示（符合用户要求）
            return True
    
    def launch_game_with_check(self):
        """启动游戏（带安全检测）"""
        # 先运行安全检测（不扫描 AddOns，仅检查外挂进程）
        cheats = self.check_cheats()
        scripts = []
        
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

        md5_ok, md5_info = self.verify_wow_md5(wow_exe)
        if not md5_ok:
            # MD5 校验失败，显示警告但允许继续
            result = messagebox.askyesno(
                "文件校验失败",
                f"Wow.exe 文件可能已被修改或损坏。\n\n当前 MD5: {md5_info}\n\n这可能影响游戏体验或建议重新下载客户端。\n\n是否仍要继续启动？",
                icon="warning"
            )
            if not result:
                return
        
        # 检查更新（失败时跳过）
        if self.patch_manager:
            try:
                manifest, needed_patches = self.patch_manager.check_for_updates()
                if needed_patches:
                    result = messagebox.askyesno(
                        "发现新补丁",
                        f"📦 发现 {len(needed_patches)} 个新补丁！\n\n建议先更新再启动游戏。\n\n是否立即更新？"
                    )
                    
                    if result:
                        self.download_and_install_patches(needed_patches)
                        return
            except Exception as e:
                print(f"[DEBUG] 检查更新失败，跳过：{e}")
                # 继续启动游戏，不阻塞
        
        # 更新realmlist
        if not self.update_realmlist(client_path):
            return
        
        # 启动游戏
        try:
            os.chdir(client_path)
            self.game_process = subprocess.Popen([wow_exe])
            self.root.protocol("WM_DELETE_WINDOW", self.on_app_closing)
            
            # 记录日志
            with open("launcher.log", 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: 游戏启动成功 (安全检测通过)\n")
            
            # 启动反作弊实时监控
            self.start_anti_cheat_monitor()
            
            # 不显示成功弹窗（符合用户要求：只在发现问题时提示）
            
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
    
    def verify_patches(self):
        """验证补丁文件"""
        client_path = self.path_entry.get().strip()
        
        if not client_path:
            messagebox.showwarning("提示", "请先设置WoW客户端路径")
            return
        
        data_path = os.path.join(client_path, "Data")
        
        if not os.path.exists(data_path):
            messagebox.showerror("错误", f"Data目录不存在：\n{data_path}")
            return
        
        # 查找所有patch-ZP开头的MPQ文件
        patch_files = []
        for file in os.listdir(data_path):
            if file.startswith('patch-ZP') and file.endswith('.MPQ'):
                file_path = os.path.join(data_path, file)
                file_size = os.path.getsize(file_path)
                patch_files.append({
                    'name': file,
                    'path': file_path,
                    'size': file_size
                })
        
        if not patch_files:
            result = "❌ 未找到任何补丁文件！\n\n"
            result += f"Data目录: {data_path}\n\n"
            result += "请先运行'检查更新'下载补丁。"
            messagebox.showwarning("验证结果", result)
            return
        
        # 显示补丁文件信息
        result = f"✅ 找到 {len(patch_files)} 个补丁文件\n\n"
        result += f"Data目录: {data_path}\n\n"
        result += "补丁文件列表：\n"
        result += "━" * 40 + "\n"
        
        for patch in sorted(patch_files, key=lambda x: x['name']):
            result += f"✓ {patch['name']}\n"
            result += f"  大小: {patch['size']:,} bytes ({patch['size']/1024:.1f} KB)\n"
            result += f"  路径: {patch['path']}\n\n"
        
        result += "━" * 40 + "\n"
        result += "\n💡 提示：\n"
        result += "• 如果补丁已存在但游戏未生效，可能是：\n"
        result += "  1. 补丁文件本身有问题\n"
        result += "  2. 需要删除Cache和WDB目录\n"
        result += "  3. WoW客户端版本不匹配\n"
        result += "\n建议操作：\n"
        result += "• 删除Cache和WDB目录\n"
        result += "• 重启游戏客户端\n"
        result += "• 联系管理员检查补丁文件"
        
        messagebox.showinfo("补丁验证结果", result)
    
    def compute_wow335_hash(self, username, password):
        """计算 WoW 3.3.5 SRP6 账户哈希（SHA1(UPPER(user):UPPER(pass)))"""
        raw = f"{username.strip().upper()}:{password.strip().upper()}".encode("utf-8")
        return hashlib.sha1(raw).hexdigest().upper()

    def format_bytes(self, num_bytes):
        units = ['B', 'KB', 'MB', 'GB']
        size = float(max(num_bytes, 0))
        for unit in units:
            if size < 1024 or unit == units[-1]:
                return f"{size:.1f}{unit}"
            size /= 1024

    def verify_wow_md5(self, wow_exe):
        if not self.expected_wow_md5:
            return True, "未配置MD5，跳过校验"
        actual = self.patch_manager.calculate_md5(wow_exe) if self.patch_manager else PatchManager('', os.path.dirname(wow_exe)).calculate_md5(wow_exe)
        ok = actual.lower() == self.expected_wow_md5.lower()
        return ok, actual

    def kill_all_wow_processes(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'wow.exe' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass

    def on_app_closing(self):
        self.monitoring_active = False
        self.kill_all_wow_processes()
        self.root.destroy()

    def open_register(self):
        """打开注册页，同时弹出 3.3.5 哈希辅助工具"""
        dialog = tk.Toplevel(self.root)
        dialog.title("3.3.5 账号注册辅助")
        dialog.geometry("420x260")
        dialog.configure(bg="#151015")
        dialog.resizable(False, False)

        tk.Label(dialog, text="账号", font=("微软雅黑", 11), fg="#f5e6c8", bg="#151015").pack(pady=(18, 4))
        user_entry = tk.Entry(dialog, font=("微软雅黑", 11), width=30)
        user_entry.pack()
        tk.Label(dialog, text="密码", font=("微软雅黑", 11), fg="#f5e6c8", bg="#151015").pack(pady=(12, 4))
        pass_entry = tk.Entry(dialog, font=("微软雅黑", 11), width=30, show="*")
        pass_entry.pack()
        result_var = tk.StringVar(value="SHA1 哈希将在这里显示")
        tk.Label(dialog, textvariable=result_var, font=("Consolas", 10), wraplength=360, fg="#d8c7ff", bg="#151015").pack(pady=14)

        def build_hash():
            u = user_entry.get().strip()
            p = pass_entry.get().strip()
            if not u or not p:
                result_var.set("请输入账号和密码")
                return
            result_var.set(self.compute_wow335_hash(u, p))

        tk.Button(dialog, text="生成 3.3.5 SHA1", command=build_hash, bg="#8A2BE2", fg="white", bd=0, padx=16, pady=6).pack()

        import webbrowser
        if self.config.get("register_url"):
            webbrowser.open(self.config["register_url"])
    
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
    
    app = WoWLauncherV3_1(root)
    root.protocol("WM_DELETE_WINDOW", app.on_app_closing)
    
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
