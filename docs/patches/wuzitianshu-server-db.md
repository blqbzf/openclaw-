# 无字天书服务端 DB 落地说明

## 当前定稿
- 物品名称：无字天书
- entry：`910000`
- 图标：`INV_Misc_Book_WuZiTianShu`
- 当前 SQL：`sql/world/2026_03_30_01_wuzitianshu_item.sql`

## 当前实现范围
首版先保证：
1. world DB 中存在可查询的物品模板
2. 客户端补丁可显示对应图标
3. 登录器可自动拉取补丁

## spell / 行为说明
当前 SQL 先用 `spellid_1 = 8690` 作为首版占位链路验证。
- 目的：先打通“能查到物品 + 能看到图标 + 能正常发包使用物品”的最小链路
- 后续若要变成“5 秒白光 + 自定义坐标传送”，建议再追加：
  - 定制 spell
  - 或 ScriptName + 服务端脚本
  - 或 spell target/脚本联动

## world DB 导入
在 world DB 执行：

```sql
SOURCE /path/to/sql/world/2026_03_30_01_wuzitianshu_item.sql;
```

校验：

```sql
SELECT entry, name, spellid_1, description
FROM item_template
WHERE entry = 910000;

SELECT ID, locale, Name, Description
FROM item_template_locale
WHERE ID = 910000;
```

## 是否需要重启
- 仅客户端补丁：不需要
- 若 world DB 已导入但 worldserver 仍查不到：建议重启 `worldserver`
- 若后续接入 ScriptName / 自定义脚本：需要重启 `worldserver`
