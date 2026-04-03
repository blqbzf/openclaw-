--[[
    无字天书传送系统 v3.3
    ALE Eluna 实现
    注意：ALE 的 OnUse 返回 false = 阻止施法（与标准 Eluna 相反）
    
    v3.3 改动：优化配色和显示
]]

local ITEM_ID = 910000

-- 颜色方案
local C = {
    prefix = "|cFFFFD700",      -- 金色 前缀
    white  = "|cFFFFFFFF",      -- 白色 普通文本
    gray   = "|cFF9D9D9D",      -- 灰色 返回/次要
    red    = "|cFFFF4444",      -- 柔红 关闭/警告
    gold   = "|cFFFFD700",      -- 金色 分类标题
    cyan   = "|cFF00FFCC",      -- 青绿 传送目标
    green  = "|cFF66FF66",      -- 绿色 成功提示
    header = "|cFFFFD700",      -- 金色 标题栏
}

-- ═══════════════════════════════════════════════════════════════
-- 坐标配置表
-- {action, name, team(0联盟/1部落/2中立), group(1主城/2出生地/3中立), map, x, y, z, o}
-- ═══════════════════════════════════════════════════════════════
local DEST = {
    -- 联盟主城
    {1001, "暴风城",     0, 1,   0, -8833.38,    628.63,   94.01, 0.67},
    {1002, "铁炉堡",     0, 1,   0, -4918.12,   -956.75,  501.45, 5.24},
    {1003, "达纳苏斯",   0, 1,   1,  9947.52,   2482.73, 1316.21, 1.59},
    {1004, "埃索达",     0, 1, 530, -4009.89, -11865.30,   -0.99, 2.15},
    -- 部落主城
    {2001, "奥格瑞玛",   1, 1,   1,  1601.08,  -4378.69,    9.98, 2.14},
    {2002, "雷霆崖",     1, 1,   1, -1281.74,    121.73,   129.69, 3.14},
    {2003, "幽暗城",     1, 1,   0,  1588.19,    239.79,   -52.12, 0.52},
    {2004, "银月城",     1, 1, 530,  9738.26,  -7454.31,    13.55, 6.26},
    -- 联盟出生地
    {1101, "北郡山谷",   0, 2,   0, -8913.23,   -132.00,    82.03, 1.00},
    {1102, "寒脊山谷",   0, 2,   0, -6240.32,    330.23,   382.76, 4.41},
    {1103, "幽影谷",     0, 2,   1, 10311.30,    831.23,  1326.41, 1.02},
    {1104, "埃门谷",     0, 2, 530, -3949.63, -11939.40,   -1.09, 2.17},
    -- 部落出生地
    {2101, "试炼谷",     1, 2,   1,  -624.00,   -4254.00,   38.78, 2.06},
    {2102, "纳拉其营地", 1, 2,   1, -2917.58,   -258.02,    55.00, 2.22},
    {2103, "死亡钟楼",   1, 2,   0,  1678.64,   1682.39,   121.18, 3.14},
    {2104, "永歌森林",   1, 2, 530, 10349.60,  -6355.44,    24.00, 5.50},
    -- 中立城市
    {3001, "希利苏斯",   2, 3,   1, -6814.00,    730.00,    42.00, 2.50},
    {3002, "加基森",     2, 3,   1, -7118.00,  -3775.00,    12.00, 2.60},
    {3003, "冬泉谷",     2, 3,   1,  6794.00,  -4745.00,   701.00, 1.20},
    {3004, "沙塔斯城",   2, 3, 530, -1859.67,   5342.69,   -12.43, 3.14},
    {3005, "达拉然",     2, 3, 571,  5809.55,    503.98,   657.53, 2.38},
}

local DEST_MAP = {}
for _, d in ipairs(DEST) do
    DEST_MAP[d[1]] = d
end

-- ═══════════════════════════════════════════════════════════════
-- 限制判断
-- ═══════════════════════════════════════════════════════════════
local function CanUse(player)
    if (player:IsInCombat()) then
        player:SendBroadcastMessage(C.red .. "[无字天书]|r 战斗中无法使用！")
        return false
    end
    if (not player:IsAlive()) then
        player:SendBroadcastMessage(C.red .. "[无字天书]|r 死亡状态下无法使用！")
        return false
    end
    if (player:InBattleground()) then
        player:SendBroadcastMessage(C.red .. "[无字天书]|r 战场中无法使用！")
        return false
    end
    if (player:InArena()) then
        player:SendBroadcastMessage(C.red .. "[无字天书]|r 竞技场中无法使用！")
        return false
    end
    return true
