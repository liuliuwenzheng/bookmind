# 🧠 BookMind — 让每本书都长出知识的翅膀

> **将任何电子书转化为可操作的智慧。** 本地 AI 驱动，无需联网，保护隐私。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LM Studio](https://img.shields.io/badge/LM%20Studio-Ready-green)

---

## ✨ 功能

| 命令 | 功能 | 输出 |
|------|------|------|
| `read` | 📖 阅读并分章节浏览 | 控制台 |
| `summarize` | 📋 AI 生成全书总结 | Markdown 文件 |
| `insights` | 💡 萃取核心洞见与知识 | Markdown 文件 |
| `skill` | 🃏 生成可复用的技能卡片 | Markdown 文件 |

## 🚀 快速开始

### 1. 启动 LM Studio

打开 LM Studio → 加载 `google/gemma-4-e4b` → 点击 **Start Server**（端口 1234）

### 2. 安装依赖

```bash
pip install requests ebooklib beautifulsoup4 lxml PyMuPDF pypdf markdown
```

### 3. 使用 BookMind

```bash
cd bookmind

# 总结一本电子书
python bookmind.py summarize 书籍.epub

# 萃取知识
python bookmind.py insights 书籍.pdf

# 生成技能卡片
python bookmind.py skill 书籍.txt

# 阅读
python bookmind.py read 书籍.epub
```

## 📁 输出示例

运行后会在当前目录生成：
- `书名_总结.md` — 全书核心总结
- `书名_洞见.md` — 知识点萃取
- `书名_技能卡片.md` — 可复用的技能模板

## 🔧 支持格式

| 格式 | 支持度 | 说明 |
|:----:|:------:|------|
| 📄 `TXT` | ✅ 完美 | UTF-8 自动检测 |
| 📘 `EPUB` | ✅ 完美 | 分章节提取 |
| 📕 `PDF` | ✅ 良好 | PyMuPDF / pypdf 双引擎 |
| 📝 `Markdown` | ✅ 完美 | 原生支持 |

## 💰 变现方案

### 当前免费层 ✅
- 本地运行，完全免费
- 无 API 调用费用
- 无限次使用

### Pro 版本（计划中）⭐
```
- Web GUI 界面
- 批量处理多本书
- 知识图谱生成
- Anki 闪卡导出
- 一键发布到 GitHub Pages
```
**定价: ¥29.9 / 永久授权**

### 企业版 🏢
```
- Web API 服务
- 多用户管理
- LDAP/OAuth 集成
- 私有部署支持
- 定制模型微调
```
**定价: ¥999 / 年起**

### 如何购买
1. **GitHub Sponsors** — [赞助获取 Pro 密钥](https://github.com/sponsors/your-username)
2. **爱发电** — [afdian.com](https://afdian.com)
3. **直接转账** — 微信/支付宝（联系作者）

## 🤝 贡献

欢迎 PR！请确保：
- 代码通过测试
- 遵循 PEP 8
- 添加必要的文档

## 📜 许可

MIT License — 免费使用、修改、分发。
Pro 功能需授权密钥。
