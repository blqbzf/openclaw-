# P1时光WoW私服登录器 - 完整部署指南

## 🎯 项目概述

这是一个完整的WoW 3.3.5a私服登录器解决方案，包括：
- ✅ Windows可执行文件（.exe）
- ✅ 自动修改realmlist.wtf
- ✅ 一键启动游戏
- ✅ 服务器状态显示
- ✅ 新闻公告系统
- ✅ 自定义配置

## 📦 文件清单

```
wow_launcher/
├── wow_launcher.py          # 主程序源码（17KB）
├── build_exe.py             # 打包脚本（3KB）
├── build_windows.bat        # Windows打包批处理
├── build_mac.sh             # Mac打包脚本
├── server_api.py            # 服务器API示例（可选）
├── requirements.txt         # Python依赖
├── launcher_config.json     # 配置文件（479B）
├── README.md                # 完整文档（3.5KB）
└── DEPLOYMENT.md            # 本文件
```

## 🚀 三种部署方式

### 方式1：直接使用（推荐）⭐⭐⭐⭐⭐

**适合：** 不想折腾的玩家

**步骤：**
```bash
1. 下载 dist/P1时光WoW登录器.exe
2. 双击运行
3. 设置WoW客户端路径
4. 点击"启动游戏"
```

**优点：** 无需任何技术知识
**缺点：** 需要等待我打包好

---

### 方式2：自行编译（开发者）

**适合：** 有Python基础的开发者

**Windows系统：**
```bash
# 1. 确保已安装Python 3.8+
python --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行打包脚本
build_windows.bat

# 4. 生成的exe在 dist/ 目录
```

**Mac/Linux系统：**
```bash
# 1. 确保已安装Python 3.8+
python3 --version

# 2. 给脚本执行权限
chmod +x build_mac.sh

# 3. 运行打包脚本
./build_mac.sh

# 4. 生成的exe在 dist/ 目录
```

**优点：** 完全自定义
**缺点：** 需要技术知识

---

### 方式3：修改源码后编译

**适合：** 需要自定义功能

**步骤：**
```bash
# 1. 编辑 wow_launcher.py
# 2. 修改界面、颜色、功能等
# 3. 编辑 launcher_config.json
# 4. 执行打包脚本
python build_exe.py
```

**常见自定义：**
- 修改服务器名称/IP
- 修改界面颜色
- 添加新功能（如自动更新）
- 添加背景音乐
- 添加图片Banner

## 🎨 自定义开发指南

### 修改界面颜色

编辑 `wow_launcher.py`，找到以下部分：

```python
# 顶部背景色
logo_frame = tk.Frame(self.root, bg="#1a1a2e")  # 深蓝色

# 启动按钮颜色
self.launch_btn = tk.Button(
    bg="#4CAF50",  # 绿色背景
    fg="white",     # 白色文字
    ...
)
```

### 添加背景图片

```python
# 在 __init__ 方法中添加：
from PIL import Image, ImageTk

# 加载背景图
bg_image = Image.open("background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(self.root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo  # 保持引用
```

### 添加自动更新功能

```python
def check_update(self):
    """检查登录器更新"""
    try:
        response = requests.get("http://1.14.59.54/launcher/version.json")
        latest_version = response.json()["version"]
        
        if latest_version > self.config["version"]:
            messagebox.showinfo("更新", "发现新版本！正在下载...")
            # 下载并替换exe
    except:
        pass
```

### 添加在线人数实时显示

需要服务器端API支持（`server_api.py`）：

```python
def update_player_count(self):
    """更新在线人数"""
    try:
        response = requests.get("http://1.14.59.54/api/online")
        players = response.json()["online"]
        self.players_label.config(text=f"{players} 人在线")
        
        # 每60秒更新一次
        self.root.after(60000, self.update_player_count)
    except:
        self.players_label.config(text="无法获取")
```

## 🌐 服务器端部署

### 部署状态API（可选）

如果需要实时显示在线人数：

```bash
# 在服务器上运行
cd wow_launcher
pip install flask flask-cors
python server_api.py

# 或使用生产服务器
gunicorn -w 4 -b 0.0.0.0:8080 server_api:app
```

### 集成到AzerothCore

在AzerothCore的worldserver.conf中添加：

```
# 启用REST API
RestAPI.Enable = 1
RestIP = 0.0.0.0
RestPort = 8080
```

然后在 `wow_launcher.py` 中修改：

```python
def update_player_count(self):
    """从AzerothCore API获取在线人数"""
    try:
        response = requests.get("http://1.14.59.54:8080/online")
        players = response.json()["playerCount"]
        self.players_label.config(text=f"{players} 人在线")
    except:
        pass
```

## 📊 参考的优秀案例

### 1. AscEmu Launcher
- **GitHub:** https://github.com/AscEmu/Launcher
- **特色:** 现代化UI，自动更新，补丁下载
- **技术栈:** C# + WPF

### 2. TrinityCore Windows Launcher
- **特色:** 轻量级，支持多服务器
- **技术栈:** Python + Tkinter

### 3. AzerothCore 官方推荐
- **Wiki:** https://www.azerothcore.org/wiki/
- **多种方案:** C#, Python, Electron等

### 4. Hellground Launcher
- **特色:** 经典设计，稳定可靠
- **技术栈:** C++ + Qt

## 🔧 常见问题解决

### Q1: PyInstaller打包后体积太大？
**A:** 使用UPX压缩：
```bash
pip install pyinstaller
pyinstaller --onefile --upx-dir=/path/to/upx wow_launcher.py
```

### Q2: 打包后被杀毒软件误报？
**A:** 
1. 使用代码签名证书（付费）
2. 或上传到VirusTotal申请白名单
3. 提示用户添加信任

### Q3: 在Mac上打包Windows exe？
**A:** PyInstaller不支持跨平台打包，解决方案：
1. 使用GitHub Actions自动化打包
2. 使用虚拟机或Docker
3. 借用Windows电脑打包

### Q4: 想要更漂亮的UI？
**A:** 
1. 使用PyQt5代替Tkinter
2. 使用Electron（JavaScript）
3. 使用C# + WPF（Windows原生）

## 📝 下一步计划

### v1.1 版本（未来）
- [ ] 添加背景图片支持
- [ ] 添加补丁自动下载
- [ ] 添加登录器自动更新
- [ ] 添加多服务器支持
- [ ] 添加游戏截图功能
- [ ] 添加Discord Rich Presence

### v2.0 版本（长期）
- [ ] 重写为Electron版本
- [ ] 添加社区功能（聊天、好友）
- [ ] 添加成就系统
- [ ] 添加游戏内置浏览器

## 📞 技术支持

### 遇到问题？

1. **查看文档:** `README.md`
2. **查看日志:** `launcher.log`
3. **提交Issue:** GitHub Issues
4. **联系管理员:** support@p1wow.com

### 有改进建议？

欢迎提交Pull Request或建议！

## 📄 许可证

MIT License - 可自由使用、修改、分发

---

**感谢使用P1时光WoW登录器！** 🎮

**祝游戏愉快！** ⚔️