end

-- ═══════════════════════════════════════════════════════════════
-- 菜单构建
-- ═══════════════════════════════════════════════════════════════
local function BuildMainMenu(player, item)
    player:GossipClearMenu()
    local team = player:GetTeam()

    player:GossipMenuAddItem(0, C.gold .. "━━━ 传 送 总 览 ━━━|r", 0, 9000)  -- 标题行，不可点击
    player:GossipMenuAddItem(0, "", 0, 9000)  -- 空行分隔

    local groupNames = {
        [1] = "|TInterface\\Icons\\INV_Misc_Map02:20|t 阵营主城",
        [2] = "|TInterface\\Icons\\INV_Misc_Map01:20|t 新手出生地",
        [3] = "|TInterface\\Icons\\INV_Misc_Map03:20|t 中立城市",
    }

    for groupId = 1, 3 do
        local hasDest = false
        for _, d in ipairs(DEST) do
            if d[4] == groupId and (d[3] == 2 or d[3] == team) then
                hasDest = true
                break
            end
        end
        if hasDest then
            player:GossipMenuAddItem(0, groupNames[groupId], 0, groupId)
        end
    end

    player:GossipMenuAddItem(0, "", 0, 9000)  -- 空行分隔
    player:GossipMenuAddItem(0, C.red .. "关闭", 0, 9999)
    player:GossipSendMenu(100, item)
end

local function BuildDestMenu(player, item, groupId)
    player:GossipClearMenu()
    local team = player:GetTeam()

    local groupTitles = {
        [1] = C.gold .. "━━━ 阵 营 主 城 ━━━|r",
        [2] = C.gold .. "━━━ 新 手 出 生 地 ━━━|r",
        [3] = C.gold .. "━━━ 中 立 城 市 ━━━|r",
    }

    player:GossipMenuAddItem(0, groupTitles[groupId] or "", 0, 9000)

    for _, d in ipairs(DEST) do
        if d[4] == groupId and (d[3] == 2 or d[3] == team) then
            player:GossipMenuAddItem(0, C.cyan .. d[2] .. C.white, 0, d[1])
        end
    end

    player:GossipMenuAddItem(0, "", 0, 9000)
    player:GossipMenuAddItem(0, C.gray .. "← 返回主菜单", 0, 8888)
    player:GossipSendMenu(100, item)
end

-- ═══════════════════════════════════════════════════════════════
-- OnUse
-- ═══════════════════════════════════════════════════════════════
local function OnUse(event, player, item, target)
    if (not CanUse(player)) then
        return false
    end
    BuildMainMenu(player, item)
    return false
end

-- ═══════════════════════════════════════════════════════════════
-- OnSelect
-- ═══════════════════════════════════════════════════════════════
local function OnSelect(event, player, item, sender, intid, code, menuid)
    if intid == 9999 then
        player:CloseGossip()
        return false
    end

    -- 标题行和空行，忽略点击
    if intid == 9000 then
        return false
    end

    if intid == 8888 then
        if (not CanUse(player)) then
            player:CloseGossip()
            return false
        end
        BuildMainMenu(player, item)
        return false
    end

    -- 分类入口 1-10
    if intid >= 1 and intid <= 10 then
        if (not CanUse(player)) then
            player:CloseGossip()
            return false
        end
        BuildDestMenu(player, item, intid)
        return false
    end

    -- 执行传送
    local dest = DEST_MAP[intid]
    if dest then
        if (not CanUse(player)) then
            player:CloseGossip()
            return false
        end
        player:Teleport(dest[5], dest[6], dest[7], dest[8], dest[9])
        player:SendBroadcastMessage(C.green .. "[无字天书]|r 已传送至 " .. C.cyan .. dest[2])
        player:CloseGossip()
        return false
    end

    player:CloseGossip()
    return false
end

RegisterItemEvent(ITEM_ID, 2, OnUse)
RegisterItemGossipEvent(ITEM_ID, 2, OnSelect)
print("[无字天书] 传送系统 v3.3 已加载")
