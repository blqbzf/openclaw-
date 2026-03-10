# OpenClaw Skills Collection

**个人 OpenClaw Skills 集合**

---

## 📦 **已安装的 Skills**

### 1. model-manager v1.5.0 🛠️

**💰 智能模型路由 - 节省最高 96% API 成本**

**功能：**
- 🎯 自动规划任务路由
- 💰 智能选择高性价比模型
- 📊 实时成本计算
- 🔄 自动模型切换

**测试状态：** ✅ 核心功能可用

**安装位置：** `skills/model-manager/`

**使用方法：**
```bash
cd skills/model-manager

# 规划任务
python3 manage_models.py plan "你的任务"

# 查看模型列表（需要网络）
python3 manage_models.py list
```

**实测效果：**
```
任务：写一个Python脚本
节省：65.3% 💰

Phase 1: Design → claude-3.5-sonnet
Phase 2: Code → gpt-4o-mini (节省96%)
Phase 3: Review → gpt-4o-mini
```

---

## 🚀 **快速开始**

### **安装 Skill**

**方法 1：从本仓库克隆**
```bash
git clone https://github.com/你的用户名/test_1_openclaw.git
cd test_1_openclaw/skills/model-manager
```

**方法 2：复制到 OpenClaw**
```bash
cp -R skills/model-manager ~/.openclaw/skills/
```

### **验证安装**
```bash
cd ~/.openclaw/skills/model-manager
python3 manage_models.py plan "test task"
```

---

## 📊 **Skill 状态**

| Skill | 版本 | 状态 | 测试结果 |
|-------|------|------|---------|
| model-manager | v1.5.0 | ✅ 可用 | 🟢 核心功能正常 |

---

## 🔧 **配置说明**

### **model-manager 配置**

**文件位置：** `~/.openclaw/openclaw.json`

**自动配置模式：**
```bash
python3 manage_models.py enable cheap     # 最大节省
python3 manage_models.py enable balanced  # 平衡模式
python3 manage_models.py enable quality   # 最佳质量
```

**手动配置示例：**
```json
{
  "agents": {
    "defaults": {
      "model": "openrouter/openai/gpt-4o-mini"
    }
  }
}
```

---

## 📝 **使用案例**

### **案例 1：翻译任务**
```bash
python3 manage_models.py plan "翻译这段文字到英文"

推荐：gpt-4o-mini
节省：96%
```

### **案例 2：编码任务**
```bash
python3 manage_models.py plan "debug这个Python错误"

Phase 1: 分析 → claude-3.5-sonnet
Phase 2: 修复 → gpt-4o-mini
节省：75%
```

### **案例 3：复杂任务**
```bash
python3 manage_models.py plan "设计数据库架构"

推荐：claude-3.5-sonnet
节省：35%
```

---

## ⚠️ **已知问题**

### **网络连接问题**
**症状：** `list` 命令失败
**原因：** OpenRouter API SSL 错误
**解决：** 
- 检查网络连接
- 使用 VPN
- 或直接使用 `plan` 命令

---

## 🔄 **更新日志**

### **2026-03-10**
- ✅ 安装 model-manager v1.5.0
- ✅ 测试核心功能
- ✅ 创建使用文档

---

## 📚 **相关资源**

**官方文档：**
- OpenClaw Docs: https://docs.openclaw.ai
- ClawHub: https://clawhub.ai

**Skill 源码：**
- GitHub: https://github.com/openclaw/skills

---

## 🤝 **贡献**

欢迎提交 Issue 和 Pull Request！

---

**维护者：** Fangqu Yang
**更新时间：** 2026-03-10
