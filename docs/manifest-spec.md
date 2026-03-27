# Manifest 规范

## 📋 JSON 格式

```json
{
  "version": "1.0.0",
  "lastUpdated": "2026-03-27T22:04:00Z",
  "serverInfo": {
    "name": "诺兰时光魔兽",
    "realm": "1.14.59.54",
    "port": 3724
  },
  "clientInfo": {
    "minVersion": "3.3.5",
    "build": 12340,
    "exe": "Wow.exe"
    "realmlist": "realmlist.wtf"
  },
  "requiredFiles": [
    "Wow.exe",
    "realmlist.wtf",
    "Data/common-2.MPQ",
    "Data/expansion1.MPQ",
    "Data/expansion2.MPQ",
    "Data/expansion3.MPQ",
    "Data/lichking.MPQ",
    "Data/patch.MPQ"
  ],
  "allowedPatterns": [
    "Data/patch-*.MPQ",
    "Data/wow-*.MPQ"
  ],
  "patches": [
    {
      "id": "patch-nolan-creature",
      "path": "Data/patch-nolan-creature.MPQ",
      "size": 5242880,
      "sha256": "abc123...",
      "required": true,
      "downloadUrl": "http://1.14.59.54:3000/files/patch-nolan-creature.MPQ",
      "description": "NPC 模型修复补丁"
    }
  ],
  "realmlist": {
    "content": "set realmlist 1.14.59.54",
    "encoding": "utf-8"
  },
  "news": [
    {
      "id": "welcome",
      "title": "欢迎来到诺兰时光魔兽",
      "content": "全新服务器,更多精彩内容等你探索",
      "date": "2026-03-27",
      "author": "管理员"
    },
    {
      "id": "launcher-update",
      "title": "登录器 v1.0.0 发布",
      "content": "全新登录器,支持自动补丁更新",
      "date": "2026-03-27",
      "author": "管理员"
    }
  ],
  "versionInfo": {
    "launcherVersion": "1.0.0",
    "backendVersion": "1.0.0",
    "minClientVersion": "3.3.5"
  }
}
```

## 🔍 必填字段说明

### version
- **类型**: string
- **说明**: manifest 版本号

### serverInfo
- **name**: 服务器名称
- **realm**: 服务器地址
- **port**: 登录端口

### clientInfo
- **minVersion**: 最低客户端版本
- **build**: 客户端构建号
- **exe**: 可执行文件名
- **realmlist**: realmlist 文件名

### requiredFiles
- **类型**: string[]
- **说明**: 必需文件列表

### allowedPatterns
- **类型**: string[]
- **说明**: 允许的补丁文件模式（用于识别冲突补丁）

### patches
- **id**: 补丁 ID
- **path**: 补丁路径（相对客户端目录）
- **size**: 文件大小（字节）
- **sha256**: SHA-256 哈希值
- **required**: 是否必需
- **downloadUrl**: 下载 URL
- **description**: 补丁描述

### realmlist
- **content**: realmlist 内容
- **encoding**: 文件编码

### news
- **id**: 公告 ID
- **title**: 公告标题
- **content**: 公告内容
- **date**: 发布日期
- **author**: 作者

### versionInfo
- **launcherVersion**: 登录器版本
- **backendVersion**: 后端版本
- **minClientVersion**: 最低客户端版本

## ⚠️ 注意事项
1. **SHA-256 校验**: 必须计算准确的 SHA-256 哈希值
2. **文件路径**: 使用相对路径，以 / 开头表示客户端根目录
3. **下载 URL**: 必须是完整的 HTTP URL
4. **allowedPatterns**: 用于识别不属于本服务器的补丁文件
