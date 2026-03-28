# 诺兰最小注册站

目标只有一个：创建 **能登录 AzerothCore / WoW 3.3.5a** 的账号。

## 当前实现

- Python Flask 最小站点
- 页面地址：`/`
- 健康检查：`/health`
- 注册接口：`POST /api/register`
- 直接写入 `acore_auth.account`
- `salt/verifier` 按 AzerothCore 源码中的 SRP6 注册逻辑生成

## 运行方式

```bash
chmod +x start.sh
./start.sh
```

默认端口：

- `5000`

## 环境变量

可选：

- `NOLAN_DB_HOST` 默认 `127.0.0.1`
- `NOLAN_DB_PORT` 默认 `3306`
- `NOLAN_DB_USER` 默认 `acore`
- `NOLAN_DB_PASSWORD` 默认 `Acore123456!`
- `NOLAN_DB_NAME` 默认 `acore_auth`
- `NOLAN_SERVER_NAME` 默认 `诺兰时光魔兽`
- `NOLAN_EMAIL_DOMAIN` 默认 `nolan.local`
- `PORT` 默认 `5000`

## 说明

这个站点是给“最小可测链路”用的：

1. 注册账号
2. 打开最小登录器
3. 自动写入 `realmlist.wtf`
4. 启动游戏
5. 登录进服
