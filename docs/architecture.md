# 系统架构

## 整体架构

```
┌─────────────────────────────┐
│      launcher-win (前端)      │
│  Electron + React + TypeScript │
└─────────────┬───────────────┘
              │
              │ HTTP/HTTPS
              │
              ▼
┌─────────────────────────────┐
│   launcher-backend (API)    │
│   Node.js + TypeScript       │
└─────────────┬───────────────┘
              │
              │ 内网
              │
              ▼
┌─────────────────────────────┐
│   现有 AzerothCore 服务端   │
│   MySQL + AuthServer + WorldServer│
└─────────────────────────────────┘
```

## 组件说明

### launcher-win (前端)

**技术栈:**
- Electron 28+ (桌面应用框架)
- React 18+ (UI 框架)
- TypeScript 5+ (类型安全)
- electron-builder 24+ (打包工具)
- axios (HTTP 客户端)
- sha.js (SHA-256 哈希)

**主要功能:**
1. 客户端目录选择与验证
2. 文件扫描与校验
3. manifest 解析
4. 补丁下载与验证
5. 缓存清理
6. 冲突补丁处理
7. realmlist 修复
8. 账号注册
9. 公告显示
10. 游戏启动

### launcher-backend (API)

**技术栈:**
- Node.js 18+
- Express/Fastify (Web 框架)
- TypeScript 5+
- mysql2 (MySQL 客户端)
- winston (日志库)
- express-rate-limit (限流)

**主要 API:**
- POST /api/register - 账号注册
- GET /api/manifest - 获取补丁清单
- GET /api/news - 获取公告
- GET /api/version - 获取版本信息
- GET /files/* - 补丁下载

**安全策略:**
1. IP 频率限制
2. 用户名格式验证
3. 密码强度检查
4. 邮箱格式验证
5. 所有 API 返回统一 JSON 格式
6. 详细日志记录
