import json
import logging
import subprocess
import sys
import threading
import webbrowser
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

ROOT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_DIR / 'launcher_config.json'
STATE_PATH = ROOT_DIR / 'launcher_state.json'
LOG_PATH = ROOT_DIR / 'launcher.log'
BG_PATH = ROOT_DIR / 'assets' / 'background.jpg'
TIMEOUT = 5
LOGGER = logging.getLogger('nuolan_launcher')


def setup_logging():
    LOGGER.setLevel(logging.INFO)
    LOGGER.handlers.clear()
    handler = RotatingFileHandler(LOG_PATH, maxBytes=512 * 1024, backupCount=2, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.propagate = False
    LOGGER.info('launcher boot')


def load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        LOGGER.exception('load_json failed: %s', e)
    return default


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.config = load_json(CONFIG_PATH, {})
        self.state = load_json(STATE_PATH, {'client_path': ''})
        self.minimal_mode = bool(self.config.get('ui', {}).get('minimal_mode', False))
        self.client_path = tk.StringVar(value=self.state.get('client_path', '') or self.config.get('client_path', ''))
        self.status_text = tk.StringVar(value='正在检查服务器状态...')
        self.server_text = tk.StringVar(value='服务器：检查中')
        self.path_hint = tk.StringVar(value='请选择 3.3.5a (12340) 客户端目录')
        self.action_hint = tk.StringVar(value='先注册账号，再选客户端目录，然后点击启动游戏')
        self.bg_tk = None
        self.setup_window()
        self.build_ui()
        self.refresh_status_async()
        self.validate_client_path(show_popup=False)

    def setup_window(self):
        ui = self.config.get('ui', {})
        width = int(ui.get('width', 960))
        height = int(ui.get('height', 640))
        min_width = int(ui.get('min_width', 900))
        min_height = int(ui.get('min_height', 580))
        self.root.title(self.config.get('window_title', '诺兰时光魔兽登录器'))
        self.root.geometry(f'{width}x{height}')
        self.root.minsize(min_width, min_height)
        self.root.configure(bg='#07111f')
        LOGGER.info('window setup width=%s height=%s minimal=%s', width, height, self.minimal_mode)

    def build_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg='#07111f')
        self.canvas.pack(fill='both', expand=True)
        self.root.bind('<Configure>', self.on_resize)

        self.main = tk.Frame(self.canvas, bg='#07111f')
        self.main_window = self.canvas.create_window((0, 0), window=self.main, anchor='nw')
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        top = tk.Frame(self.main, bg='#07111f')
        top.pack(fill='x', padx=24, pady=(24, 12))
        tk.Label(top, text=self.config.get('server_name', '诺兰时光魔兽'), fg='#edf4ff', bg='#07111f', font=('Microsoft YaHei UI', 24, 'bold')).pack(anchor='w')
        tk.Label(top, text=f"最小可测版  |  客户端版本：{self.config.get('game_version', '3.3.5a (12340)')}", fg='#98a7d1', bg='#07111f', font=('Microsoft YaHei UI', 11)).pack(anchor='w', pady=(6, 0))

        body = tk.Frame(self.main, bg='#07111f')
        body.pack(fill='both', expand=True, padx=24, pady=12)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        left = tk.Frame(body, bg='#0d1830', bd=0, highlightthickness=1, highlightbackground='#22365f')
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        right = tk.Frame(body, bg='#0d1830', bd=0, highlightthickness=1, highlightbackground='#22365f')
        right.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        self.build_left(left)
        self.build_right(right)
        self.paint_background()

    def build_left(self, parent):
        inner = tk.Frame(parent, bg='#0d1830')
        inner.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(inner, text='步骤 1：注册账号', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w')
        tk.Button(inner, text='打开注册页', command=self.open_register, bg='#235a9f', fg='white', activebackground='#2c6dbc', relief='flat', padx=18, pady=12).pack(anchor='w', pady=(10, 16))

        tk.Label(inner, text='步骤 2：选择客户端目录', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w')
        row = tk.Frame(inner, bg='#0d1830')
        row.pack(fill='x', pady=(10, 8))
        self.path_entry = tk.Entry(row, textvariable=self.client_path, font=('Consolas', 11), bg='#08111f', fg='#edf4ff', insertbackground='#edf4ff', relief='flat')
        self.path_entry.pack(side='left', fill='x', expand=True, ipady=10)
        tk.Button(row, text='选择目录', command=self.select_client_path, bg='#182846', fg='white', activebackground='#20345a', relief='flat', padx=16, pady=10).pack(side='left', padx=(10, 0))
        tk.Label(inner, textvariable=self.path_hint, fg='#98a7d1', bg='#0d1830', font=('Microsoft YaHei UI', 10)).pack(anchor='w', pady=(0, 16))

        tk.Label(inner, text='步骤 3：启动游戏', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w')
        btns = tk.Frame(inner, bg='#0d1830')
        btns.pack(fill='x', pady=(10, 16))
        tk.Button(btns, text='验证目录', command=lambda: self.validate_client_path(show_popup=True), bg='#1e3a63', fg='white', activebackground='#274a7e', relief='flat', padx=18, pady=12).pack(side='left')
        tk.Button(btns, text='启动游戏', command=self.launch_game, bg='#2bb673', fg='white', activebackground='#239a61', relief='flat', padx=24, pady=12).pack(side='left', padx=10)

        tk.Label(inner, text='当前说明', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w')
        notice = tk.Text(inner, height=14, wrap='word', bg='#08111f', fg='#dbe7ff', relief='flat', font=('Microsoft YaHei UI', 10))
        notice.pack(fill='both', expand=True, pady=(10, 0))
        notice.insert('1.0', self.config.get('news', ''))
        notice.configure(state='disabled')

    def build_right(self, parent):
        inner = tk.Frame(parent, bg='#0d1830')
        inner.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(inner, text='链路检查', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w')
        self.make_status_card(inner, '服务器状态', self.server_text)
        self.make_status_card(inner, '接口状态', self.status_text)
        self.make_status_card(inner, '操作提示', self.action_hint)

        tips = (
            '最小可测版目标：\n\n'
            '• 注册页能否打开\n'
            '• 客户端目录能否识别\n'
            '• realmlist.wtf 能否自动写入\n'
            '• Wow.exe 能否拉起并连接服务器\n\n'
            '如果失败：\n'
            '• 回传 launcher.log\n'
            '• 告诉我卡在哪一步\n'
        )
        tk.Label(inner, text='测试重点', fg='#cbd9ff', bg='#0d1830', font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor='w', pady=(18, 8))
        msg = tk.Text(inner, height=14, wrap='word', bg='#08111f', fg='#dbe7ff', relief='flat', font=('Microsoft YaHei UI', 10))
        msg.pack(fill='both', expand=True)
        msg.insert('1.0', tips)
        msg.configure(state='disabled')

    def make_status_card(self, parent, title, var):
        frame = tk.Frame(parent, bg='#101d38', highlightthickness=1, highlightbackground='#22365f')
        frame.pack(fill='x', pady=(10, 0))
        tk.Label(frame, text=title, fg='#98a7d1', bg='#101d38', font=('Microsoft YaHei UI', 10)).pack(anchor='w', padx=14, pady=(12, 4))
        tk.Label(frame, textvariable=var, fg='#edf4ff', bg='#101d38', font=('Microsoft YaHei UI', 12, 'bold'), wraplength=280, justify='left').pack(anchor='w', padx=14, pady=(0, 12))

    def on_resize(self, _event=None):
        self.paint_background()

    def on_canvas_configure(self, event):
        try:
            self.canvas.itemconfigure(self.main_window, width=event.width, height=event.height)
        except Exception as e:
            LOGGER.exception('on_canvas_configure failed: %s', e)

    def paint_background(self):
        if not (Image and ImageTk and BG_PATH.exists()):
            return
        try:
            w = max(self.root.winfo_width(), 900)
            h = max(self.root.winfo_height(), 580)
            img = Image.open(BG_PATH).convert('RGB')
            img = img.resize((w, h))
            overlay = Image.new('RGBA', img.size, (7, 17, 31, 165))
            img = Image.blend(img.convert('RGBA'), overlay, 0.42)
            self.bg_tk = ImageTk.PhotoImage(img)
            self.canvas.delete('bg')
            self.canvas.create_image(0, 0, image=self.bg_tk, anchor='nw', tags='bg')
            self.canvas.tag_lower('bg')
        except Exception as e:
            LOGGER.exception('paint_background failed: %s', e)

    def select_client_path(self):
        path = filedialog.askdirectory(title='选择 WoW 客户端目录')
        if path:
            LOGGER.info('client path selected: %s', path)
            self.client_path.set(path)
            self.persist_state()
            self.validate_client_path(show_popup=False)

    def persist_state(self):
        self.state['client_path'] = self.client_path.get().strip()
        save_json(STATE_PATH, self.state)
        LOGGER.info('state persisted')

    def get_base_path(self):
        raw = self.client_path.get().strip()
        return Path(raw) if raw else None

    def get_executable_candidates(self, base: Path):
        exes = self.config.get('launch', {}).get('preferred_executables', ['Wow.exe', 'Wow-64.exe'])
        return [base / name for name in exes]

    def get_wow_exe(self):
        base = self.get_base_path()
        if not base:
            return None
        for p in self.get_executable_candidates(base):
            if p.exists():
                return p
        return None

    def realmlist_candidates(self, base: Path):
        rels = self.config.get('launch', {}).get('realmlist_candidates', [
            'Data/zhCN/realmlist.wtf',
            'Data/enUS/realmlist.wtf',
            'realmlist.wtf'
        ])
        return [base / rel for rel in rels]

    def validate_client_path(self, show_popup=False):
        base = self.get_base_path()
        if not base:
            self.path_hint.set('请选择 WoW 客户端目录')
            return False
        if not base.exists() or not base.is_dir():
            LOGGER.warning('invalid client directory: %s', base)
            self.path_hint.set('目录不存在或不可访问')
            if show_popup:
                messagebox.showerror('目录无效', f'目录不存在：\n{base}')
            return False
        wow_exe = self.get_wow_exe()
        if not wow_exe:
            LOGGER.warning('wow executable missing under: %s', base)
            self.path_hint.set('未找到 Wow.exe / Wow-64.exe')
            if show_popup:
                messagebox.showerror('目录无效', '该目录下未找到 Wow.exe 或 Wow-64.exe。')
            return False
        self.path_hint.set(f'已识别客户端：{wow_exe.name}')
        if show_popup:
            messagebox.showinfo('目录有效', f'已识别客户端：\n{wow_exe}')
        return True

    def write_realmlist(self, base: Path):
        content = self.config.get('realmlist', f"set realmlist {self.config.get('server_ip', '127.0.0.1')}") + '\n'
        last_err = None
        for p in self.realmlist_candidates(base):
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding='utf-8')
                LOGGER.info('realmlist written: %s', p)
                return p
            except Exception as e:
                last_err = e
                LOGGER.warning('realmlist write failed: %s (%s)', p, e)
        raise RuntimeError(f'写入 realmlist 失败: {last_err}')

    def open_register(self):
        url = (self.config.get('register_url') or '').strip()
        if not url:
            messagebox.showerror('注册链接缺失', '当前未配置注册链接。')
            return
        LOGGER.info('open register url: %s', url)
        try:
            webbrowser.open(url)
            self.action_hint.set('已尝试打开注册页；如果浏览器仍打不开，说明服务端注册站点当前异常。')
        except Exception as e:
            LOGGER.exception('open register failed: %s', e)
            messagebox.showerror('打开失败', f'无法打开注册链接：\n{e}')

    def launch_game(self):
        if not self.validate_client_path(show_popup=False):
            LOGGER.warning('launch aborted: invalid client path')
            messagebox.showerror('启动失败', '未找到有效客户端目录，请先修正路径。')
            return
        wow_exe = self.get_wow_exe()
        try:
            self.persist_state()
            written = self.write_realmlist(wow_exe.parent)
            subprocess.Popen([str(wow_exe)], cwd=str(wow_exe.parent), shell=False)
            LOGGER.info('game launched: %s', wow_exe)
            self.action_hint.set('已写入 realmlist 并尝试启动游戏。现在请看客户端是否成功连服。')
            messagebox.showinfo('启动成功', f'已写入:\n{written}\n\n并尝试启动:\n{wow_exe.name}')
        except Exception as e:
            LOGGER.exception('launch failed: %s', e)
            messagebox.showerror('启动失败', str(e))

    def refresh_status_async(self):
        threading.Thread(target=self.refresh_status, daemon=True).start()

    def refresh_status(self):
        url = self.config.get('status_url', '').strip()
        if not url:
            self.root.after(0, lambda: self.status_text.set('未配置状态接口'))
            return
        try:
            resp = requests.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            world = data.get('services', {}).get('worldserver', {}).get('running')
            auth = data.get('services', {}).get('authserver', {}).get('running')
            summary = f"world={'在线' if world else '离线'} / auth={'在线' if auth else '离线'}"
            self.root.after(0, lambda: self.server_text.set(summary))
            self.root.after(0, lambda: self.status_text.set('已连接服务器状态接口'))
            LOGGER.info('status refreshed: %s', summary)
        except Exception as e:
            LOGGER.exception('status refresh failed: %s', e)
            self.root.after(0, lambda: self.status_text.set(f'状态接口失败: {e}'))


def main():
    setup_logging()
    LOGGER.info('python=%s', sys.version.replace('\n', ' '))
    root = tk.Tk()
    LauncherApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
