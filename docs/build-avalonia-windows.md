# Avalonia Windows 构建文档

## 构建方式

### 方式 1: GitHub Actions 自动构建（推荐）

#### 触发构建
- Push 到 `main` 或 `feat/wow-launcher` 分支
- 手动触发 (workflow_dispatch)

#### 下载构建产物
1. 进入 **Actions** 页面
2. 选择 "Build Windows Launcher (Avalonia)"
3. 选择最新的成功构建记录
4. 滚动到底部 **Artifacts** 区域
5. 点击 `NolanWoWLauncher-Windows-x64` 下载

#### 构建时间
- 首次构建: ~5-8 分钟
- 后续构建: ~3-5 分钟（有缓存）

---

### 方式 2: 本地构建

#### 前置要求
- Windows 10/11
- .NET 8.0 SDK
- Visual Studio 2022 / Rider / VS Code

#### 构建命令
```bash
cd NolanWoWLauncher
dotnet restore
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

#### 输出位置
```
NolanWoWLauncher/bin/Release/net8.0-windows/win-x64/publish/NolanWoWLauncher.exe
```

---

## 构建类型说明

### Self-Contained (当前默认)
- **定义**: 包含 .NET Runtime，无需预先安装 .NET
- **大小**: ~80MB
- **优势**: 用户无需安装任何依赖，直接运行
- **劣势**: 体积较大

### Framework-Dependent (可选)
- **定义**: 依赖系统安装的 .NET Runtime
- **大小**: ~5-10MB
- **优势**: 体积小
- **劣势**: 用户需要先安装 .NET 8 Runtime

---

## 当前默认交付

**Self-Contained 单文件版**

- ✅ 包含 .NET Runtime
- ✅ 单个可执行文件
- ✅ 无需安装依赖
- ✅ 便携式，解压即用

**构建参数:**
```bash
-r win-x64                          # 目标平台
--self-contained true                # 包含 Runtime
-p:PublishSingleFile=true            # 单文件
-p:IncludeNativeLibrariesForSelfExtract=true  # 包含原生库
-p:PublishTrimmed=true               # 裁剪未使用的代码（减小体积）
```

---

## Artifact 内容

**NolanWoWLauncher-Windows-x64.zip**
- `NolanWoWLauncher.exe` (~80MB)
- `Assets/background.jpg` (背景图片，嵌入到 exe 中)

---

## 故障排除

### 构建失败
1. 检查 .NET SDK 版本（必须是 8.0.x）
2. 查看 Actions 日志
3. 确认代码无语法错误

### 下载失败
1. 检查构建是否成功
2. 检查 artifact 保留时间（30天）
3. 重新触发构建

### exe 无法运行
1. 检查 Windows Defender 是否拦截
2. 添加到杀毒软件白名单
3. 使用自签名证书（见 `docs/signing-notes.md`）

---

## 未来改进

- [ ] 添加代码签名
- [ ] 提供 Framework-Dependent 版本
- [ ] 添加自动更新功能
- [ ] 支持 Linux/macOS
