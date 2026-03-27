# Windows 打包说明

## 本地打包

### 前置要求
- Node.js 18.x
- npm 9.x
- Windows 10+ 或 Linux/macOS (通过 Wine)

### 构建步骤

#### 1. 安装依赖
```bash
cd launcher-win
npm install
```

#### 2. 构建前端
```bash
npm run build:frontend
```

#### 3. 打包 Windows 可执行文件
```bash
npm run build:win
```

### 输出目录
构建产物会输出到 `dist/` 目录:
```
launcher-win/
└── dist/
    ├── win-unpacked/
    │   ├── NolanWoWLauncher.exe
    │   ├── resources/
    │   └── ...
    └── NolanWoWLauncher Setup 1.0.0.exe
```

- `win-unpacked/` - 未打包的应用目录
- `NolanWoWLauncher Setup 1.0.0.exe` - NSIS 安装程序

### 本地构建要求
- **Windows**: 直接构建
- **Linux/macOS**: 需要安装 Wine

## GitHub Actions 构建

### 自动触发条件
- Push 到 `main` 分支
- 手动触发

### 手动触发
1. 访问 Actions 页面
2. 选择 "Build Windows Launcher"
3. 点击 "Run workflow"

### 下载构建产物
1. 进入 Actions → 选择对应的 workflow 运行记录
2. 滚动到底部 "Artifacts" 区域
3. 点击 `NolanWoWLauncher-Windows` 下载

### 构建时间
- 首次构建: ~10-15 分钟
- 后续构建: ~5-8 分钟

## 为什么源码仓库不包含构建产物？

1. **文件过大** - 可执行文件通常 > 50MB
2. **二进制文件** - 不适合版本控制
3. **自动生成** - 每次构建都不同
4. **CI/CD 最佳实践** - 通过 GitHub Actions 分发

## 构建配置

### electron-builder 配置
文件: `electron-builder.yml`

关键配置:
- **appId**: `com.nolanwow.launcher`
- **productName**: `诺兰时光WoW登录器`
- **target**: NSIS 安装程序
- **arch**: x64

### NSIS 安装选项
- 允许用户选择安装目录
- 创建桌面快捷方式
- 创建开始菜单快捷方式
- 卸载时删除应用数据

## 构建产物说明

### NolanWoWLauncher.exe
- 主可执行文件
- 包含完整的 Electron + React 应用
- 文件大小: ~60-80MB (未压缩)

### Setup.exe
- NSIS 安装程序
- 包含完整应用 + 安装向导
- 文件大小: ~50-60MB (已压缩)

## 分发方式

### 方式 1: GitHub Release
```bash
# 自动上传到 GitHub Release
electron-builder --publish always
```

### 方式 2: 手动分发
```bash
# 只生成构建产物，不上传
electron-builder --publish never
```

### 方式 3: GitHub Artifacts
通过 GitHub Actions 自动生成，保留 30 天

## 故障排除

### 构建失败
1. 检查 Node.js 版本 (必须是 18.x)
2. 检查依赖是否完整安装
3. 查看 GitHub Actions 日志

### 产物无法运行
1. 检查 Windows Defender 是否阻止
2. 检查杀毒软件是否拦截
3. 使用自签名证书签名可执行文件

### 构建产物过大
1. 检查是否包含不必要的 node_modules
2. 启用 asar 打包
3. 使用 electron-builder 的文件过滤功能

## 下一步: 添加代码签名

内测版可以使用自签名证书:
1. 生成自签名证书 (见 `signing/README.md`)
2. 配置 electron-builder 签名选项
3. 重新构建产物

---

**构建产物不会提交到 Git 仓库，只通过 GitHub Release 或 Artifacts 分发。**
