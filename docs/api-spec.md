# API 规范

## 统一响应格式

所有 API 必须返回统一的 JSON 格式：

### 成功响应
```json
{
  "success": true,
  "data": {
    // 匉具体数据
  },
  "message": "操作成功"
}
```

### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "ERROR代码",
    "message": "错误详情"
  },
  "details": {
    // 错误堆栈或详细信息
  }
}
```

## 具体接口

### POST /api/register
**请求:**
```json
{
  "username": "player001",
  "password": "SecurePassword123",
  "email": "player@example.com"
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "userId": 123,
    "username": "player001"
  },
  "message": "注册成功"
}
```

### GET /api/manifest
**响应:**
```json
{
  "success": true,
  "data": {
    "version": "1.0.0",
    "lastUpdated": "2026-03-27T21:59:00Z",
    "serverInfo": { ... },
    "requiredFiles": [ ... ],
    "allowedPatterns": [ ... ],
    "patches": [ ... ]
  }
}
```

### GET /api/news
**响应:**
```json
{
  "success": true,
  "data": {
    "news": [
      {
        "id": "news001",
        "title": "欢迎来到诺兰时光",
        "content": "服务器已正式开放...",
        "date": "2026-03-27",
        "important": true
      }
    ]
  }
}
```

### GET /api/version
**响应:**
```json
{
  "success": true,
  "data": {
    "launcherVersion": "1.0.0",
    "backendVersion": "1.0.0",
    "minClientVersion": "3.3.5"
  }
}
```

## 错误处理

1. 所有 API 必须捕获异常并记录到日志
2. 簡化错误信息，返回友好的错误提示
3. 对于 500 错误,需要重试机制
4. 对于 401/403 错误,需要适当的延迟重试
