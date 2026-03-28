# 诺兰时光魔兽登录器

最小可测版，目标只做 4 件事：

1. 打开注册页
2. 选择 WoW 客户端目录
3. 自动写入 `realmlist.wtf`
4. 启动游戏并连接服务器

## 当前链路状态

已打通：

- 注册页：`http://1.14.59.54:5000`
- 注册接口：`/api/register`
- 游戏登录：已用新注册账号实测成功
- 服务器：`1.14.59.54`
- 客户端版本：`3.3.5a (12340)`

## 本地开发运行

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wow_launcher.py
```

## Windows 打包

在 Windows 上运行：

```bat
build_windows.bat
```

输出目录：

```text
dist\NuolanWoWLauncher\
```

## 最小测试流程

1. 打开注册页创建账号
2. 选择 WoW 客户端目录
3. 点击“验证目录”
4. 点击“启动游戏”
5. 登录进服

## 说明

当前仓库先提交源码与打包脚本。
Windows `.exe` 需在真实 Windows 环境执行 `build_windows.bat` 生成。
