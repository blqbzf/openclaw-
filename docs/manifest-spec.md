# Manifest 规范

## manifest.json 格式

```json
{
  "version": "1.0.0",
  "lastUpdated": "2026-03-27T21:59:00Z",
  "serverInfo": {
    "name": "诺兰时光魔兽",
    "realm": "1.14.59.54",
    "port": 3724
  },
  "requiredFiles": [
    "Wow.exe",
    "realmlist.wtf"
  ],
  "allowedPatterns": [
    "patch-*.MPQ",
    "lichking.MPQ"
  ],
  "patches": [
    {
      "path": "Data/patch-nolan.MPQ",
      "size": 15728640,
      "sha256": "abc123...",
      "required": true,
      "downloadUrl": "https://1.14.59.54:8080/files/Data/patch-nolan.MPQ"
      "description": "核心补丁 - 自定义模型和功能"
    }
  ],
  "realmlist": {
    "content": "set realmlist 1.14.59.54",
    "encoding": "utf-8"
  },
  "news": [
    {
      "id": "launcher-v1",
      "title": "登录器 v1.0.0 发布",
      "date": "2026-03-27",
      "content": "全新登录器上线，支持自动更新和修复功能"
    }
  ]
}
```

## 字段说明

- `version`: manifest 版本
- `lastUpdated`: 最后更新时间 (ISO 8601)
- `serverInfo`: 服务器信息
- `requiredFiles`: 必需文件列表
- `allowedPatterns`: 允许的 MPQ 文件模式
- `patches`: 补丁列表
  - `path`: 相对于客户端目录的路径
  - `size`: 文件大小（字节）
  - `sha256`: SHA-256 哈希值
  - `required`: 是否必需
  - `downloadUrl`: 下载 URL
  - `description`: 补丁描述
- `realmlist`: realmlist 配置
- `news`: 公告列表
