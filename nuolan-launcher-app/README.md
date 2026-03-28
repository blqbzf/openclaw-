# 诺兰时光魔兽登录器

最小可测版：先验证注册、启动、登录、进服链路。

## 当前目标

只验证 4 件事：

1. 能打开注册页
2. 能选择 WoW 客户端目录
3. 能自动写入 `realmlist.wtf`
4. 能启动游戏并连接服务器

## 当前已实现

- 打开注册页按钮
- 选择并保存 WoW 客户端目录
- 自动校验 `Wow.exe` / `Wow-64.exe`
- 自动写入 `realmlist.wtf`
- 兼容路径：
  - `Data/zhCN/realmlist.wtf`
  - `Data/zhTW/realmlist.wtf`
  - `Data/enUS/realmlist.wtf`
  - 根目录 `realmlist.wtf`
- 一键启动游戏
- 检查 auth/world 基础在线状态
- 日志文件：`launcher.log`

## 注意

当前注册链接配置为：

- `http://1.14.59.54:5000`

如果点击注册页后浏览器打不开，不代表登录器按钮没做，
而是说明服务端注册站点本身当前没有正常返回页面。

## 本地开发运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wow_launcher.py
```

## Windows 打包

```bat
build_windows.bat
```

输出结果：

```text
 dist\NuolanWoWLauncher.exe              # 单独可双击执行文件
 dist\NuolanWoWLauncher\                # 便携目录（不是安装器）
 ├─ NuolanWoWLauncher.exe
 ├─ launcher_config.json
 ├─ README.md
 ├─ assets\background.jpg
```

## 最小测试流程

1. 点击“打开注册页”
2. 选择 WoW 客户端目录
3. 点击“验证目录”
4. 点击“启动游戏”
5. 看客户端是否成功连接到 `1.14.59.54`

## 如果失败

请回传：

- `launcher.log`
- 卡在哪一步
- 客户端目录是什么结构

## 交付建议

当前优先交付便携目录 / zip，不做安装器。
