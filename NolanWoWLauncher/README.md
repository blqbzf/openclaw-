# 诺兰时光 WoW 登录器 (C# Avalonia 版本)

## 技术栈
- **C# + .NET 8.0** - 跨平台框架
- **Avalonia UI 11.0** - XAML 跨平台 UI 框架
- **MVVM** - CommunityToolkit.Mvvm
- **Newtonsoft.Json** - JSON 序列化

## 功能特性

### ✅ 核心功能
1. **客户端目录选择** - 自动验证客户端完整性
2. **realmlist 修复** - 一键修复服务器地址
3. **账号注册** - 在登录器内直接注册账号
4. **清除缓存** - 删除 Cache/WDB 等目录
5. **检查更新** - 从服务端获取补丁清单
6. **补丁安装** - 自动下载并安装缺失补丁
7. **进度显示** - 实时显示下载进度
8. **服务器更新信息** - 显示最新更新内容

## 使用方法

### 首次使用
1. 选择客户端目录（WoW 3.3.5a）
2. 点击"注册账号"创建账号
3. 点击"检查更新"下载必要补丁
4. 点击"启动游戏"进入游戏

### 日常使用
1. 启动登录器
2. 点击"启动游戏"

## 项目结构
```
NolanWoWLauncher/
├── App.axaml                 # 应用主配置
├── App.axaml.cs             # 应用启动类
├── Program.cs                # 程序入口
├── Assets/
│   ├── background.jpg        # 背景图片
│   └── icon.ico              # 应用图标
├── Views/
│   ├── MainWindow.axaml      # 主窗口 UI
│   ├── MainWindow.axaml.cs   # 主窗口后台
│   ├── RegisterDialog.axaml  # 注册对话框 UI
│   └── RegisterDialog.axaml.cs # 注册对话框后台
├── ViewModels/
│   └── MainViewModel.cs      # 主视图模型（MVVM）
├── Services/
│   ├── ClientService.cs      # 客户端服务（验证、启动等）
│   ├── AccountService.cs     # 账号服务（注册）
│   └── PatchService.cs        # 补丁服务（下载、校验）
└── NolanWoWLauncher.csproj   # 项目配置
```

## 构建说明

### 开发环境要求
- .NET 8.0 SDK
- Visual Studio 2022 / Rider / VS Code
- Windows 10/11

### 构建步骤
```bash
# 还原依赖
dotnet restore

# 调试构建
dotnet build

# 发布单文件可执行程序
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

### 输出位置
```
bin/Release/net8.0-windows/publish/NolanWoWLauncher.exe
```

## 服务器配置

### API 端点
- `GET /api/patches/manifest` - 获取补丁清单
- `POST /api/register` - 注册账号
- `GET /api/updates` - 获取服务器更新信息

### manifest.json 格式
```json
[
  {
    "name": "patch-nolan.MPQ",
    "version": "1.0.0",
    "size": 15728640,
    "sha256": "abc123...",
    "downloadUrl": "http://1.14.59.54:8080/files/patch-nolan.MPQ",
    "required": true
  }
]
```

### 更新信息格式
```json
{
  "date": "2026-03-28",
  "updates": [
    "修复了 ICC 副本 BOSS 技能",
    "新增 50 个自定义 NPC",
    "优化了服务器性能"
  ]
}
```

## 优势对比

### vs Python + Tkinter
- ✅ 原生 Windows UI，更流畅
- ✅ 单文件部署，无需 Python 环境
- ✅ 更好的性能和稳定性
- ❌ 体积稍大（约 80MB）

### vs Electron
- ✅ 体积极小（80MB vs 150MB+）
- ✅ 启动更快
- ✅ 内存占用更低
- ✅ 原生 UI 性能

## 已知问题
- 需要自签名证书避免杀毒软件拦截
- 暂不支持 macOS/Linux（可扩展）

## 开发者信息
- **开发者:** 鸽子命 (OpenClaw Agent)
- **GitHub:** https://github.com/blqbzf/openclaw-
- **版本:** 1.0.0
- **发布日期:** 2026-03-28
