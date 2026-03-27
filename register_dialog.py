#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程账号注册对话框
"""

import tkinter as tk
from tkinter import messagebox
import requests
import threading


class RegisterDialog:
    """注册对话框"""
    
    def __init__(self, parent, config):
        self.config = config
        self.api_url = f"http://{config['server_ip']}:8081"
        self.api_key = "nolan_wow_2026_secret_key"
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("注册账号")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() - 400) // 2
        y = (self.dialog.winfo_screenheight() - 300) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        tk.Label(
            main_frame,
            text="注册新账号",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # 用户名
        tk.Label(main_frame, text="用户名 (3-16个字母或数字):").pack(anchor=tk.W)
        self.username_entry = tk.Entry(main_frame, width=40)
        self.username_entry.pack(pady=(0, 10), fill=tk.X)
        
        # 密码
        tk.Label(main_frame, text="密码 (至少6个字符):").pack(anchor=tk.W)
        self.password_entry = tk.Entry(main_frame, show="*", width=40)
        self.password_entry.pack(pady=(0, 10), fill=tk.X)
        
        # 确认密码
        tk.Label(main_frame, text="确认密码:").pack(anchor=tk.W)
        self.confirm_entry = tk.Entry(main_frame, show="*", width=40)
        self.confirm_entry.pack(pady=(0, 10), fill=tk.X)
        
        # 邮箱（可选）
        tk.Label(main_frame, text="邮箱 (可选，用于找回密码):").pack(anchor=tk.W)
        self.email_entry = tk.Entry(main_frame, width=40)
        self.email_entry.pack(pady=(0, 20), fill=tk.X)
        
        # 按钮
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame,
            text="注册",
            command=self.register,
            width=15,
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="取消",
            command=self.dialog.destroy,
            width=15
        ).pack(side=tk.RIGHT, padx=5)
    
    def register(self):
        """注册账号"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # 验证输入
        if not username or not password:
            messagebox.showwarning("提示", "请输入用户名和密码", parent=self.dialog)
            return
        
        if len(username) < 3 or len(username) > 16:
            messagebox.showwarning("提示", "用户名必须是3-16个字符", parent=self.dialog)
            return
        
        if not username.isalnum():
            messagebox.showwarning("提示", "用户名只能包含字母和数字", parent=self.dialog)
            return
        
        if len(password) < 6:
            messagebox.showwarning("提示", "密码至少需要6个字符", parent=self.dialog)
            return
        
        if password != confirm:
            messagebox.showwarning("提示", "两次输入的密码不一致", parent=self.dialog)
            return
        
        # 禁用按钮，显示加载中
        self.dialog.config(cursor="watch")
        
        # 在后台线程注册
        def do_register():
            try:
                url = f"{self.api_url}/register"
                data = {
                    "username": username,
                    "password": password,
                    "email": email,
                    "api_key": self.api_key
                }
                
                response = requests.post(url, json=data, timeout=10)
                result = response.json()
                
                self.dialog.after(0, lambda: self.on_register_complete(result, username, password))
            
            except requests.exceptions.Timeout:
                self.dialog.after(0, lambda: messagebox.showerror(
                    "错误",
                    "连接服务器超时，请检查网络连接",
                    parent=self.dialog
                ))
            except requests.exceptions.ConnectionError:
                self.dialog.after(0, lambda: messagebox.showerror(
                    "错误",
                    "无法连接到服务器，请检查网络连接",
                    parent=self.dialog
                ))
            except Exception as e:
                self.dialog.after(0, lambda: messagebox.showerror(
                    "错误",
                    f"注册失败：{str(e)}",
                    parent=self.dialog
                ))
            finally:
                self.dialog.after(0, lambda: self.dialog.config(cursor=""))
        
        threading.Thread(target=do_register, daemon=True).start()
    
    def on_register_complete(self, result, username, password):
        """注册完成回调"""
        if result.get('success'):
            messagebox.showinfo(
                "注册成功",
                f"账号注册成功！\n\n用户名: {username}\n密码: {password}\n\n现在可以登录游戏了！",
                parent=self.dialog
            )
            self.dialog.destroy()
        else:
            messagebox.showerror(
                "注册失败",
                result.get('message', '未知错误'),
                parent=self.dialog
            )


if __name__ == "__main__":
    # 测试代码
    root = tk.Tk()
    root.withdraw()
    
    config = {
        "server_ip": "1.14.59.54"
    }
    
    dialog = RegisterDialog(root, config)
    root.mainloop()
