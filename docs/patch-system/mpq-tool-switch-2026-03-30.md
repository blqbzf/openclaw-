# MPQ 工具切换记录（2026-03-30）

## 原方案备份
已备份到：
- `backups/mpq-workflow-20260330/build-mpq.ps1.bak`
- `backups/mpq-workflow-20260330/build-png-blp-mpq.yml.bak`
- `backups/mpq-workflow-20260330/manifest.json.bak`（如存在）
- `backups/mpq-workflow-20260330/version.json.bak`（如存在）

## 切换原因
- `smpq` 在 GitHub Actions + vcpkg StormLib 环境下卡在版本检查
- 先切换到 `TheGrayDot/mpqcli` 评估兼容性

## 回滚方式
直接把 `backups/mpq-workflow-20260330/` 下备份文件覆盖回原位置即可。
