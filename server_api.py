#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WoW服务器状态API模拟
实际部署时可以集成到服务器上
"""

from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/status')
def get_status():
    """获取服务器状态"""
    # 实际部署时，这里应该查询数据库
    # 示例：
    # cursor.execute("SELECT COUNT(*) FROM characters WHERE online = 1")
    # online_players = cursor.fetchone()[0]
    
    return jsonify({
        "status": "online",
        "online_players": random.randint(50, 150),
        "max_players": 500,
        "uptime": "23:45:12",
        "version": "3.3.5a"
    })

@app.route('/api/online')
def get_online():
    """获取在线人数"""
    return jsonify({
        "online": random.randint(50, 150)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
