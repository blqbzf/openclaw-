# 补丁系统部署指南

## 📁 服务器端配置

### 1. 创建补丁目录
```bash
mkdir -p /var/www/html/patches/patches
```

### 2. 放置文件
```
/var/www/html/patches/
├── manifest.json          # 补丁清单（从本项目复制）
└── patches/               # 补丁文件目录
    ├── patch-ZP1.MPQ     # 补丁文件1
    ├── patch-ZP2.MPQ     # 补丁文件2
    └── patch-ZP3.MPQ     # 补丁文件3
```

### 3. Nginx配置
```nginx
server {
    listen 8080;
    server_name 1.14.59.54;
    
    location /patches/ {
        alias /var/www/html/patches/;
        autoindex on;
        
        # 允许跨域
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods 'GET, OPTIONS';
    }
}
```

### 4. 重启Nginx
```bash
nginx -t
nginx -s reload
```

---

## 📋 manifest.json 格式说明

```json
{
  "version": "1.0.5",              // 总版本号
  "release_date": "2026-03-22",    // 发布日期
  "changelog": "更新说明",          // 更新日志
  "patches": [                     // 补丁列表
    {
      "name": "patch-ZP1.MPQ",     // 补丁文件名
      "version": "1.0.5",          // 补丁版本
      "size": 315000,              // 文件大小（字节）
      "md5": "abc123def456",       // MD5校验码
      "description": "描述",        // 补丁说明
      "release_date": "2026-03-22", // 发布日期
      "required": true             // 是否必需
    }
  ]
}
```

---

## 🔧 生成MD5校验码

```bash
# Linux/Mac
md5sum patch-ZP1.MPQ

# Windows
certutil -hashfile patch-ZP1.MPQ MD5
```

---

## 📊 工作流程

### 1. 新增物品/功能
```
修改数据库/服务端
    ↓
创建新的MPQ补丁
    ↓
计算MD5
    ↓
更新manifest.json
    ↓
上传到服务器
    ↓
客户端自动检测更新
```

### 2. 客户端更新流程
```
启动登录器
    ↓
下载manifest.json
    ↓
对比本地版本
    ↓
发现新补丁？
    ├─ 是 → 提示更新
    │       ├─ 下载补丁
    │       ├─ MD5校验
    │       ├─ 应用补丁
    │       └─ 更新版本记录
    └─ 否 → 直接启动游戏
```

---

## ✅ 测试清单

### 1. 服务器测试
```bash
# 测试访问manifest.json
curl http://1.14.59.54:8080/patches/manifest.json

# 测试下载补丁
curl -I http://1.14.59.54:8080/patches/patches/patch-ZP1.MPQ
```

### 2. 客户端测试
```
✅ 首次启动 → 下载所有补丁
✅ 再次启动 → 无需更新
✅ 新增补丁 → 自动检测并提示
✅ 下载中断 → 重试后继续
✅ MD5校验 → 文件损坏提示重新下载
```

---

## 🚀 快速开始

### 1. 准备补丁文件
```bash
# 将你的MPQ补丁复制到服务器
scp patch-ZP1.MPQ root@1.14.59.54:/var/www/html/patches/patches/
```

### 2. 生成MD5
```bash
md5sum /var/www/html/patches/patches/patch-ZP1.MPQ
# 输出: abc123def456  patch-ZP1.MPQ
```

### 3. 更新manifest.json
```bash
nano /var/www/html/patches/manifest.json
# 修改md5、version、size等字段
```

### 4. 测试
```bash
# 在浏览器访问
http://1.14.59.54:8080/patches/manifest.json

# 应该看到JSON格式的补丁清单
```

---

## 📝 注意事项

1. **文件权限**
```bash
chmod -R 755 /var/www/html/patches
chown -R www-data:www-data /var/www/html/patches
```

2. **Nginx端口**
确保8080端口已开放：
```bash
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

3. **补丁命名规范**
```
patch-ZP1.MPQ - 自定义物品
patch-ZP2.MPQ - 机器人系统
patch-ZP3.MPQ - 其他功能
...
patch-ZP9.MPQ - 最后一个可用补丁
```

4. **版本号规则**
```
1.0.0 → 初始版本
1.0.1 → 小更新（修复bug）
1.1.0 → 功能更新
2.0.0 → 大版本更新
```

---

## 🔍 故障排查

### 客户端无法检测到更新
```
检查项：
✅ Nginx是否运行
✅ 8080端口是否开放
✅ manifest.json格式是否正确
✅ 文件权限是否正确
```

### 下载失败
```
检查项：
✅ 补丁文件是否存在
✅ URL是否正确
✅ 文件大小是否匹配
✅ MD5是否正确
```

---

## 📞 支持

如有问题，请检查：
1. Nginx日志：/var/log/nginx/error.log
2. 登录器日志：launcher.log
3. 网络连接：ping 1.14.59.54
