# 补丁系统部署指南（鸽子命版本）

## 🎯 服务器信息

```
服务器IP: 1.14.59.54
协议: HTTP
端口: 8080
补丁目录: /var/www/html/patches/
```

---

## 📁 服务器目录结构

```
/var/www/html/patches/
├── patch-info.json      ← 补丁信息文件（必需）
├── patch-ZP1.MPQ        ← 补丁文件
└── README.txt           ← 说明文档（可选）
```

---

## 📋 patch-info.json 格式

```json
{
  "version": "1.0.0",
  "patch_file": "patch-ZP1.MPQ",
  "download_url": "http://1.14.59.54:8080/patches/patch-ZP1.MPQ",
  "file_size": 10240,
  "md5": "abc123def456...",
  "required": true,
  "description": "补丁描述",
  "changelog": [
    "更新1",
    "更新2"
  ],
  "min_client_version": "3.3.5a",
  "release_date": "2026-03-23"
}
```

---

## 🚀 快速部署

### 1. 生成MD5校验码

```bash
# Linux/Mac
md5sum /var/www/html/patches/patch-ZP1.MPQ

# 输出示例：
# abc123def456...  patch-ZP1.MPQ
```

### 2. 更新patch-info.json

```bash
nano /var/www/html/patches/patch-info.json

# 修改以下字段：
# - version: 新版本号（如 1.0.1）
# - md5: 刚才生成的MD5值
# - file_size: 文件大小（字节）
# - description: 更新说明
# - changelog: 更新日志
```

### 3. 测试访问

```bash
# 测试补丁信息
curl http://1.14.59.54:8080/patches/patch-info.json

# 测试下载
curl -I http://1.14.59.54:8080/patches/patch-ZP1.MPQ
```

---

## 📝 更新流程

### 新增物品/功能

```
1. 修改服务端数据库
   ↓
2. 制作新的MPQ补丁
   - 使用Ladik's MPQ Editor
   - 添加物品图标等文件
   ↓
3. 计算MD5
   md5sum patch-ZP1.MPQ
   ↓
4. 更新patch-info.json
   - 修改version
   - 修改md5
   - 修改description
   - 添加changelog
   ↓
5. 上传到服务器
   scp patch-ZP1.MPQ root@1.14.59.54:/var/www/html/patches/
   ↓
6. 客户端自动检测更新
```

---

## 🔧 服务器配置

### Python HTTP Server（当前方案）

```bash
# 启动服务
cd /var/www/html
nohup python3 -m http.server 8080 > /dev/null 2>&1 &

# 查看进程
ps aux | grep "http.server"

# 停止服务
pkill -f "http.server"
```

### Nginx（推荐生产环境）

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
        
        # 缓存设置
        location ~* \.(mpq|MPQ)$ {
            add_header Cache-Control "no-cache";
        }
        
        location ~* \.(json|txt)$ {
            add_header Cache-Control "no-cache";
        }
    }
}
```

---

## 🛠️ MPQ补丁制作

### 工具
- **Ladik's MPQ Editor** - Windows
- 下载：https://www.zezula.net/en/mpq/download.html

### 步骤

```
1. 创建工作目录
   mkdir -p patch-temp/Interface/Icons

2. 提取/创建图标文件
   - 使用MPQ Editor打开官方MPQ
   - 提取需要的BLP图标
   - 或创建新的BLP图标

3. 创建MPQ文件
   - MPQ Editor → File → New MPQ
   - 添加文件：Interface/Icons/xxx.blp
   - 保存为：patch-ZP1.MPQ
   - 压缩：Best Compression

4. 测试补丁
   - 复制到WoW客户端Data目录
   - 启动游戏验证

5. 计算MD5
   md5sum patch-ZP1.MPQ

6. 上传服务器
   scp patch-ZP1.MPQ root@1.14.59.54:/var/www/html/patches/
```

---

## ✅ 验证清单

### 服务器端

```bash
# 1. 检查HTTP服务
curl http://1.14.59.54:8080/patches/patch-info.json
# 应该返回JSON格式数据

# 2. 检查文件权限
ls -la /var/www/html/patches/
# 应该显示：-rw-r--r-- 1 root root

# 3. 检查文件大小
stat --format="%s" /var/www/html/patches/patch-ZP1.MPQ
# 应该与patch-info.json中的file_size一致

# 4. 检查MD5
md5sum /var/www/html/patches/patch-ZP1.MPQ
# 应该与patch-info.json中的md5一致
```

### 客户端

```
1. 启动登录器
2. 检查日志文件（launcher.log）
3. 验证补丁下载
4. 验证MD5校验
5. 验证补丁应用
6. 启动游戏测试
```

---

## ⚠️ 常见问题

### 客户端无法检测到更新

```
检查项：
□ HTTP服务是否运行
   ps aux | grep "http.server"

□ 8080端口是否开放
   firewall-cmd --list-ports

□ patch-info.json格式是否正确
   python3 -m json.tool patch-info.json

□ 文件权限是否正确
   chmod 644 /var/www/html/patches/*
```

### MD5校验失败

```
原因：
1. 文件上传不完整
2. 文件被修改
3. MD5值错误

解决：
1. 重新计算MD5
   md5sum patch-ZP1.MPQ

2. 更新patch-info.json
   修改md5字段

3. 重新上传文件
```

### 下载速度慢

```
优化方案：
1. 使用Nginx代替Python HTTP Server
2. 启用gzip压缩
3. 使用CDN加速
4. 增加服务器带宽
```

---

## 📊 版本号规则

```
格式：主版本.功能版本.修复版本

示例：
1.0.0 - 初始版本
1.0.1 - 修复bug
1.1.0 - 新增功能
2.0.0 - 大版本更新

递增规则：
- 修复bug：第三位+1
- 新增功能：第二位+1，第三位归零
- 重大更新：第一位+1，其他归零
```

---

## 📞 技术支持

### 日志文件

```
服务器日志：
/var/log/nginx/access.log
/var/log/nginx/error.log

客户端日志：
launcher.log（登录器日志）
violation.log（违规记录）
```

### 检查命令

```bash
# 检查HTTP服务
systemctl status nginx

# 检查端口
netstat -tlnp | grep 8080

# 检查防火墙
firewall-cmd --list-all

# 检查文件
ls -lh /var/www/html/patches/
```

---

**文档版本：2.0.0**
**最后更新：2026-03-23**
**维护者：鸽子命 + 波波AI**
