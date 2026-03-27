# Launcher Backend - 部署指南

## 快速开始

### 1. 安装依赖
```bash
cd launcher-backend
npm install
```

### 2. 配置
复制配置文件:
```bash
cp config/default.json config/production.json
```

编辑 `config/production.json` 修改数据库连接等信息。

### 3. 启动服务
```bash
npm run build
npm start
```

服务将在 `http://localhost:3001` 启动。

## API 端点

### GET /api/manifest
获取客户端补丁清单。

**响应示例:**
```json
{
  "version": "1.0.0",
  "lastUpdated": "2026-03-27T22:04:00Z",
  "serverInfo": {
    "name": "诺兰时光魔兽",
    "realm": "1.14.59.54",
    "port": 3724
  },
  "patches": [...]
}
```

### GET /api/news
获取公告列表。

### GET /api/version
获取版本信息。

### GET /health
健康检查。

## 配置说明

### 数据库配置
```json
{
  "database": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "acore",
    "password": "your_password",
    "database": "acore_auth"
  }
}
```

### 文件路径配置
```json
{
  "files": {
    "manifestPath": "./data/manifest.json",
    "newsPath": "./data/news.json",
    "patchDir": "./patches"
  }
}
```

## 部署到生产环境

### 使用 PM2
```bash
pm2 start launcher-backend
```

### 使用 Docker
```bash
docker build -t launcher-backend .
docker run -d -p 3001:3001 launcher-backend
```

## 日志

日志文件位于 `./logs/` 目录:
- `error.log` - 错误日志
- `combined.log` - 所有日志

## 安全建议
1. 使用 HTTPS
2. 配置防火墙规则
3. 定期备份 `data/` 目录
4. 监控日志文件
