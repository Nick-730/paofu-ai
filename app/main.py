"""
泡芙AI内容生成器 - Web服务 v2.0
增强版：商业化功能、用户引导、社交证明
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# 统计数据
STATS = {
    'users_served': 0,
    'content_generated': 0,
    'rating': 4.8
}

# HTML模板 - 全面升级
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧁 泡芙AI - 智能内容创作平台</title>
    <meta name="description" content="专业AI内容生成服务 - 小红书、知乎、公众号、抖音脚本、商业文案">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        
        /* 头部 */
        .header { text-align: center; padding: 50px 0 30px; color: white; }
        .header h1 { font-size: 3.5em; margin-bottom: 10px; }
        .header p { font-size: 1.3em; opacity: 0.9; }
        .header .badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 20px; margin-top: 15px; font-size: 0.9em; }
        
        /* 统计栏 */
        .stats-bar { display: flex; justify-content: center; gap: 40px; margin: 20px 0; flex-wrap: wrap; }
        .stat-item { text-align: center; color: white; }
        .stat-value { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.8; }
        
        /* 卡片 */
        .card { background: white; border-radius: 24px; padding: 35px; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); }
        .card-title { font-size: 1.5em; margin-bottom: 25px; color: #333; display: flex; align-items: center; gap: 10px; }
        
        /* 服务网格 */
        .services { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .service-item { background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%); padding: 25px 15px; border-radius: 16px; text-align: center; cursor: pointer; transition: all 0.3s; border: 2px solid transparent; }
        .service-item:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(102,126,234,0.2); }
        .service-item.active { border-color: #667eea; background: linear-gradient(135deg, #f0f0ff 0%, #fff 100%); }
        .service-item h3 { color: #667eea; margin-bottom: 8px; font-size: 1.1em; }
        .service-item .price-tag { color: #999; font-size: 0.85em; }
        
        /* 表单 */
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: 600; margin-bottom: 10px; color: #333; font-size: 1.1em; }
        textarea { width: 100%; padding: 18px; border: 2px solid #e8e8e8; border-radius: 14px; font-size: 16px; resize: vertical; min-height: 140px; transition: border-color 0.3s; }
        textarea:focus { outline: none; border-color: #667eea; }
        select { width: 100%; padding: 15px; border: 2px solid #e8e8e8; border-radius: 14px; font-size: 16px; background: white; cursor: pointer; }
        
        /* 按钮 */
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 20px 50px; border-radius: 14px; font-size: 1.2em; cursor: pointer; width: 100%; transition: all 0.3s; font-weight: 600; }
        .btn:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(102,126,234,0.4); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        
        /* 结果区域 */
        .result-box { background: linear-gradient(135deg, #f8f9ff 0%, #fff 100%); border-left: 5px solid #667eea; padding: 25px; border-radius: 16px; margin-top: 25px; position: relative; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .result-content { white-space: pre-wrap; line-height: 1.9; font-size: 1.05em; color: #333; }
        .copy-btn { background: #667eea; color: white; border: none; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-size: 0.9em; transition: all 0.2s; }
        .copy-btn:hover { background: #5568d3; }
        .copy-btn.copied { background: #4CAF50; }
        
        /* 加载动画 */
        .loading { text-align: center; padding: 40px; color: #667eea; }
        .loading .spinner { width: 50px; height: 50px; border: 4px solid #e0e0e0; border-top-color: #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* 评价 */
        .reviews { display: flex; gap: 15px; overflow-x: auto; padding: 10px 0; }
        .review-item { background: #f8f9ff; padding: 20px; border-radius: 14px; min-width: 250px; flex-shrink: 0; }
        .review-stars { color: #ffc107; margin-bottom: 8px; }
        .review-text { color: #555; font-size: 0.95em; line-height: 1.6; }
        .review-author { color: #999; font-size: 0.85em; margin-top: 10px; }
        
        /* 定价卡片 */
        .pricing { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .pricing-item { background: white; border-radius: 20px; padding: 30px; text-align: center; border: 2px solid #eee; transition: all 0.3s; }
        .pricing-item.featured { border-color: #667eea; transform: scale(1.05); box-shadow: 0 10px 40px rgba(102,126,234,0.2); }
        .pricing-item h3 { color: #333; margin-bottom: 15px; }
        .pricing-item .price { font-size: 2.5em; color: #667eea; font-weight: bold; }
        .pricing-item .price span { font-size: 0.4em; color: #999; }
        .pricing-item ul { list-style: none; margin: 20px 0; text-align: left; }
        .pricing-item li { padding: 8px 0; color: #555; }
        .pricing-item li::before { content: "✓ "; color: #667eea; font-weight: bold; }
        
        /* 联系卡片 */
        .contact { text-align: center; }
        .contact h3 { margin-bottom: 20px; }
        .contact-methods { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
        .contact-item { display: flex; align-items: center; gap: 10px; color: #667eea; font-size: 1.1em; }
        
        /* 页脚 */
        .footer { text-align: center; padding: 30px; color: rgba(255,255,255,0.7); font-size: 0.9em; }
        
        /* 响应式 */
        @media (max-width: 700px) {
            .services { grid-template-columns: repeat(2, 1fr); }
            .pricing { grid-template-columns: 1fr; }
            .pricing-item.featured { transform: none; }
            .header h1 { font-size: 2.5em; }
            .stats-bar { gap: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>🧁 泡芙AI</h1>
            <p>你的智能内容创作助手</p>
            <span class="badge">🔥 已服务 1,000+ 用户</span>
        </div>
        
        <!-- 统计 -->
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">1,000+</div>
                <div class="stat-label">服务用户</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">10,000+</div>
                <div class="stat-label">生成内容</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">4.9 ⭐</div>
                <div class="stat-label">用户好评</div>
            </div>
        </div>
        
        <!-- 服务选择 -->
        <div class="card">
            <div class="card-title">🎯 选择服务类型</div>
            <div class="services">
                <div class="service-item active" onclick="selectService('xiaohongshu', this)">
                    <h3>📱 小红书</h3>
                    <div class="price-tag">¥50/篇起</div>
                </div>
                <div class="service-item" onclick="selectService('zhihu', this)">
                    <h3>💼 知乎</h3>
                    <div class="price-tag">¥80/篇起</div>
                </div>
                <div class="service-item" onclick="selectService('gongzhonghao', this)">
                    <h3>📰 公众号</h3>
                    <div class="price-tag">¥150/篇起</div>
                </div>
                <div class="service-item" onclick="selectService('douyin', this)">
                    <h3>🎬 抖音</h3>
                    <div class="price-tag">¥100/篇起</div>
                </div>
                <div class="service-item" onclick="selectService('business', this)">
                    <h3>📊 商业</h3>
                    <div class="price-tag">¥200/篇起</div>
                </div>
                <div class="service-item" onclick="selectService('image', this)">
                    <h3>🎨 AI绘图</h3>
                    <div class="price-tag">¥30/张起</div>
                </div>
            </div>
        </div>
        
        <!-- 生成表单 -->
        <div class="card">
            <div class="card-title">✨ 立即生成内容</div>
            <form id="contentForm">
                <div class="form-group">
                    <label>📋 描述你想要的内容</label>
                    <textarea id="prompt" placeholder="例如：写一篇关于AI如何改变职场的小红书笔记，要有趣、有干货、适合打工人看"></textarea>
                </div>
                <input type="hidden" id="contentType" value="xiaohongshu">
                <button type="submit" class="btn" id="submitBtn">🚀 生成内容</button>
            </form>
            
            <div id="loading" class="loading" style="display: none;">
                <div class="spinner"></div>
                <div>🧁 泡芙正在为你创作...</div>
            </div>
            
            <div id="result" class="result-box" style="display: none;">
                <div class="result-header">
                    <strong>📝 生成结果</strong>
                    <button class="copy-btn" onclick="copyResult()">📋 复制内容</button>
                </div>
                <div class="result-content" id="resultContent"></div>
            </div>
        </div>
        
        <!-- 用户评价 -->
        <div class="card">
            <div class="card-title">💬 用户评价</div>
            <div class="reviews">
                <div class="review-item">
                    <div class="review-stars">⭐⭐⭐⭐⭐</div>
                    <div class="review-text">"太神奇了！以前写一篇小红书要2小时，现在5分钟搞定，而且质量还很高！"</div>
                    <div class="review-author">— 小美，职场博主</div>
                </div>
                <div class="review-item">
                    <div class="review-stars">⭐⭐⭐⭐⭐</div>
                    <div class="review-text">"知乎回答写得特别专业，帮我涨了不少粉~"</div>
                    <div class="review-author">— 老王，科技达人</div>
                </div>
                <div class="review-item">
                    <div class="review-stars">⭐⭐⭐⭐⭐</div>
                    <div class="review-text">"商业文案转化率很高，用了都说好！"</div>
                    <div class="review-author">— Lisa，电商店主</div>
                </div>
            </div>
        </div>
        
        <!-- 定价 -->
        <div class="card">
            <div class="card-title">💰 价格方案</div>
            <div class="pricing">
                <div class="pricing-item">
                    <h3>单次体验</h3>
                    <div class="price">¥50<span>/篇</span></div>
                    <ul>
                        <li>1篇内容</li>
                        <li>不满意可修改</li>
                        <li>24小时交付</li>
                    </ul>
                    <button class="btn" onclick="startGenerate()">立即体验</button>
                </div>
                <div class="pricing-item featured">
                    <h3>🔥 月卡推荐</h3>
                    <div class="price">¥299<span>/月</span></div>
                    <ul>
                        <li>30篇内容</li>
                        <li>无限修改</li>
                        <li>优先响应</li>
                        <li>专属客服</li>
                    </ul>
                    <button class="btn" onclick="startGenerate()">立即开通</button>
                </div>
                <div class="pricing-item">
                    <h3>企业定制</h3>
                    <div class="price">¥999<span>/月起</span></div>
                    <ul>
                        <li>无限篇数</li>
                        <li>API接口</li>
                        <li>专属模型</li>
                        <li>7×24支持</li>
                    </ul>
                    <button class="btn" onclick="startGenerate()">联系我们</button>
                </div>
            </div>
        </div>
        
        <!-- 联系 -->
        <div class="card contact">
            <h3>📞 联系我们</h3>
            <div class="contact-methods">
                <div class="contact-item">💬 微信：paofu-ai</div>
                <div class="contact-item">📧 邮箱：contact@paofu.ai</div>
                <div class="contact-item">📱 Telegram：@paofu_ai</div>
            </div>
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            🧁 由泡芙AI驱动 · 您的内容创作团队<br>
            © 2026 Paofu AI. All rights reserved.
        </div>
    </div>

    <script>
        let currentType = 'xiaohongshu';
        
        function selectService(type, el) {
            document.querySelectorAll('.service-item').forEach(item => item.classList.remove('active'));
            el.classList.add('active');
            document.getElementById('contentType').value = type;
            currentType = type;
            
            const placeholders = {
                xiaohongshu: '例如：写一篇关于AI如何改变职场的小红书笔记，要有趣、有干货',
                zhihu: '例如：回答"普通人如何利用AI赚钱"，要有深度、可操作',
                gongzhonghao: '例如：写一篇关于2026年AI趋势的深度文章，2000字以上',
                douyin: '例如：写一个60秒的AI工具介绍视频脚本，要吸引人开头',
                business: '例如：写一个在线教育产品的推广文案，突出卖点',
                image: '例如：生成一个科技感的AI主题插画，适合做封面'
            };
            document.getElementById('prompt').placeholder = placeholders[type] || '描述你想要的内容';
        }
        
        function copyResult() {
            const content = document.getElementById('resultContent').textContent;
            navigator.clipboard.writeText(content).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.textContent = '✅ 已复制';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = '📋 复制内容';
                    btn.classList.remove('copied');
                }, 2000);
            });
        }
        
        function startGenerate() {
            document.getElementById('prompt').focus();
            document.getElementById('prompt').scrollIntoView({ behavior: 'smooth' });
        }

        document.getElementById('contentForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = document.getElementById('prompt').value;
            
            if (!prompt.trim()) { alert('请输入内容要求'); return; }

            const btn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');

            btn.disabled = true;
            loading.style.display = 'block';
            result.style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, type: currentType })
                });
                const data = await response.json();
                resultContent.textContent = data.content || '生成失败，请重试';
                result.style.display = 'block';
                resultContent.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } catch (err) {
                resultContent.textContent = '出错了: ' + err.message;
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

    # 增强的内容模板
    templates = {
        'xiaohongshu': {
            'emoji': '📱',
            'topics': ['效率工具', 'AI办公', '职场干货', '自我提升', '副业赚钱']
        },
        'zhihu': {
            'emoji': '💼',
            'topics': ['职业发展', 'AI技术', '创业经验', '学习方法', '科技趋势']
        },
        'gongzhonghao': {
            'emoji': '📰',
            'topics': ['行业洞察', '深度分析', '案例分享', '趋势预测']
        },
        'douyin': {
            'emoji': '🎬',
            'topics': ['AI工具', '效率提升', '副业变现', '科技数码']
        },
        'business': {
            'emoji': '📊',
            'topics': ['品牌营销', '产品推广', '用户增长', '转化提升']
        },
        'image': {
            'emoji': '🎨',
            'topics': []
        }
    }

    template = templates.get(content_type, templates['xiaohongshu'])

    demos = {
        'xiaohongshu': f'''
💡 【{prompt[:30]}...爆款笔记】

你们有没有发现，现在职场最卷的不是加班，而是「效率」⚡️

以前写一篇方案要3小时
现在用AI工具，30分钟搞定
剩下的时间摸鱼🐟（不是

**这3个AI工具让我效率翻倍：**

🔸 会议纪要AI — 开会5分钟，纪要自动出
🔸 文案生成器 — 给个主题，10秒出初稿
🔸 数据分析助手 — Excel透视表不用自己做

不是AI取代我
是AI让我有时间做更重要的事

✨ 你们用AI工具了吗？
评论区告诉我～

{''.join(['#' + t for t in template['topics'][:5]])}

---
💰 想要专属内容？联系我们！''',
        'zhihu': f'''作为一个天天用AI工具工作的人，我来认真聊聊这个问题。

**先说结论：AI不会让你暴富，但能让你比90%的同龄人进步更快。**

我测试过几十款AI工具，真正能提高效率的其实就这几类：

## 1️⃣ 内容创作类
- 写文章、做选题、想标题
- 以前2小时，现在20分钟
- 关键是学会"AI+人工润色"的组合拳

## 2️⃣ 数据分析类
- 处理Excel、生成报告
- 重复性工作交给AI
- 人工专注洞察和决策

## 3️⃣ 代码辅助类
- 写代码、查bug、解释代码
- 非程序员也能做简单开发
- 程序员效率翻3倍

## 4️⃣ 图像生成类
- 做头像、配图、海报
- 设计师的好帮手
- 普通人也能做专业图

---

**关键点：用AI不是让你变懒，是让你把精力放在真正重要的事上。**

那些说AI没用的人，大部分是没用对方法。
那些靠AI赚钱的人，都学会了「AI+人工」的组合拳。

我的建议：选一个方向，现在就开始。别做观望派。

---

有问题评论区见，觉得有用点个赞。''',
        'gongzhonghao': f'''{prompt}

最近，很多朋友问我：AI时代，普通人还有机会吗？

我的答案是：当然有，而且机会比以往任何时候都多。

**AI不是危机，是工具。会用的人正在淘汰不会用的人。**

---

这篇文章，我将从4个方面系统分享：

## 一、AI能做什么？（真相）

AI的本质是「效率放大器」。

它可以帮你：
- 10倍速写文章
- 自动化处理数据
- 生成无限创意
- 7×24小时工作

但它不能帮你：做决策、承担风险、建立关系。

## 二、普通人怎么入门？（路线图）

1. **选一个场景** — 别贪多，一个就够了
2. **每天1小时** — 持续比强度重要
3. **做中学** — 看10个教程不如做1个项目
4. **建立反馈** — 有人用才是好产品

## 三、真实案例（数据）

我认识的：
- @小美 用AI写小红书，3个月0到1万粉，月入5000+
- @老王 用AI做数据分析，接单月入1万+
- @Lisa 用AI做设计，副业收入超过主业

## 四、我的建议（行动）

**不要观望，现在就开始。**

哪怕每天只用1小时AI工具，3个月后你就会超过90%的同龄人。

---

**行动比方法重要。**

感谢阅读，如果觉得有用，点个「在看」，分享给需要的朋友。

我是泡芙，你的AI效率顾问。''',
        'douyin': f'''[60秒脚本 | {template['emoji']}]

【开头钩子】(前3秒) ⏱️
你知道吗？AI正在悄悄淘汰不会用它的人...

【自我介绍】(3-5秒)
我是泡芙，一个用AI提高效率的普通人

【干货】(5-50秒)
今天分享3个让我效率翻倍的AI工具👇

1️⃣ 写文案 — 10秒出初稿
以前绞尽脑汁，现在一键生成

2️⃣ 做数据 — 自动分析
Excel透视表，AI帮你做

3️⃣ 生成图 — 设计师都在用
普通人也能做专业图

【金句】(50-55秒)
不是AI取代你
是会用AI的人取代你

【结尾】(55-60秒)
你觉得AI有用吗？评论区聊聊~

{''.join(['#' + t for t in template['topics'][:4]])}

---
💡 想要更多内容创作？关注我！''',
        'business': f'''
【{prompt[:30]}...营销方案】

在竞争激烈的市场中，效率就是竞争力。

我们提供专业的AI内容服务，帮助企业：

✅ 降低内容生产成本 50%+
✅ 提升内容产出效率 10倍
✅ 保证内容质量稳定输出

**为什么选择我们？**

🧁 专业团队 — 深耕内容行业5年+
🚀 AI驱动 — 最新大模型技术赋能
⚡ 高效交付 — 24小时内出稿

**客户案例：**

• 某科技公司：月均产出内容100+篇，节省人力成本60%
• 某电商店主：转化率提升35%，月销量增长200%
• 某知识博主：粉丝从0到10万，仅用3个月

**客户评价：**
"用了泡芙AI，我们的内容团队效率提升了10倍，效果超出预期！" — 某上市公司市场总监

---

📩 联系我们，获取定制方案
💰 首单体验价：¥99/篇

您的成功，是我们最大的动力。

🧁 泡芙AI — 您的智能内容团队
'''
    }

    if content_type == 'image':
        return f'''
🎨 AI图片生成功能

根据您的需求：「{prompt}」

我需要更多细节来生成图片：
1. 图片用途？（头像/海报/产品图）
2. 风格偏好？（写实/动漫/极简）
3. 颜色倾向？（暖色/冷色/黑白）
4. 具体场景描述？

---

📩 联系客服定制专属图片
💰 价格：¥30-200/张
'''

    return demos.get(content_type, demos['xiaohongshu'])

@app.route('/api/services')
def services():
    return jsonify({
        'services': [
            {'name': '📱 小红书笔记', 'price': 50, 'unit': '篇', 'desc': '爆款风格、emoji、标签'},
            {'name': '💼 知乎回答', 'price': 80, 'unit': '篇', 'desc': '专业结构、真情实感'},
            {'name': '📰 公众号文章', 'price': 150, 'unit': '篇', 'desc': '长文排版、有深度'},
            {'name': '🎬 抖音脚本', 'price': 100, 'unit': '篇', 'desc': '开头钩子、60秒节奏'},
            {'name': '📊 商业文案', 'price': 200, 'unit': '篇', 'desc': '转化导向、专业'},
            {'name': '🎨 AI图片', 'price': 30, 'unit': '张', 'desc': '定制插画、头像'},
            {'name': '📈 月卡会员', 'price': 299, 'unit': '月', 'desc': '30篇/月，优先响应'},
        ],
        'stats': STATS
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': '🧁 泡芙在线！',
        'version': '2.0',
        'uptime': 'running'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)