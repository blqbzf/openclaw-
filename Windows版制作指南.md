# P1时光WoW登录器 - Windows版制作指南

## 🎯 目标

制作Windows版登录器，关联云服务器 1.14.59.54

---

## 🚀 三种制作方案

### **方案1：使用GitHub Actions（全自动，推荐）⭐⭐⭐⭐⭐**

**适合：有GitHub账号**

**步骤：**

1. **创建GitHub仓库**
   ```bash
   cd /Users/mac/Documents/bobo/boboai/test_1_openclaw/wow_launcher
   git init
   git add .
   git commit -m "feat: P1时光WoW登录器"
   git branch -M main
   git remote add origin https://github.com/你的用户名/p1-wow-launcher.git
   git push -u origin main
   ```

2. **创建发布版本**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **自动打包**
   - GitHub Actions自动运行
   - 生成Windows exe + Mac app
   - 下载地址：Actions → Artifacts

4. **下载exe**
   - 访问仓库 → Actions
   - 下载 `windows-launcher`
   - 解压即用

**优点：**
- ✅ 全自动，无需Windows电脑
- ✅ 同时生成Windows + Mac版
- ✅ 版本管理清晰

**缺点：**
- ⚠️ 需要GitHub账号
- ⚠️ 首次配置需要5分钟

**耗时：** 5-10分钟（首次）

---

### **方案2：在Windows电脑上打包（手动）⭐⭐⭐⭐**

**适合：有Windows电脑**

**步骤：**

1. **复制文件到Windows**
   - 整个 `wow_launcher` 目录复制到Windows

2. **安装Python**
   - 下载：https://www.python.org/downloads/
   - 版本：Python 3.9
   - 安装时勾选 "Add Python to PATH"

3. **运行打包脚本**
   ```cmd
   cd wow_launcher
   build_windows_complete.bat
   ```

4. **获取exe**
   - 位置：`dist\发布包\P1时光WoW登录器.exe`

**优点：**
- ✅ 完全本地，不依赖网络
- ✅ 可以自定义修改

**缺点：**
- ⚠️ 需要Windows电脑
- ⚠️ 需要安装Python

**耗时：** 10-15分钟

---

### **方案3：使用Docker（适合开发者）⭐⭐⭐**

**适合：有Docker经验**

**步骤：**

1. **使用Docker打包Windows版**
   ```bash
   docker run --rm -v "$(pwd):/src/" cdrx/pyinstaller-windows
   ```

2. **获取exe**
   - 位置：`dist/P1时光WoW登录器.exe`

**优点：**
- ✅ 不需要Windows电脑

**缺点：**
- ⚠️ 需要Docker环境
- ⚠️ 打包速度较慢

**耗时：** 15-20分钟

---

## 📋 推荐流程（最快）

### **如果现在就要：**

1. **在Mac上测试Python代码**（2分钟）
   ```bash
   cd /Users/mac/Documents/bobo/boboai/test_1_openclaw/wow_launcher
   python3 wow_launcher.py
   ```

2. **确认功能正常后，选择打包方式：**
   - 有GitHub → **方案1**（推荐）
   - 有Windows → **方案2**
   - 都没有 → 找朋友帮忙

3. **分发exe给玩家**

---

## 🔧 当前配置（已更新）

**服务器信息：**
```
服务器IP: 1.14.59.54
登录端口: 3724
游戏端口: 8085
注册地址: http://1.14.59.54:5000
```

**配置文件：** `launcher_config.json`

---

## 📂 文件位置

```
/Users/mac/Documents/bobo/boboai/test_1_openclaw/wow_launcher/

关键文件：
├── wow_launcher.py              # 主程序（17KB）
├── launcher_config.json         # 配置文件（587B，已更新IP）
├── .github/workflows/build.yml  # GitHub Actions配置（2.7KB）
├── build_windows_complete.bat   # Windows打包脚本（3.3KB）
└── register.html                # 注册网页（13KB）
```

---

## ⚡ 快速决策

**波哥，你现在：**

1. **有GitHub账号？**
   - ✅ → 用方案1（GitHub Actions）
   - ❌ → 继续下一个问题

2. **有Windows电脑？**
   - ✅ → 用方案2（Windows本地打包）
   - ❌ → 用方案3（Docker）或找朋友帮忙

3. **或者我可以帮你：**
   - 我帮你创建GitHub仓库并上传
   - 你只需要点一下创建tag
   - 5分钟后自动下载exe

---

**告诉我你选择哪个方案，我立即协助！** 🚀
