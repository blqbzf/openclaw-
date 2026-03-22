# 自动更新问题排查指南

## 🔍 问题现象
启动登录器后：
1. ✅ 反外挂弹窗还在出现
2. ❌ 没有自动更新补丁

---

## 📋 排查步骤

### 1️⃣ 确认版本

**下载最新版本：**
```
https://github.com/blqbzf/openclaw-/releases/tag/v3.2.3

版本历史：
- v3.2.0：有反外挂弹窗问题
- v3.2.1：半透明背景
- v3.2.2：修复反外挂 + 适配manifest.json
- v3.2.3：调试版本（推荐）✨
```

---

### 2️⃣ 使用调试模式

**Windows用户：**
1. 下载 `NolanWoWLauncher-Windows.zip`
2. 解压后，双击 `debug_launcher.bat`
3. 黑窗口会显示调试信息
4. 复制调试信息发给我

**Mac用户：**
```bash
cd /Applications/诺兰时光魔兽登录器.app/Contents/MacOS
./诺兰时光魔兽登录器
```

---

### 3️⃣ 检查客户端路径

**必须设置WoW路径：**
```
1. 启动登录器
2. 点击"浏览"按钮
3. 选择WoW客户端目录（包含Wow.exe的文件夹）
4. 点击"进入艾泽拉斯"
5. 重启登录器
```

**示例路径：**
```
D:\WoW\3.3.5a
C:\Games\World of Warcraft
E:\WoW\WotLK
```

---

### 4️⃣ 测试补丁服务器

**在浏览器访问：**
```
http://1.14.59.54:8080/patches/manifest.json
```

**应该看到：**
```json
{
  "system_version": "1.2.0",
  "last_updated": "2026-03-23 04:21",
  "patches": [...]
}
```

**如果看不到：**
- 补丁服务器未启动
- 联系鸽子命检查

---

## 🔧 常见问题

### 问题1：客户端路径为空
```
现象：启动后不检查更新
原因：代码检测到路径为空，跳过更新
解决：设置WoW客户端路径
```

### 问题2：manifest.json访问失败
```
现象：调试日志显示HTTP 502
原因：补丁服务器未运行
解决：联系鸽子命启动服务器
```

### 问题3：反外挂弹窗还在
```
现象：检测通过还弹窗
原因：使用的是旧版本
解决：下载v3.2.3最新版
```

---

## 📊 调试日志示例

**正常流程：**
```
[DEBUG] 检查更新 - 客户端路径: D:\WoW\3.3.5a
[DEBUG] 正在获取: http://1.14.59.54:8080/patches/manifest.json
[DEBUG] 响应状态: 200
[DEBUG] 成功获取manifest: {...}
[DEBUG] 开始检查更新...
[DEBUG] manifest: {...}
[DEBUG] needed_patches: [...]
[DEBUG] 发现新补丁:
• patch-ZP3.MPQ v1.0.0
```

**异常流程：**
```
[DEBUG] 客户端路径为空，跳过更新检查
```

---

## 📞 需要帮助？

**提供以下信息：**
1. ✅ 使用的版本号
2. ✅ 调试窗口的完整输出
3. ✅ 客户端路径是否设置
4. ✅ manifest.json能否在浏览器打开

---

**下载调试版本：**
https://github.com/blqbzf/openclaw-/releases/tag/v3.2.3
