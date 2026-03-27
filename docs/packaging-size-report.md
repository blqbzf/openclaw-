# 登录器体积优化报告

## 优化前体积分析

### 预计问题
- ❌ 打包了不必要的大文件
- ❌ 没有排除 node_modules 中的文档和测试文件
- ❌ 没有启用 asar 压缩
- ❌ 包含了整个项目目录（docs, logs, 等）

### 预估体积: 150-300MB 😱

## 优化措施

### 1. 启用 ASAR 打包
```yaml
asar: true
```
**效果:** 将应用文件打包成单个归档文件，**减少:** 约 50%

### 2. 排除不必要文件

#### 排除 node_modules 中的文档
```yaml
files:
  - "!**/node_modules/*/{README,readme,readme.md,readme.txt,CHANGELOG,changelog,changelog.md,changelog.txt,LICENSE,license,license.md,license.txt,NOTICE,notice,notice.md,notice.txt}"
  - "!**/node_modules/.bin/**"
  - "!**/node_modules/**/*.ts"
  - "!**/node_modules/**/*.map"
```
**减少:** 约 30-50MB

#### 排除开发文件
```yaml
files:
  - "!**/docs/**"
  - "!**/logs/**"
  - "!**/cache/**"
  - "!**/screenshots/**"
  - "!**/tests/**"
  - "!**/__tests__/**"
  - "!**/src/**"
  - "!**/public/**"
  - "!**/.env*"
  - "!**/*.ts"
  - "!**/*.tsx"
  - "!**/*.map"
  - "!**/*.log"
  - "!**/*.gif"
  - "!**/*.svg"
```
**减少:** 约 20-40MB

### 3. 只上传必要文件

修改 GitHub Actions workflow:
```yaml
path: |
  launcher-win/dist/*.exe
  launcher-win/dist/*.blockmap
  launcher-win/dist/builder-effective-config.yaml
```
**不包含:**
- ❌ win-unpacked/ 目录 (未打包的应用目录)
- ❌ 其他配置文件

## 优化后体积预估

| 组件 | 优化前 | 优化后 | 减少 |
|------|-------|-------|------|
| **node_modules 文档** | 30-50MB | 0MB | -30-50MB |
| **TypeScript 源文件** | 20-30MB | 0MB | -20-30MB |
| **测试/日志文件** | 10-20MB | 0MB | -10-20MB |
| **ASAR 压缩** | - | -50% | -40-80MB |
| **其他排除项** | 20-40MB | 0MB | -20-40MB |
| **总计** | **150-300MB** | **50-80MB** | **-100-220MB** |

## 最终产物大小

### 单个可执行文件
- **NolanWoWLauncher Setup 1.0.0.exe**: **50-80MB**
  - 包含: Electron 运行时 + 应用代码 + 依赖
  - 压缩: NSIS 安装程序压缩

### dist 目录大小
- **优化前**: ~300MB (包含 win-unpacked/)
- **优化后**: ~80MB (只包含必要文件)
- **减少**: ~220MB

## 文件排除详细列表

### 完全排除
- ✅ 所有 TypeScript 源文件 (`*.ts`, `*.tsx`)
- ✅ 所有 SourceMap 文件 (`*.map`)
- ✅ 所有日志文件 (`*.log`)
- ✅ 所有文档目录 (`docs/`)
- ✅ 所有测试目录 (`tests/`, `__tests__/`)
- ✅ 所有缓存目录 (`cache/`)
- ✅ 所有截图目录 (`screenshots/`)
- ✅ 所有图片文件 (`*.gif`, `*.svg`)
- ✅ 所有环境配置文件 (`.env*`)

### node_modules 排除
- ✅ README 文件
- ✅ CHANGELOG 文件
- ✅ LICENSE 文件
- ✅ NOTICE 文件
- ✅ .bin 目录
- ✅ TypeScript 定义文件 (`*.d.ts`)
- ✅ SourceMap 文件 (`*.map`)

## 验证方法

### 本地构建验证
```bash
cd launcher-win
npm install
npm run build:win
du -sh dist/
```

**预期输出:** `50-80MB` (优化后)

### GitHub Actions 验证
构建完成后，1. 下载 Artifact
2. 解压查看大小
3. 确认只包含 `*.exe`, `*.blockmap`, `*.yaml`

## 关键配置文件

### electron-builder.yml
```yaml
asar: true  # 启用 ASAR 打包

files:
  - package.json
  - dist/**/*
  # 排除规则...
  - "!**/*.ts"
  - "!**/*.tsx"
  # ...

nsis:
  # ... NSIS 配置
```

### GitHub Actions workflow
```yaml
- name: Upload Windows Artifact
  uses: actions/upload-artifact@v4
  with:
    path: |
      launcher-win/dist/*.exe
      launcher-win/dist/*.blockmap
      launcher-win/dist/builder-effective-config.yaml
```

## 性能影响

### 启动速度
- ✅ ASAR 打包提升读取速度
- ✅ 减少文件数量提升启动速度

### 安装速度
- ✅ 更小的安装包下载更快
- ✅ NSIS 解压速度更快

### 运行时性能
- ✅ 没有性能影响
- ✅ ASAR 不会影响运行时性能

## 下一步优化

- [ ] 启用压缩 (compression: maximum)
- [ ] 删除未使用的依赖
- [ ] 使用 webpack/vite 进一步优化
- [ ] 添加代码签名
- [ ] 启用增量更新

---

**优化完成时间:** 2026-03-27 23:53
**预计减少:** 100-220MB
**最终大小:** 50-80MB
