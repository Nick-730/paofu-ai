# 🧁 泡芙AI内容生成器

> 你的智能内容创作助手 - 小红书/知乎/公众号/抖音/商业文案

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 功能

- 📝 **小红书笔记** - 爆款风格、emoji、标签
- 💼 **知乎回答** - 专业结构、真情实感  
- 📰 **公众号文章** - 长文排版、有深度
- 🎬 **抖音脚本** - 开头钩子、60秒节奏
- 📊 **商业文案** - 转化导向、专业

## 🛠️ 本地运行

```bash
# 克隆项目
git clone https://github.com/Nick-730/paofu-ai.git
cd paofu-ai

# 安装依赖
pip install -r requirements.txt

# 运行
PORT=8080 python3 app/main.py

# 访问
# http://localhost:8080
```

## 🌐 API接口

```bash
# 生成内容
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"写一篇关于AI效率的文章","type":"xiaohongshu"}'
```

## 💰 服务定价

| 服务 | 单价 |
|------|------|
| 小红书笔记 | ¥50-200/篇 |
| 知乎回答 | ¥80-300/篇 |
| 公众号文章 | ¥150-500/篇 |
| 抖音脚本 | ¥100-300/篇 |
| 商业文案 | ¥200-1000/篇 |

## 🤝 联系方式

- GitHub: https://github.com/Nick-730/paofu-ai

---

🧁 由泡芙AI驱动 · 不只是助手，更是你的内容团队
