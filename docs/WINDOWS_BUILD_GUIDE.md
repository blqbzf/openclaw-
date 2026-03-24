# 诺兰时光魔兽登录器 - Windows版本制作指南

**创建时间**: 2026-03-24
**版本**: v3.3.0

---

## ⚠️ 重要说明

**Windows版本的.exe文件必须在Windows系统上打包！**

原因：
- Mac无法生成Windows .exe可执行文件
- PyInstaller不支持跨平台打包
- Windows可执行文件格式与Mac不同

---

## 🎯 两种方案

### 方案1: 在Windows电脑上打包（推荐）

#### 准备工作

```
1. 准备一台Windows电脑（Windows 7/8/10/11）
2. 安装Python 3.8+ (https://www.python.org/downloads/)
3. 下载项目代码
```

#### 操作步骤

```
1. 下载项目代码
   git clone https://github.com/blqbzf/openclaw-
   cd openclaw-/wow_launcher

2. 运行打包脚本
   双击运行: build_windows_complete.bat

3. 等待打包完成（1-2分钟）
   输出位置: dist\发布包\

4. 测试运行
   双击: dist\发布包\P1时光WoW登录器.exe

5. 打包分发
   将 "发布包" 文件夹压缩成ZIP
```

---

### 方案2: 使用GitHub Actions自动构建（推荐）

#### 配置GitHub Actions

项目已包含 `.github/workflows/build.yml`，推送代码后会自动构建！

#### 使用方法

```bash
# 1. 提交代码
cd /Users/mac/Documents/bobo/boboai/test_1_openclaw/wow_launcher
git add .
git commit -m "feat: 准备发布v3.3.0"
git push origin HEAD:launcher-v1

# 2. 创建tag触发构建
git tag v3.3.0
git push origin v3.3.0

# 3. 等待自动构建（约5分钟）
# 访问: https://github.com/blqbzf/openclaw-/actions

# 4. 下载构建产物
# 访问: https://github.com/blqbzf/openclaw-/releases
```

---

## 📦 Windows版本文件清单

### 发布包内容

```
诺兰时光魔兽登录器-Windows-v3.3.0.zip
├── P1时光WoW登录器.exe (约10-15 MB)
├── launcher_config.json
├── background.jpg (可选)
├── 使用说明.txt
└── realmlist备份说明.txt
```

### 配置文件 (launcher_config.json)

```json
{
  "server_name": "诺兰时光魔兽",
  "server_ip": "1.14.59.54",
  "realmlist": "set realmlist 1.14.59.54",
  "client_path": "",
  "register_url": "http://1.14.59.54:5000",
  "website_url": "http://1.14.59.54",
  "discord_url": "",
  "patch_url": "http://1.14.59.54:8080/patches",
  "version": "3.3.5a",
  "game_version": "3.3.5a (12340)",
  "news": "欢迎来到诺兰时光魔兽！",
  "status_api": "http://1.14.59.54:5000/api/online"
}
```

---

## 🔧 手动打包步骤（Windows系统）

### 1. 安装依赖

```cmd
pip install pyinstaller pillow psutil requests
```

### 2. 执行打包命令

```cmd
pyinstaller --clean --noconfirm ^
    --onefile ^
    --windowed ^
    --name "P1时光WoW登录器" ^
    --add-data "launcher_config.json;." ^
    --hidden-import=PIL._tkinter_finder ^
    wow_launcher.py
```

### 3. 创建发布包

```cmd
mkdir dist\发布包
copy dist\P1时光WoW登录器.exe dist\发布包\
copy launcher_config.json dist\发布包\
copy background.jpg dist\发布包\
```

### 4. 压缩分发

```cmd
# 使用7-Zip或WinRAR压缩
# 或使用PowerShell:
Compress-Archive -Path dist\发布包 -DestinationPath 诺兰时光魔兽登录器-Windows-v3.3.0.zip
```

---

## 📥 下载地址设置

### 选项1: GitHub Releases（推荐）

```
1. 推送代码到GitHub
2. 创建Release
3. 上传Windows ZIP文件
4. 玩家下载链接:
   https://github.com/blqbzf/openclaw-/releases/download/v3.3.0/诺兰时光魔兽登录器-Windows-v3.3.0.zip
```

### 选项2: 服务器直接下载

```bash
# 在服务器上操作
ssh root@1.14.59.54

# 创建下载目录
mkdir -p /var/www/html/downloads

# 上传Windows ZIP文件
# (从Windows电脑上传)
scp 诺兰时光魔兽登录器-Windows-v3.3.0.zip root@1.14.59.54:/var/www/html/downloads/

# 玩家下载链接
http://1.14.59.54/downloads/诺兰时光魔兽登录器-Windows-v3.3.0.zip
```

### 选项3: 网盘分享

```
上传到网盘服务:
- 百度网盘
- 蓝奏云
- Google Drive
- OneDrive

获取分享链接后发给玩家
```

---

## ✅ 验证清单

### 打包前检查

```
□ Python版本 >= 3.8
□ 已安装pyinstaller
□ 已安装pillow, psutil, requests
□ launcher_config.json配置正确
□ background.jpg存在（可选）
□ wow_launcher.py代码已更新
```

### 打包后检查

```
□ .exe文件已生成
□ 文件大小10-15MB
□ 双击可运行
□ 配置文件已包含
□ 无明显错误提示
```

### 发布前检查

```
□ 在干净的Windows系统测试
□ 能正常启动
□ 能检测WoW客户端
□ 能下载补丁
□ 能启动游戏
□ 杀毒软件测试（可能误报）
```

---

## 🎯 快速方案推荐

### 最快方案: GitHub Actions自动构建

```
1. 提交代码
2. 创建tag
3. 等待自动构建
4. 下载构建产物
5. 发布到玩家

优点:
✅ 无需Windows电脑
✅ 自动化构建
✅ 可靠稳定
✅ 版本管理清晰
```

---

## 📝 当前状态

### 已完成

```
✅ Mac版本已打包 (12MB)
✅ 补丁系统已验证
✅ 服务器配置正常
✅ 文档已完善
```

### 待完成

```
⏳ Windows版本打包
⏳ GitHub Release发布
⏳ 玩家下载页面
```

---

## 💬 建议

**由于你在Mac上，推荐使用GitHub Actions自动构建Windows版本！**

步骤：
1. 提交当前代码到GitHub
2. 创建v3.3.0 tag
3. 等待自动构建（5分钟）
4. 下载Windows版本
5. 发布给玩家

---

**需要我帮你准备GitHub Actions配置吗？** 😊
