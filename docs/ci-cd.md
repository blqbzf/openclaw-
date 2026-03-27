# CI/CD 流程说明

## GitHub Actions 工作流

### 触发条件
- Push 到 `main` 或 `feat/wow-launcher` 分支
- 手动触发 (workflow_dispatch)

### 构建流程
1. **检出代码** - checkout@v4
2. **安装依赖** - npm ci (launcher-win)
3. **构建产物** - npm run build:win
4. **上传 Artifact** - actions/upload-artifact@v4

### 构建产物
**Artifact 名称:** `NolanWoWLauncher-Windows`

**包含文件:**
- `*.exe` - Windows 可执行文件
- `*.yml` - 配置文件
- `*.blockmap` - 增量更新文件

**保留时间:** 30 天

## 下载构建产物

### 方式 1: GitHub UI
1. 进入 Actions 页面
2. 选择对应的 workflow 运行记录
3. 滚动到底部 Artifacts 区域
4. 点击 `NolanWoWLauncher-Windows` 下载

### 方式 2: GitHub CLI
```bash
gh run download <run-id> -n NolanWoWLauncher-Windows
```

### 方式 3: API
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/blqbzf/openclaw-/actions/artifacts \
  | jq -r '.artifacts[] | select(.name == "NolanWoWLauncher-Windows") | .archive_download_url'
```

## 当前限制

### 不支持自动发布
- ❌ 不会自动创建 GitHub Release
- ❌ 不需要 GH_TOKEN
- ✅ 只生成构建产物

### 未来计划
- [ ] 添加自动发布到 GitHub Release
- [ ] 添加版本号自动递增
- [ ] 添加变更日志生成
- [ ] 添加多平台构建 (macOS, Linux)

## 构建配置

### electron-builder 配置
文件: `launcher-win/electron-builder.yml`

关键配置:
```yaml
win:
  target:
    - target: nsis
      arch:
        - x64
  publish: never  # 不自动发布
```

### package.json 配置
```json
{
  "scripts": {
    "build:win": "npm run build && npx electron-builder --win --x64 --publish never"
  }
}
```

## 监控和日志

### 查看构建状态
```bash
gh run list --workflow build-windows-launcher.yml --limit 5
```

### 查看构建日志
```bash
gh run view <run-id> --log
```

### 实时监控
```bash
gh run watch <run-id>
```

## 故障排除

### 构建失败
1. 检查 TypeScript 编译错误
2. 检查依赖版本
3. 查看 GitHub Actions 日志

### Artifact 下载失败
1. 检查权限
2. 确认 Artifact 未过期
3. 重新运行构建

### 构建时间过长
1. 缓存 node_modules
2. 减少构建目标
3. 优化 TypeScript 编译

## 最佳实践

1. **提交前测试**
   ```bash
   cd launcher-win
   npm ci
   npm run build:win
   ```

2. **检查产物大小**
   - 正常大小: 50-80MB
   - 过大: 检查是否包含不必要文件

3. **保留构建记录**
   - 重要版本保留 Artifacts
   - 定期清理旧的构建

4. **版本管理**
   - 使用语义化版本号
   - 记录每个版本的变更

## 安全注意事项

1. **不要提交敏感信息**
   - 证书文件
   - API 密钥
   - 数据库密码

2. **使用 Secrets**
   - GitHub Secrets 存储敏感信息
   - 环境变量传递配置

3. **代码签名**
   - 未来添加代码签名
   - 使用受信任的证书

---

**当前状态:** ✅ Windows 构建流程已优化，只生成产物不自动发布
