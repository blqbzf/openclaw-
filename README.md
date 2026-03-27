# 诺兰时光 WoW 登录器

基于 Electron + React + TypeScript 构建的魔兽世界 3.3.5a 私服登录器

## 技术栈

- **前端**: Electron + React + TypeScript
- **构建**: electron-builder
- **CI/CD**: GitHub Actions (Windows runner)
- **后端**: Node.js/TypeScript (launcher backend)
- **配置**: JSON
- **文件校验**: SHA-256

## 项目结构

```
/
├── launcher/              # Electron 应用主目录
│   ├── src/              # TypeScript 源码
│   ├── public/           # 静态资源
│   └── electron-builder.json
├── backend/              # Launcher Backend API
│   ├── src/              # TypeScript 源码
│   └── config/           # 配置文件
├── docs/                 # 文档
└── scripts/              # 构建和部署脚本
```

## 功能列表

- [x] 选择客户端目录
- [x] 检查 Wow.exe 和必要 MPQ 文件
- [x] 拉取 manifest.json
- [x] 自动下载缺失或 hash 不一致的补丁
- [x] 修复 realmlist.wtf
- [x] 清理本地客户端缓存
- [x] 识别其他私服补丁（白名单 + 冲突识别）
- [x] 对冲突补丁执行"备份后移除"
- [x] 提供账号注册入口
- [x] 显示公告/新闻
- [x] 显示当前登录器版本
- [x] 一键启动 Wow.exe
- [x] Windows 构建流程
- [x] 自签名流程（内测版）

## 开发环境

- Node.js 18+
- npm 9+
- Windows 10+ (构建)

## 快速开始

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建 Windows 版本
npm run build:win
```

## 许可证

MIT
