#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1时光WoW 注册API服务器
提供账号注册功能
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import hashlib
import re
import os

app = Flask(__name__)
CORS(app)

# 数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'acore',
    'password': 'P1WoW2026!',
    'database': 'acore_auth'
}

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"数据库连接失败：{e}")
        return None

def hash_password(username, password):
    """生成WoW密码哈希"""
    # WoW使用的SHA1哈希：USERNAME:PASSWORD
    s = f"{username.upper()}:{password.upper()}"
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def validate_username(username):
    """验证用户名"""
    if not username:
        return False, "用户名不能为空"
    if len(username) < 3 or len(username) > 16:
        return False, "用户名长度必须在3-16个字符之间"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    return True, ""

def validate_password(password):
    """验证密码"""
    if not password:
        return False, "密码不能为空"
    if len(password) < 6 or len(password) > 32:
        return False, "密码长度必须在6-32个字符之间"
    return True, ""

def validate_email(email):
    """验证邮箱"""
    if not email:
        return False, "邮箱不能为空"
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "邮箱格式不正确"
    return True, ""

@app.route('/')
def index():
    """返回注册页面"""
    return send_from_directory('.', 'register.html')

@app.route('/api/register', methods=['POST'])
def register():
    """注册API"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()

        # 验证输入
        valid, msg = validate_username(username)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        valid, msg = validate_password(password)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        valid, msg = validate_email(email)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        # 连接数据库
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': '数据库连接失败'}), 500

        cursor = conn.cursor()

        # 检查用户名是否已存在
        cursor.execute("SELECT id FROM account WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '用户名已存在'}), 400

        # 检查邮箱是否已存在
        cursor.execute("SELECT id FROM account WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': '邮箱已被注册'}), 400

        # 生成密码哈希
        sha_pass_hash = hash_password(username, password)

        # 插入新账号
        sql = """
        INSERT INTO account (username, sha_pass_hash, email, reg_date, last_ip, online, expansion)
        VALUES (%s, %s, %s, NOW(), %s, 0, 2)
        """
        
        client_ip = request.remote_addr
        cursor.execute(sql, (username, sha_pass_hash, email, client_ip))
        conn.commit()
        
        account_id = cursor.lastrowid
        
        # 设置普通账号权限（gmlevel = 0）
        cursor.execute("INSERT INTO account_access (id, gmlevel, RealmID) VALUES (%s, 0, -1)", (account_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': '注册成功！',
            'account_id': account_id
        })

    except Exception as e:
        print(f"注册错误：{e}")
        return jsonify({'success': False, 'message': f'服务器错误：{str(e)}'}), 500

@app.route('/api/check-username/<username>')
def check_username(username):
    """检查用户名是否可用"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'available': False, 'message': '数据库连接失败'}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM account WHERE username = %s", (username,))
        exists = cursor.fetchone() is not None
        
        cursor.close()
        conn.close()

        return jsonify({
            'available': not exists,
            'message': '用户名可用' if not exists else '用户名已存在'
        })

    except Exception as e:
        return jsonify({'available': False, 'message': f'服务器错误：{str(e)}'}), 500

@app.route('/api/online')
def get_online_players():
    """获取在线玩家数"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'online': 0}), 500

        cursor = conn.cursor()
        
        # 查询acore_characters库的在线玩家
        conn_chars = mysql.connector.connect(
            host='127.0.0.1',
            user='acore',
            password='P1WoW2026!',
            database='acore_characters'
        )
        cursor_chars = conn_chars.cursor()
        cursor_chars.execute("SELECT COUNT(*) FROM characters WHERE online = 1")
        online_count = cursor_chars.fetchone()[0]
        
        cursor_chars.close()
        conn_chars.close()
        cursor.close()
        conn.close()

        return jsonify({'online': online_count})

    except Exception as e:
        print(f"获取在线人数错误：{e}")
        return jsonify({'online': 0}), 500

if __name__ == '__main__':
    print("="*50)
    print("P1时光WoW 注册服务器")
    print("="*50)
    print()
    print("访问地址：")
    print("  本地：http://localhost:5000")
    print("  外网：http://1.14.59.54:5000")
    print()
    print("数据库配置：")
    print(f"  主机：{DB_CONFIG['host']}")
    print(f"  用户：{DB_CONFIG['user']}")
    print(f"  数据库：{DB_CONFIG['database']}")
    print()
    print("按 Ctrl+C 停止服务器")
    print("="*50)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
