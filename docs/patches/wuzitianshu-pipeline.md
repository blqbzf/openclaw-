# 无字天书 PNG → BLP → MPQ 流水线

当前已入库：
- 源图：`assets/icons-src/INV_Misc_Book_WuZiTianShu.png`（已缩为 64×64）
- Workflow：`.github/workflows/build-png-blp-mpq.yml`
- 脚本：`.github/scripts/build-mpq.ps1`

## 目标产物
- `Interface/Icons/INV_Misc_Book_WuZiTianShu.blp`
- `Patch-WuZiTianShu.mpq`

## 当前状态
这次先把仓库结构、64×64 图标源、Windows Actions 构建入口和 MPQ staging 目录全部落到仓库。
下一步继续补：
1. 在 Windows runner 上接入稳定可下载的 BLPConverter
2. 产出 `.blp`
3. 接入 MPQ 打包工具
4. 上传最终 `.mpq` artifact / release asset
