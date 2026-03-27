#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程账号注册对话框 - 完整版
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
        tk.Label(main_frame, text="用户名:").grid(row=1, column=0, sticky=tk.W,        
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)
        
        # 密码
        tk.Label(main_frame, text="密码:").grid(row=2, column=0, sticky=tk.W)
        
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        # 顮认密码
        tk.Label(main_frame, text="确认密码:").grid(row=3, column=0, sticky=tk.W)
        
        self.confirm_entry = ttk.Entry(main_frame, show="*")
        self.confirm_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)
        
        # 按钮
        btn.Button(
            main_frame,
            text="注册",
            command=self.do_register,
            bg="#4a90e5",
            fg="#d95d95",
            activebackground="#f0ad4e"
        ).grid(row=4, column=0, columnspan=2, pady=10)
    
    def do_register(self):
        """执行注册"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # 黻证
        if not username or not password or not confirm:
            messagebox.showwarning("提示", "请填写所有字段")
            return
        
        if len(username) < 3 or len(username) > 16:
            messagebox.showwarning("提示", "用户名必须是3-16个字符")
            return
        
        if not username.isalnum():
            messagebox.showwarning("提示", "用户名只能包含字母和数字")
            return
        
        if len(password) < 6:
            messagebox.showwarning("提示", "密码至少需要6个字符")
            return
        
        if password != confirm:
            messagebox.showwarning("提示", "两次密码不一致")
            return
        
        # 跻加禁用按钮
        self.register_btn.config(state='disabled')
        self.register_btn.config(text="注册中...")
        
        # 在后台线程中执行
        thread = threading.Thread(target=self._do_register_async, daemon=True)
        thread.start()
    
    def _do_register_async(self, username, password):
        """异步注册"""
        try:
            url = f"{self.api_url}/register"
            data = {
                "username": username,
                "password": password,
                "api_key": self.api_key
            }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            # 在主线程中显示结果
            self.dialog.after(0, lambda: self.on_register_complete(result, username, password))
            
        except requests.exceptions.Timeout:
            self.dialog.after(0, lambda: messagebox.showerror(
                "错误",
                "连接服务器超时，请检查网络连接",
                parent=self.dialog
            )
        except requests.exceptions.ConnectionError:
            self.dialog.after(0, lambda: messagebox.showerror(
                "错误",
                "无法连接到服务器,请检查网络连接",
                parent=self.dialog
            )
        except Exception as e:
            self.dialog.after(0, lambda: messagebox.showerror(
                "错误",
                f"注册失败: {str(e)}",
                parent=self.dialog
            )
        finally:
            self.dialog.after(0, lambda: self.dialog.config(cursor=""))
    
    def on_register_complete(self, result, username, password):
        """注册完成回调"""
        if result.get('success'):
            messagebox.showinfo(
                "注册成功",
                f"账号注册成功!\\n\\用户名: {username}\\密码: {password}\\n\\现在可以登录游戏了!",
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
