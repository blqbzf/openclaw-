# 客户端补丁完整流水线

## 目录
- `patches/src/`：补丁源文件（MPQ 内部目录结构）
- `patches/dist/`：Actions 生成的 MPQ
- `patch-manifests/manifest.json`：登录器拉取补丁清单
- `patch-manifests/version.json`：补丁版本摘要
- `tools/BlpCli/`：仓库内置 BLP 生成工具
- `tools/manifest/`：manifest/version 生成脚本

## 当前首版
- 分发方式：GitHub Actions artifact / GitHub Release
- 登录器优先拉服务端 manifest，失败后回退 GitHub manifest
