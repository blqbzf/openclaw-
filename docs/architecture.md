# 系统架构

诺兰时光 WoW 登录器采用 Electron + React + TypeScript 构建。
技术栈包括:
- **前端**: Electron + React + TypeScript
- **后端**: Node.js + Express + TypeScript
- **构建**: electron-builder + GitHub Actions

- **文件校验**: SHA-256（已禁用 MD5）

- **配置**: JSON
## 枌述目录结构

### 庂端端 - launcher-win (前端)
- **技术栈**: Electron + React + TypeScript
- **主要功能**:
  - 客户端目录选择
  - 文件扫描
  - 补丁下载
  - 缓存清理
  - realmlist 修复
  - 游戏启动
- **构建工具**: electron-builder

- **目标平台**: Windows 10+

### 后端 - launcher-backend (API 服务)
- **技术栈**: Node.js + Express + TypeScript
- **主要 API**:
  - POST /api/register - 账号注册
  - GET /api/manifest - 获取补丁清单
  - GET /api/news - 获取公告
  - GET /api/version - 版本信息
  - GET /files/* - 补丁下载
- **安全策略**:
  - IP 频率限制
  - 输入验证
  - 日志记录

## 🔒 安全要求

1. **不直接访问数据库** - 通过 API 间接访问
2. **危险操作确认** - UI 弹窗确认
3. **日志落盘** - 所有操作记录到日志文件
4. **文件备份** - 删除前先备份
5. **SHA-256 校验** - 确保文件完整性
6. **密钥管理** - 证书私钥不提交到 Git

