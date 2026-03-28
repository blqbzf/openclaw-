import hashlib
import os
import secrets
from pathlib import Path

import pymysql
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent

DB_CONFIG = {
    'host': os.getenv('NOLAN_DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('NOLAN_DB_PORT', '3306')),
    'user': os.getenv('NOLAN_DB_USER', 'acore'),
    'password': os.getenv('NOLAN_DB_PASSWORD', 'Acore123456!'),
    'database': os.getenv('NOLAN_DB_NAME', 'acore_auth'),
    'charset': 'utf8mb4',
    'autocommit': False,
}

SERVER_NAME = os.getenv('NOLAN_SERVER_NAME', '诺兰时光魔兽')
DEFAULT_EMAIL_DOMAIN = os.getenv('NOLAN_EMAIL_DOMAIN', 'nolan.local')
SECRET_KEY = os.getenv('NOLAN_SECRET_KEY', 'nolan-minimal-register')
PORT = int(os.getenv('PORT', '5000'))

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False

# AzerothCore SRP6 params
G = 7
N = int('894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7', 16)


def sha1_bytes(*parts) -> bytes:
    h = hashlib.sha1()
    for part in parts:
        if isinstance(part, str):
            h.update(part.encode('utf-8'))
        else:
            h.update(part)
    return h.digest()


def upper_latin(s: str) -> str:
    return (s or '').strip().upper()


def make_registration_data(username: str, password: str):
    username = upper_latin(username)
    password = upper_latin(password)
    salt = secrets.token_bytes(32)
    inner = sha1_bytes(username, ':', password)
    # AzerothCore BigNumber defaults to little-endian byte interpretation/output.
    x = int.from_bytes(sha1_bytes(salt, inner), 'little')
    verifier_int = pow(G, x, N)
    verifier = verifier_int.to_bytes(32, 'little')
    return salt, verifier


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def validate_input(username: str, password: str, email: str):
    username = (username or '').strip()
    password = (password or '').strip()
    email = (email or '').strip()

    if not username or not password:
        return False, '账号和密码不能为空'
    if len(username) < 3 or len(username) > 16:
        return False, '账号长度必须在 3 到 16 位之间'
    if not username.isalnum():
        return False, '账号只能使用英文字母和数字'
    if len(password) < 6 or len(password) > 32:
        return False, '密码长度必须在 6 到 32 位之间'
    if email and ('@' not in email or '.' not in email.split('@')[-1]):
        return False, '邮箱格式不正确'
    return True, ''


@app.get('/')
def index():
    return render_template('index.html', server_name=SERVER_NAME)


@app.get('/health')
def health():
    return jsonify({'ok': True, 'server': SERVER_NAME})


@app.post('/api/register')
def api_register():
    try:
        data = request.get_json(silent=True) or request.form or {}
        username = (data.get('username') or '').strip()
        password = (data.get('password') or '').strip()
        email = (data.get('email') or '').strip()

        ok, message = validate_input(username, password, email)
        if not ok:
            return jsonify({'success': False, 'message': message}), 400

        username_up = upper_latin(username)
        if not email:
            email = f'{username.lower()}@{DEFAULT_EMAIL_DOMAIN}'

        salt, verifier = make_registration_data(username_up, password)

        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM account WHERE username = %s', (username_up,))
                if cur.fetchone():
                    return jsonify({'success': False, 'message': '账号已存在'}), 409

                cur.execute('SELECT id FROM account WHERE email = %s', (email,))
                if cur.fetchone():
                    return jsonify({'success': False, 'message': '邮箱已被使用'}), 409

                cur.execute(
                    '''
                    INSERT INTO account (username, salt, verifier, email, reg_mail, expansion)
                    VALUES (%s, %s, %s, %s, %s, 2)
                    ''',
                    (username_up, salt, verifier, email, email),
                )
                conn.commit()
        finally:
            conn.close()

        return jsonify({
            'success': True,
            'message': '注册成功，现在可以回到登录器启动游戏。',
            'username': username_up,
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {e}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
