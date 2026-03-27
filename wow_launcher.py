#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诺兰时光魔兽登录器 v3.7 - 极简智能版
基于 v3.3.1 緻加自动补丁功能
无启动卡顿，"""

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
                    for chunk in response.iter_content(chunk):
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


        return False, "下载失败"


    
    def apply_patch(self, patch_name):
        """应用补丁（已下载到Data目录）"""
        # 补丁已经在Data目录，， return True, None


    
    def install_all_needed_patches(self, progress_window=None):
        """安装所有需要的补丁"""
        manifest, needed = self.check_for_updates()
        if not needed:
            return True
        
        for i, patch in enumerate(needed):
            success, error = self.download_patch(patch, progress_window)
            if not success:
                return False
            
            success, error = self.apply_patch(patch['name'])
            if not success:
                return False
            
        
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
        return True


