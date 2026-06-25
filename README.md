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
| `serve` | 🌐 启动 Web 图形界面 (Streamlit) | Web 浏览器 |

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

# 🌐 启动 Web 图形界面
python bookmind.py serve
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

## 💰 支持项目

如果您觉得 BookMind 有用，欢迎打赏支持开发 ❤️

<p align="center">
  <img src="assets/wechat-pay-qrcode.jpg" alt="微信收款码" width="250"/>
</p>
<p align="center">
  <strong>微信收款</strong> — 您的心意是嘻嘻持续创造的动力 🚀
</p>

## 🤝 贡献

欢迎 PR！请确保：
- 代码通过测试
- 遵循 PEP 8
- 添加必要的文档

## 🧑‍💼 项目管理

本仓库由 **嘻嘻 (Xixi)** 代为维护运营。如有问题欢迎提 Issue。

## 📜 许可

MIT License — 免费使用、修改、分发。
