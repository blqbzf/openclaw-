# Windows 构建和打包流程

## 构建策略

**当前模式:** 只构建，不自动发布

- ✅ 生成 Windows 构建产物
- ✅ 通过 GitHub Actions Artifacts 分发
- ❌ 暂不启用自动 GitHub Release

## 本地构建

### 1. 安装依赖
```bash
cd launcher-win
npm ci
```

### 2. 构建产物
```bash
npm run build:win
```

### 3. 输出位置
```
launcher-win/dist/
├── win-unpacked/
│   ├── NolanWoWLauncher.exe
│   ├── resources/
│   └── ...
├── NolanWoWLauncher Setup 1.0.0.exe
├── NolanWoWLauncher Setup 1.0.0.exe.blockmap
└── builder-effective-config.yaml
```

**重要文件:**
- `NolanWoWLauncher Setup 1.0.0.exe` - NSIS 安装程序 (约50-60MB)
- `win-unpacked/` - 未打包的应用目录

## GitHub Actions 构建

### 自动触发
- Push 到 `main` 或 `feat/wow-launcher` 分支
- 手动触发（workflow_dispatch）

### 下载构建产物

#### 方法 1: 通过 Actions 页面
1. 访问 https://github.com/blqbzf/openclaw-/actions
2. 选择最新的 "Build Windows Launcher" 运行记录
3. 滚动到底部 "Artifacts" 区域
4. 点击 `NolanWoWLauncher-Windows` 下载

#### 方法 2: 通过 API
```bash
gh run download --repo blqbzf/openclaw- --name NolanWoWLauncher-Windows
```

### 构建产物内容
- `NolanWoWLauncher Setup 1.0.0.exe` - 安装程序
- `*.blockmap` - 增量更新文件
- `*.yml` - 构建配置

### 构建时间
- 首次构建: ~8-12 分钟
- 后续构建: ~5-7 分钟（有缓存）

### Artifact 保留时间
- 默认保留: 30 天
- 可手动延长

## 为什么不自动发布 Release？

1. **安全性** - 需要审核构建产物
2. **灵活性** - 可以在发布前测试
3. **控制权** - 管理员决定何时发布
4. **版本管理** - 避免自动生成过多版本

## 手动发布 Release

如果需要发布正式版本:

```bash
# 1. 下载构建产物
gh run download --name NolanWoWLauncher-Windows

# 2. 创建 Release
gh release create v1.0.0 \
  --title "v1.0.0 - 诺兰时光WoW登录器" \
  --notes "## 更新内容

- 全新登录器
- 自动补丁更新
- 缓存清理
- 客户端扫描

## 下载

- Windows: NolanWoWLauncher Setup 1.0.0.exe" \
  NolanWoWLauncher*.exe
```

## 构建配置

### electron-builder 配置
文件: `electron-builder.yml`

**关键配置:**
- 只构建 Windows x64
- 使用 NSIS 安装程序
- 不自动发布（publish: never）

### package.json 构建脚本
```json
{
  "scripts": {
    "build:win": "npm run build && npx electron-builder --win --x64 --publish never"
  }
}
```

**参数说明:**
- `--win` - 只构建 Windows 版本
- `--x64` - 只构建 64 位
- `--publish never` - 不自动发布

## 故障排除

### 构建失败
1. 检查 TypeScript 编译错误
2. 检查依赖是否正确安装
3. 查看 GitHub Actions 日志

### 产物过大
1. 检查是否包含不必要的文件
2. 启用 asar 打包
3. 使用 files 过滤

### 下载失败
1. 检查 Artifact 保留时间
2. 重新运行构建
3. 使用 gh CLI 下载

## 下一步

- [ ] 添加代码签名
- [ ] 添加自动更新功能
- [ ] 优化构建速度
- [ ] 添加多语言支持
