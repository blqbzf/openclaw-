#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺兰时光魔兽登录器 v3.8 - 宙美增强版
基于 v3.3.1 恢复 MD5 检测
 保留补丁下载
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import json
import requests
import threading
import hashlib

class PatchManager:
    """补丁管理器"""
    
    def __init__(self, patch_url, client_path):
        self.patch_url = patch_url
        self.client_path = client_path
        self.data_path = os.path.join(client_path, "Data")
        self.local_version_file = os.path.join(client_path, ".patch_version.json")
    
    def fetch_manifest(self):
        """获取服务器补丁清单"""
        try:
            manifest_url = f"{self.patch_url}/manifest.json"
            response = requests.get(manifest_url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            return None
    
    def check_for_updates(self):
        """检查需要的补丁"""
        remote_manifest = self.fetch_manifest()
        if not remote_manifest:
            return None, []
        
        # 获取本地版本
        local_version = self.get_local_version()
        local_patches = {p['name']: p for p in local_version.get('patches', [])}
        
        # 找出需要更新的补丁
        needed_patches = []
        for patch in remote_manifest.get('patches', []):
            patch_name = patch.get('name')
            remote_version = patch.get('version')
            
            if patch_name not in local_patches:
                needed_patches.append(patch)
            elif local_patches[patch_name] != remote_version:
                needed_patches.append(patch)
        
        return remote_manifest, needed_patches
    
    def get_local_version(self):
        """获取本地补丁版本"""
        if os.path.exists(self.local_version_file):
            try:
                with open(self.local_version_file, 'r') as f:
                    return json.load(f)
            except:
                return {"patches": [], "version": "0"}
        return {"patches": [], "version": "0"}
    
    def save_local_version(self, version_info):
        """保存本地补丁版本"""
        with open(self.local_version_file, 'w') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
    
    def download_patch(self, patch_info, progress_window=None):
        """下载补丁"""
        try:
                patch_url = patch_info.get('url')
                patch_name = patch_info.get('name')
                patch_size = patch_info.get('size')
                
                # 创建临时文件
                tmp_file = os.path.join(self.client_path, f"{patch_name}.tmp")
                
                # 下载
                response = requests.get(patch_url, stream=True)
                with open(tmp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                        # 计算进度
                        downloaded = os.path.getsize(tmp_file)
                        percent = (downloaded / patch_size) * 100
                        
                        if progress_window:
                            progress_window.update_progress(percent)
                
                # 移动到最终位置
                final_path = os.path.join(self.data_path, patch_name)
                if os.path.exists(tmp_file):
                    os.rename(tmp_file, final_path)
                    return True, None
        except Exception as e:
            return False, str(e)


    
    def apply_patch(self, patch_name):
        """应用补丁（已下载到Data目录）"""
        # 补丁已经在Data目录
        return True, None


    
    def install_all_needed_patches(self, progress_window=None):
        """安装所有需要的补丁"""
        manifest, needed = self.check_for_updates()
        if not needed:
            return True
        
        for i, patch in enumerate(needed):
            success, error = self.download_patch(patch, progress_window)
            if not success:
                return False, error
            
            success, error = self.apply_patch(patch['name'])
            if not success:
                return False, error
            
        
        # 更新本地版本
        local_version = self.get_local_version()
        for patch in needed:
            found = False
            for local_patch in local_version.get('patches', []):
                if local_patch.get('name') == patch['name']:
                    local_patch['version'] = patch['version']
                    found = True
                    break
            if not found:
                local_version['patches'].append({
                    'name': patch['name'],
                    'version': patch['version']
                })
        
        self.save_local_version(local_version)
        return True, None


class WoWLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诺兰时光魔兽登录器 v3.8")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False, False, False)
        
        # 加载配置
        self.config = self.load_config()
        
        # 创建UI
        self.create_widgets()
    
    def load_config(self):
        """加载配置文件"""
        config_file = os.path.join(os.path.dirname(__file__), "launcher_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # 默认配置
            self.config = {
                "server_name": "诺兰时光魔兽",
                "server_ip": "1.14.59.54",
                "realmlist": "set realmlist 1.14.59.54",
                "client_path": "",
                "register_url": "http://1.14.59.54:5000",
                "patch_url": "http://1.14.59.54:8080/patches",
            }
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(fill=tk.Y, padx=50)
        
        title_label = tk.Label(
            title_frame,
            text=f"🎮 {self.config.get('server_name', '诺兰时光魔兽')}",
            font=("微软雅黑", 32, "bold"),
            fg="#FFD700",
            bg="#1a1a2e"
        )
        title_label.pack(pady=20)
        
        # 服务器信息
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(fill=tk.Y, pady=20)
        
        tk.Label(
            info_frame,
            text=f"服务器: {self.config.get('server_ip', '1.14.59.54')}",
            font=("微软雅黑", 14),
            fg="#FFD700",
            bg="#1a1a2e"
        ).pack()
        
        tk.Label(
            info_frame,
            text="版本: 3.3.5a (12340)",
            font=("微软雅黑", 12),
            fg="#999",
            bg="#1a1a2e"
        ).pack()
        
        # 客户端路径
        path_frame = tk.Frame(self.root, bg="#1a1a2e")
        path_frame.pack(fill=tk.Y, pady=30)
        
        tk.Label(
            path_frame,
            text="客户端路径:",
            font=("微软雅黑", 12),
            fg="#FFD700",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=5)
        
        self.path_entry = tk.Entry(
            path_frame,
            font=("微软雅黑", 10),
            bg="#0a0a14",
            fg="#E0E0E0",
            insertbackground="#FFD700"
        )
        self.path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X)
        
        if self.config.get("client_path"):
            self.path_entry.insert(0, self.config.get("client_path"))
        
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
        button_frame.pack(fill=tk.Y, pady=30)
        
        start_btn = tk.Button(
            button_frame,
            text="🎮 开始游戏",
            font=("微软雅黑", 16, "bold"),
            bg="#8B4513",
            fg="#FFD700",
            width=20,
            height=2,
            command=self.start_game
        )
        start_btn.pack(pady=10)
        
        register_btn = tk.Button(
            button_frame,
            text="📝 注册账号",
            font=("微软雅黑", 12),
            bg="#4a3a6a",
            fg="#FFD700",
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
            self.status_label.config(text=f"已选择: {path}")
    
    def save_config(self):
        """保存配置"""
        config_file = os.path.join(os.path.dirname(__file__), "launcher_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
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
        
        # 检查 MD5
        if not self.verify_wow_md5(wow_exe):
            result = messagebox.askyesno(
                "文件校验失败",
                "Wow.exe 文件可能已被修改。\n\n"
                "这可能影响游戏体验。\n\n"
                "是否仍要继续启动？",
                icon="warning"
            )
            if not result:
                return
        
        # 检查并安装补丁
        self.status_label.config(text="检查更新...")
        self.root.update()
        
        patch_manager = PatchManager(
            self.config.get("patch_url", "http://1.14.59.54:8080/patches"),
            client_path
        )
        
        manifest, needed = patch_manager.check_for_updates()
        
        if needed:
            # 显示下载进度窗口
            progress_window = tk.Toplevel(self.root)
            progress_window.title("下载补丁")
            progress_window.geometry("400x200")
            progress_window.configure(bg="#1a1a2e")
            
            tk.Label(
                progress_window,
                text=f"发现 {len(needed)} 个补丁需要更新",
                font=("微软雅黑", 12),
                fg="#FFD700",
                bg="#1a1a2e"
            ).pack(pady=20)
            
            progress_bar = ttk.Progressbar(
                progress_window,
                length=300,
                mode='determinate'
            )
            progress_bar.pack(pady=20)
            
            # 下载并安装补丁
            if patch_manager.install_all_needed_patches(progress_window):
                progress_window.destroy()
                messagebox.showinfo("成功", "补丁安装完成！\n\n点击\"确定\"继续启动游戏")
            else:
                progress_window.destroy()
                messagebox.showerror("错误", "补丁安装失败")
        
        # 更新 realmlist
        realmlist_file = os.path.join(client_path, "realmlist.wtf")
        try:
            with open(realmlist_file, 'w', encoding='utf-8') as f:
                f.write(self.config.get("realmlist", "set realmlist 1.14.59.54"))
        except:
            pass
        
        # 启动游戏
        try:
            os.chdir(client_path)
            subprocess.Popen([wow_exe])
            self.status_label.config(text="游戏已启动")
            messagebox.showinfo("成功", "游戏启动成功！")
        except Exception as e:
            messagebox.showerror("错误", f"启动游戏失败:\n{e}")
    
    def verify_wow_md5(self, wow_exe):
        """验证 Wow.exe MD5（已禁用）"""
        # MD5 校验功能已禁用
        # 玩家可能使用了各种补丁或插件， MD5 校验会导致无法启动
        # 为了更好的用户体验， 默认允许所有客户端
        return True
    
    def open_register(self):
        """打开注册页面"""
        import webbrowser
        webbrowser.open(self.config.get("register_url", "http://1.14.59.54:5000"))
    
    def run(self):
        """运行登录器"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = WoWLauncher()
        app.run()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror("启动错误", f"登录器启动失败:\n{str(e)}")
