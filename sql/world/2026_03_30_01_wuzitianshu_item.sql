-- 无字天书（自定义传送道具）
-- entry: 910000
-- 说明：首版先落普通物品模板 + spell 触发占位，后续可再接入更复杂脚本/坐标分流。

SET @ENTRY := 910000;
SET @SPELL_ID := 8690; -- Hearthstone: item cast, 10s base cast. 用于首版链路验证，后续可替换为定制传送 spell/脚本。

DELETE FROM `item_template` WHERE `entry` = @ENTRY;
INSERT INTO `item_template` (
  `entry`,`class`,`subclass`,`SoundOverrideSubclass`,`name`,`displayid`,`Quality`,`Flags`,`FlagsExtra`,
  `BuyCount`,`BuyPrice`,`SellPrice`,`InventoryType`,`AllowableClass`,`AllowableRace`,`ItemLevel`,`RequiredLevel`,
  `RequiredSkill`,`RequiredSkillRank`,`requiredspell`,`requiredhonorrank`,`RequiredCityRank`,`RequiredReputationFaction`,
  `RequiredReputationRank`,`maxcount`,`stackable`,`ContainerSlots`,`StatsCount`,`stat_type1`,`stat_value1`,`stat_type2`,
  `stat_value2`,`ScalingStatDistribution`,`ScalingStatValue`,`dmg_min1`,`dmg_max1`,`dmg_type1`,`armor`,`holy_res`,`fire_res`,
  `nature_res`,`frost_res`,`shadow_res`,`arcane_res`,`delay`,`ammo_type`,`RangedModRange`,`spellid_1`,`spelltrigger_1`,
  `spellcharges_1`,`spellppmRate_1`,`spellcooldown_1`,`spellcategory_1`,`spellcategorycooldown_1`,`spellid_2`,`spelltrigger_2`,
  `spellcharges_2`,`spellppmRate_2`,`spellcooldown_2`,`spellcategory_2`,`spellcategorycooldown_2`,`bonding`,`description`,
  `PageText`,`LanguageID`,`PageMaterial`,`startquest`,`lockid`,`Material`,`sheath`,`RandomProperty`,`RandomSuffix`,`block`,
  `itemset`,`MaxDurability`,`area`,`Map`,`BagFamily`,`TotemCategory`,`socketColor_1`,`socketContent_1`,`socketColor_2`,
  `socketContent_2`,`socketColor_3`,`socketContent_3`,`socketBonus`,`GemProperties`,`RequiredDisenchantSkill`,`ArmorDamageModifier`,
  `duration`,`ItemLimitCategory`,`HolidayId`,`ScriptName`,`DisenchantID`,`FoodType`,`minMoneyLoot`,`maxMoneyLoot`,`flagsCustom`,
  `VerifiedBuild`
) VALUES (
  @ENTRY,15,0,-1,'无字天书',21600,4,0,0,
  1,0,0,0,-1,-1,80,1,
  0,0,0,0,0,0,
  0,1,1,0,0,0,0,
  0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
  0,0,1.0,@SPELL_ID,0,
  0,0,0,0,0,0,0,
  0,0,0,0,0,1,'一卷无字，却可引路。使用后在白光中归返既定之地。',
  0,0,0,0,0,1,0,0,0,0,
  0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,
  0,0,0,'',0,0,0,0,0,
  12340
);

DELETE FROM `item_template_locale` WHERE `ID` = @ENTRY AND `locale` = 'zhCN';
INSERT INTO `item_template_locale` (`ID`,`locale`,`Name`,`Description`,`VerifiedBuild`) VALUES
(@ENTRY,'zhCN','无字天书','一卷无字，却可引路。使用后在白光中归返既定之地。',12340);
