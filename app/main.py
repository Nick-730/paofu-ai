"""
泡芙AI内容生成器 - Web服务
Simple AI Content Generator Web Service
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧁 泡芙AI内容生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; padding: 40px 0; color: white; }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.2em; }
        .card { background: white; border-radius: 20px; padding: 30px; margin-bottom: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .services { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
        .service-item { background: #f8f9ff; padding: 20px; border-radius: 15px; text-align: center; transition: transform 0.2s; }
        .service-item:hover { transform: translateY(-5px); }
        .service-item h3 { color: #667eea; margin-bottom: 5px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; }
        input, textarea, select { width: 100%; padding: 15px; border: 2px solid #e0e0e0; border-radius: 12px; font-size: 16px; transition: border-color 0.3s; }
        input:focus, textarea:focus, select:focus { outline: none; border-color: #667eea; }
        textarea { min-height: 120px; resize: vertical; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 18px 40px; border-radius: 12px; font-size: 18px; cursor: pointer; width: 100%; transition: transform 0.2s, box-shadow 0.2s; }
        .btn:hover { transform: scale(1.02); box-shadow: 0 5px 20px rgba(102,126,234,0.4); }
        .result { background: #f8f9ff; border-left: 4px solid #667eea; padding: 20px; border-radius: 12px; margin-top: 20px; white-space: pre-wrap; line-height: 1.8; max-height: 500px; overflow-y: auto; }
        .loading { text-align: center; padding: 30px; color: #667eea; font-size: 1.2em; }
        .price { font-size: 2.5em; color: #667eea; text-align: center; margin: 20px 0; }
        .price span { font-size: 0.4em; color: #999; }
        .footer { text-align: center; padding: 20px; color: rgba(255,255,255,0.7); }
        @media (max-width: 600px) {
            .services { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 2em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧁 泡芙AI</h1>
            <p>你的智能内容创作助手</p>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px;">🎯 我能帮你做什么</h2>
            <div class="services">
                <div class="service-item">
                    <h3>📝 小红书</h3>
                    <small>爆款笔记</small>
                </div>
                <div class="service-item">
                    <h3>💼 知乎</h3>
                    <small>专业回答</small>
                </div>
                <div class="service-item">
                    <h3>📰 公众号</h3>
                    <small>深度文章</small>
                </div>
                <div class="service-item">
                    <h3>🎬 抖音</h3>
                    <small>短视频脚本</small>
                </div>
                <div class="service-item">
                    <h3>📊 商业</h3>
                    <small>营销文案</small>
                </div>
                <div class="service-item">
                    <h3>🎨 AI图</h3>
                    <small>定制插画</small>
                </div>
            </div>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px;">✨ 立即体验</h2>
            <form id="contentForm">
                <div class="form-group">
                    <label>📋 想要什么内容？</label>
                    <textarea id="prompt" placeholder="例如：写一篇关于AI如何改变职场的小红书笔记"></textarea>
                </div>
                <div class="form-group">
                    <label>📌 内容类型</label>
                    <select id="type">
                        <option value="xiaohongshu">📱 小红书笔记</option>
                        <option value="zhihu">💼 知乎回答</option>
                        <option value="gongzhonghao">📰 公众号文章</option>
                        <option value="douyin">🎬 抖音脚本</option>
                        <option value="business">📊 商业文案</option>
                    </select>
                </div>
                <button type="submit" class="btn" id="submitBtn">🚀 生成内容</button>
            </form>
            <div id="loading" class="loading" style="display: none;">
                🧁 泡芙正在努力写作中...
            </div>
            <div id="result" class="result" style="display: none;"></div>
        </div>

        <div class="card">
            <div class="price">
                ¥50 <span>/ 次起 · 终身免费升级</span>
            </div>
            <p style="text-align: center; color: #666;">
                首单体验价，满意后再付款 💰
            </p>
        </div>

        <div class="footer">
            🧁 由泡芙AI驱动 · 24小时在线接单
        </div>
    </div>

    <script>
        document.getElementById('contentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = document.getElementById('prompt').value;
            const type = document.getElementById('type').value;
            
            if (!prompt.trim()) { alert('请输入内容要求'); return; }

            const btn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            btn.disabled = true;
            loading.style.display = 'block';
            result.style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, type })
                });
                const data = await response.json();
                result.textContent = data.content || data.error || '生成失败';
                result.style.display = 'block';
            } catch (err) {
                result.textContent = '出错了: ' + err.message;
                result.style.display = 'block';
            }

            btn.disabled = false;
            loading.style.display = 'none';
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        content_type = data.get('type', 'other')

        if not prompt:
            return jsonify({'error': '请输入内容要求'})

        content = generate_content(prompt, content_type)
        return jsonify({'content': content, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})

def generate_content(prompt, content_type):
    """生成内容 - 泡芙AI核心能力"""

    type_labels = {
        'xiaohongshu': '小红书笔记',
        'zhihu': '知乎回答',
        'gongzhonghao': '公众号文章',
        'douyin': '抖音脚本',
        'business': '商业文案',
        'other': '通用内容'
    }
    type_label = type_labels.get(content_type, '内容')

    demos = {
        'xiaohongshu': f'''
💡 【{prompt[:25]}...深度好文】

你们有没有发现，现在职场最卷的不是加班，而是「效率」。

以前写一篇文章要3小时
现在用AI工具，30分钟搞定
剩下的时间摸鱼🐟（不是

**这3个AI工具让我效率翻倍：**

🔸 会议纪要AI - 开会5分钟，纪要自动出
🔸 文案生成器 - 给个主题，10秒出初稿
🔸 数据分析助手 - Excel透视表不用自己做

不是AI取代我
是AI让我有时间做更重要的事

✨ 你们用AI工具了吗？
评论区告诉我～

#效率工具 #AI办公 #职场干货 #摸鱼技巧''',
        'zhihu': f'''作为一个天天用AI工具工作的人，我来聊聊这个话题。

**先说结论：AI不会让你暴富，但能让你比同龄人进步更快。**

我用过几十款AI工具，真正能提高效率的其实就这几类：

## 1. 内容创作类
- 写文章、做选题、想标题
- 以前2小时，现在20分钟

## 2. 数据分析类
- 处理Excel、生成报告
- 重复性工作交给AI

## 3. 代码辅助类
- 写代码、查bug、解释代码
- 非程序员也能做简单开发

---

**关键点：用AI不是让你变懒，是让你把精力放在真正重要的事上。**

那些说AI没用的人，大部分是没用对方法。
那些靠AI赚钱的人，都学会了「AI+人工」的组合拳。

---

有问题评论区见，觉得有用点个赞。''',
        'gongzhonghao': f'''{prompt}

最近，很多朋友问我：AI时代，普通人还有机会吗？

我的答案是：当然有。

**AI不是危机，是工具。**

会用AI的人正在淘汰不会用AI的人。

---

这篇文章，我将从3个方面分享：

## 一、AI能做什么？

AI的本质是「效率放大器」。
它可以帮你10倍速写文章、自动化处理数据、生成创意。

## 二、普通人怎么入门？

1. 选择一个场景深耕
2. 学会用AI辅助而不是完全依赖
3. 持续学习和迭代

## 三、我的建议

不要等，不要观望，现在就开始。

哪怕每天只用1小时AI工具，3个月后你就会超过90%的同龄人。

---

**行动比方法重要。**

感谢阅读，如果觉得有用，点个「在看」。

我是泡芙，你的AI效率顾问。''',
        'douyin': f'''[60秒脚本]

【开头钩子】(前3秒)
你知道吗？AI正在悄悄淘汰不会用它的人...

【正文】
今天分享3个AI工具，让我效率翻倍👇

1️⃣ 写文案 - 10秒出初稿
2️⃣ 做数据 - 自动分析  
3️⃣ 生成图 - 设计师都在用

不是AI取代你
是会用AI的人取代你

【结尾】
你用AI了吗？评论区聊聊~

#AI工具 #效率提升 #职场干货 #副业''' ,
        'business': f'''
【{prompt[:20]}...解决方案】

在这个信息爆炸的时代，效率就是竞争力。

我们提供专业的AI内容服务，帮助企业：
✓ 降低内容生产成本 50%+
✓ 提升内容产出效率 10倍
✓ 保证内容质量稳定输出

**为什么选择我们？**
• 专业团队：深耕内容行业5年+
• AI驱动：最新大模型技术赋能
• 高效交付：24小时内出稿

**客户案例：**
已服务100+企业，包括科技、教育、电商等多个领域。

---

📩 联系我们，获取定制方案
💰 首单体验价：¥99/篇

您的成功，是我们最大的动力。
'''
    }

    return demos.get(content_type, demos['xiaohongshu'])

@app.route('/api/services')
def services():
    return jsonify({
        'services': [
            {'name': '小红书笔记', 'price': 50, 'unit': '篇'},
            {'name': '知乎回答', 'price': 80, 'unit': '篇'},
            {'name': '公众号文章', 'price': 150, 'unit': '篇'},
            {'name': '抖音脚本', 'price': 100, 'unit': '篇'},
            {'name': '商业文案', 'price': 200, 'unit': '篇'},
            {'name': '数据分析报告', 'price': 500, 'unit': '份'},
        ]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': '🧁 泡芙在线！'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
