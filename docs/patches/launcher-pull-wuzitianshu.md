# 登录器直接拉取无字天书补丁

## 当前实现
- `build-png-blp-mpq` 已在 GitHub Actions 主线成功产出 `INV_Misc_Book_WuZiTianShu.blp`
- 仓库已新增：
  - `dist/patches/INV_Misc_Book_WuZiTianShu.blp`
  - `patch-manifests/manifest.json`
- 登录器 `PatchService` 现在会：
  1. 先请求服务器 `http://1.14.59.54:8080/api/patches/manifest`
  2. 如果失败，则回退到 GitHub Raw manifest

## GitHub Raw fallback
- Manifest:
  - `https://raw.githubusercontent.com/blqbzf/openclaw-/main/patch-manifests/manifest.json`
- 当前补丁文件:
  - `https://github.com/blqbzf/openclaw-/raw/main/dist/patches/INV_Misc_Book_WuZiTianShu.blp`

## 当前落地行为
下载目标：
- `<ClientPath>/Data/INV_Misc_Book_WuZiTianShu.blp`

> 下一步仍建议改成完整 MPQ 产物后再让 manifest 指向 MPQ。
