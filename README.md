# P1时光WoW私服登录器

## 📋 功能特性

- ✅ 自动修改realmlist.wtf
- ✅ 一键启动游戏
- ✅ 服务器状态显示
- ✅ 在线人数统计（需要API支持）
- ✅ 新闻/公告系统
- ✅ 账号注册链接
- ✅ 官网链接
- ✅ 自定义配置

## 🚀 快速开始

### 方式1：直接使用（推荐）

1. 下载 `dist/P1时光WoW登录器.exe`
2. 双击运行
3. 首次运行时设置WoW客户端路径
4. 点击"启动游戏"

### 方式2：从源码编译

#### Windows系统：

```bash
# 1. 安装Python 3.8+
python --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 打包成exe
python build_exe.py

# 4. 生成的exe在 dist/ 目录
```

#### Mac/Linux系统：

```bash
# 1. 安装Python 3.8+
python3 --version

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 运行（开发模式）
python3 wow_launcher.py

# 注意：Mac/Linux不支持exe格式
```

## ⚙️ 配置说明

### launcher_config.json 配置文件：

```json
{
  "server_name": "P1时光WoW",
  "server_ip": "1.14.59.54",
  "realmlist": "set realmlist 1.14.59.54",
  "register_url": "http://1.14.59.54/register",
  "website_url": "http://1.14.59.54",
  "discord_url": "",
  "version": "3.3.5a"
}
```

### 自定义配置：

1. 修改 `launcher_config.json`
2. 重启登录器即可生效

## 📁 文件结构

```
wow_launcher/
├── wow_launcher.py          # 主程序源码
├── build_exe.py             # 打包脚本
├── build_windows.bat        # Windows打包批处理
├── requirements.txt         # Python依赖
├── README.md                # 说明文档
├── icon.ico                 # 程序图标（可选）
└── dist/                    # 生成的exe目录
    ├── P1时光WoW登录器.exe
    └── launcher_config.json
```

## 🎨 自定义开发

### 修改界面颜色：

在 `wow_launcher.py` 中修改：

```python
# 顶部背景色
logo_frame = tk.Frame(self.root, bg="#1a1a2e")

# 按钮颜色
self.launch_btn = tk.Button(
    bg="#4CAF50",  # 背景色
    fg="white",     # 文字色
    ...
)
```

### 添加新功能：

```python
def check_server_status(self):
    """检查服务器状态"""
    # 实现在线人数API调用
    # 示例：
    # response = requests.get("http://1.14.59.54/api/online")
    # players = response.json()["online"]
    # self.players_label.config(text=f"{players} 人在线")
    pass
```

## 📊 优秀案例参考

### 1. AscEmu Launcher
- GitHub: https://github.com/AscEmu/Launcher
- 特点：现代化UI，自动更新

### 2. TrinityCore Launcher
- 特点：简洁实用，多服务器支持

### 3. AzerothCore 官方推荐
- 官方Wiki: https://www.azerothcore.org/wiki/
- 多种登录器方案

## ⚠️ 注意事项

1. **客户端版本**：确保使用3.3.5a客户端
2. **防火墙**：首次运行可能需要允许防火墙
3. **杀毒软件**：部分杀毒软件可能误报，添加信任即可
4. **管理员权限**：建议以管理员身份运行

## 🐛 常见问题

### Q1: 启动后提示找不到Wow.exe？
**A:** 检查客户端路径是否正确，确保路径下有 `Wow.exe`

### Q2: 启动后闪退？
**A:** 检查是否以管理员身份运行，或查看 `launcher.log` 日志

### Q3: 无法修改realmlist.wtf？
**A:** 确保WoW客户端目录有写入权限

## 📝 更新日志

### v1.0 (2026-03-22)
- ✅ 初始版本发布
- ✅ 基础登录器功能
- ✅ 自动修改realmlist
- ✅ 一键启动游戏

## 📞 技术支持

- GitHub Issues: [提交问题]
- 邮箱: support@p1wow.com
- Discord: [加入Discord]

## 📄 许可证

MIT License

Copyright (c) 2026 P1时光WoW

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
