# MPQ 构建失败记录（2026-03-30）

## 主线失败 run
- workflow: `build-png-blp-mpq`
- run id: `23745220524`

## 已确认根因
`smpq` 不是简单路径写错，而是它依赖 `StormLib`。原脚本直接 clone + cmake build，没有先提供 `StormLib`，因此最终没有生成 `smpq.exe`。

## 修复策略
1. Actions 内显式拉取 `vcpkg`
2. 安装 `stormlib:x64-windows`
3. 用 `vcpkg` toolchain 配置 `smpq`
4. 关闭不需要的 `WITH_KDE`
5. 同时兼容 `build/Release/smpq.exe` 与 `build/smpq.exe`
6. 失败时上传调试产物
