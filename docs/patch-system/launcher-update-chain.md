# 登录器补丁更新链路

## 当前实现
- 读取 `manifest.json`
- 读取 `version.json`
- 校验本地 `Data` 目录中的补丁哈希
- 缺失或过期则自动下载
- 下载完成后自动清理 `Cache/` 与 `WDB/`

## 下载顺序
1. 服务器 manifest API
2. GitHub Raw fallback manifest

## 当前分发方式
- 首版：GitHub artifact/release 路线兼容
- 后续：可切到自有下载服务器
