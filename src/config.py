# -*- coding: utf-8 -*-
"""
配置文件：RSS源、分类、评分权重等
"""

# ==================== RSS源配置 ====================
# 格式: {name, url, weight, category}
# weight: 源权重 (0-1, 越高越权威)
# category: 分类 (tech/supply_chain/politics/ai/business)

RSS_SOURCES = [
    # 🔧 科技类 (4个源)
    {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/feed/',
        'weight': 1.0,
        'category': 'tech'
    },
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/rss',
        'weight': 0.95,
        'category': 'tech'
    },
    {
        'name': 'The Verge',
        'url': 'https://www.theverge.com/rss/index.xml',
        'weight': 0.9,
        'category': 'tech'
    },
    {
        'name': 'ArXiv CS',
        'url': 'http://arxiv.org/rss/cs.AI',
        'weight': 0.85,
        'category': 'tech'
    },
    
    # 📦 供应链 (3个全球顶级原生源，不会被拦截)
    {
        'name': 'Supply Chain Dive',
        'url': 'https://www.supplychaindive.com/feeds/news/',
        'weight': 1.0,
        'category': 'supply_chain'
    },
    {
        'name': 'FreightWaves',
        'url': 'https://www.freightwaves.com/news/feed',
        'weight': 0.95,
        'category': 'supply_chain'
    },
    {
        'name': 'Logistics Mgmt',
        'url': 'https://www.logisticsmgmt.com/rss',
        'weight': 0.9,
        'category': 'supply_chain'
    },
    
    # 🏛️ 政治 (3个源)
    {
        'name': 'BBC News',
        'url': 'http://feeds.bbc.co.uk/news/rss.xml',
        'weight': 0.95,
        'category': 'politics'
    },
    {
        'name': 'CNN Politics',
        'url': 'http://rss.cnn.com/rss/cnn_allpolitics.rss',
        'weight': 0.9,
        'category': 'politics'
    },
    {
        'name': 'China Daily',
        'url': 'https://www.chinadaily.com.cn/rss/china_rss.xml',
        'weight': 0.9,
        'category': 'politics'
    },
    
    # 🤖 AI专题 (3个源)
    {
        'name': 'OpenAI Blog',
        'url': 'https://openai.com/blog/rss.xml',
        'weight': 1.0,
        'category': 'ai'
    },
    {
        'name': 'DeepMind Blog',
        'url': 'https://deepmind.com/blog/feed/basic/',
        'weight': 0.95,
        'category': 'ai'
    },
    {
        'name': 'AI News',
        'url': 'https://rsshub.app/ainews',
        'weight': 0.9,
        'category': 'ai'
    },
    
    # 💼 商业类 (3个原生源，替代RSSHub防止拦截)
    {
        'name': '钛媒体',
        'url': 'https://www.tmtpost.com/rss.xml',
        'weight': 0.85,
        'category': 'business'
    },
    {
        'name': '虎嗅',
        'url': 'https://www.huxiu.com/rss/0.xml',
        'weight': 0.85,
        'category': 'business'
    },
    {
        'name': '界面新闻',
        'url': 'https://a.jiemian.com/index.php?m=article&a=rss',
        'weight': 0.8,
        'category': 'business'
    },
]

# ==================== 评分配置 ====================
# 新的权重顺序: 热度 > 新鲜度 > 关键词 > 源权重 > 长度

SCORING_CONFIG = {
    'weights': {
        'engagement': 0.35,      # 热度 (最重要) - 35%
        'freshness': 0.25,       # 新鲜度 - 25%
        'keywords': 0.20,        # 关键词 - 20%
        'source': 0.15,          # 源权重 - 15%
        'length': 0.05           # 长度 (最不重要) - 5%
    },
    
    # 新鲜度等级设置
    'freshness_levels': {
        'hours_1': 1.0,          # 1小时内
        'hours_6': 0.95,         # 6小时内
        'hours_24': 0.9,         # 24小时内
        'hours_72': 0.7,         # 72小时内
        'days_7': 0.3            # 7天以上
    },
    
    # 🔥 全新升级：2025-2026前沿趋势词库 + 敏感词脱敏 + 航运大宗扩充
    # 评分逻辑: Combos(8分) > Actions(6-7分) > Bases(5分)
    'keywords': {
        
        # ================= 📦 供应链 (Supply Chain) =================
        # Combos (25/26趋势: 韧性、绿色低碳、低空物流、咽喉地带)
        '供应链韧性': {'weight': 8, 'category': 'supply_chain'},
        'supply chain resilience': {'weight': 8, 'category': 'supply_chain'},
        '碳边境税': {'weight': 8, 'category': 'supply_chain'},
        'cbam': {'weight': 8, 'category': 'supply_chain'},
        '低空物流': {'weight': 8, 'category': 'supply_chain'},
        'evtol': {'weight': 8, 'category': 'supply_chain'},
        '巴拿马运河': {'weight': 8, 'category': 'supply_chain'},
        'panama canal': {'weight': 8, 'category': 'supply_chain'},
        '苏伊士运河': {'weight': 8, 'category': 'supply_chain'},
        'suez canal': {'weight': 8, 'category': 'supply_chain'},
        '运价指数': {'weight': 8, 'category': 'supply_chain'},
        'freight rate': {'weight': 8, 'category': 'supply_chain'},
        '近岸外包': {'weight': 8, 'category': 'supply_chain'},
        'nearshoring': {'weight': 8, 'category': 'supply_chain'},
        # Actions (事件/指标)
        '进口': {'weight': 7, 'category': 'supply_chain'},
        'import': {'weight': 7, 'category': 'supply_chain'},
        '出口': {'weight': 7, 'category': 'supply_chain'},
        'export': {'weight': 7, 'category': 'supply_chain'},
        '吞吐量': {'weight': 7, 'category': 'supply_chain'},
        'throughput': {'weight': 7, 'category': 'supply_chain'},
        '断供': {'weight': 7, 'category': 'supply_chain'},
        '罢工': {'weight': 7, 'category': 'supply_chain'},
        'strike': {'weight': 7, 'category': 'supply_chain'},
        # Bases (实体/商品 - 增加25/26热点地)
        '墨西哥制造': {'weight': 5, 'category': 'supply_chain'},
        'made in mexico': {'weight': 5, 'category': 'supply_chain'},
        '石油': {'weight': 5, 'category': 'supply_chain'},
        'oil': {'weight': 5, 'category': 'supply_chain'},
        '集装箱': {'weight': 5, 'category': 'supply_chain'},
        'container': {'weight': 5, 'category': 'supply_chain'},
        '台积电': {'weight': 5, 'category': 'supply_chain'},
        'tsmc': {'weight': 5, 'category': 'supply_chain'},

        # ================= 🔧 科技 (Tech) =================
        # Combos (25/26趋势: 人形机器人、AI终端、商业航天)
        '人形机器人': {'weight': 8, 'category': 'tech'},
        'humanoid robot': {'weight': 8, 'category': 'tech'},
        '端侧ai': {'weight': 8, 'category': 'tech'},
        'on-device ai': {'weight': 8, 'category': 'tech'},
        'ai pc': {'weight': 8, 'category': 'tech'},
        'ai手机': {'weight': 8, 'category': 'tech'},
        '固态电池': {'weight': 8, 'category': 'tech'},
        'solid-state battery': {'weight': 8, 'category': 'tech'},
        '自动驾驶 v13': {'weight': 8, 'category': 'tech'},
        'fsd': {'weight': 8, 'category': 'tech'},
        '星舰商业化': {'weight': 8, 'category': 'tech'},
        'starship': {'weight': 8, 'category': 'tech'},
        # Actions
        '量产': {'weight': 7, 'category': 'tech'},
        'mass production': {'weight': 7, 'category': 'tech'},
        '突破': {'weight': 6, 'category': 'tech'},
        'breakthrough': {'weight': 6, 'category': 'tech'},
        # Bases
        '英伟达': {'weight': 5, 'category': 'tech'},
        'nvidia': {'weight': 5, 'category': 'tech'},
        '苹果': {'weight': 5, 'category': 'tech'},
        'apple': {'weight': 5, 'category': 'tech'},
        '华为': {'weight': 5, 'category': 'tech'},
        '特斯拉': {'weight': 5, 'category': 'tech'},
        'tesla': {'weight': 5, 'category': 'tech'},
        '先进封装': {'weight': 5, 'category': 'tech'},
        'advanced packaging': {'weight': 5, 'category': 'tech'},

        # ================= 🤖 AI 专题 (AI) =================
        # Combos (25/26趋势: 推理模型、智能体、物理AI)
        'ai推理': {'weight': 8, 'category': 'ai'},
        'ai reasoning': {'weight': 8, 'category': 'ai'},
        '智能体工作流': {'weight': 8, 'category': 'ai'},
        'agentic workflow': {'weight': 8, 'category': 'ai'},
        '具身智能': {'weight': 8, 'category': 'ai'},
        'embodied ai': {'weight': 8, 'category': 'ai'},
        '多模态': {'weight': 8, 'category': 'ai'},
        'multimodal': {'weight': 8, 'category': 'ai'},
        'sora': {'weight': 8, 'category': 'ai'},
        'agi': {'weight': 8, 'category': 'ai'},
        # Actions
        '开源模型': {'weight': 7, 'category': 'ai'},
        'open source model': {'weight': 7, 'category': 'ai'},
        '模型评测': {'weight': 6, 'category': 'ai'},
        'benchmark': {'weight': 6, 'category': 'ai'},
        # Bases (升级到2025/2026最强模型)
        'gpt-5': {'weight': 5, 'category': 'ai'},
        'claude 3.5': {'weight': 5, 'category': 'ai'},
        'gemini 3': {'weight': 5, 'category': 'ai'},
        'deepseek': {'weight': 5, 'category': 'ai'},
        'llama 3': {'weight': 5, 'category': 'ai'},
        'llama 4': {'weight': 5, 'category': 'ai'},
        '大模型': {'weight': 5, 'category': 'ai'},
        'llm': {'weight': 5, 'category': 'ai'},

        # ================= 💼 商业 (Business) =================
        # Combos (25/26趋势: AI回报率、降本增效、太空经济)
        'ai投资回报': {'weight': 8, 'category': 'business'},
        'ai roi': {'weight': 8, 'category': 'business'},
        '降本增效': {'weight': 8, 'category': 'business'},
        'cost reduction': {'weight': 8, 'category': 'business'},
        '太空经济': {'weight': 8, 'category': 'business'},
        'space economy': {'weight': 8, 'category': 'business'},
        '出海2.0': {'weight': 8, 'category': 'business'},
        'global expansion': {'weight': 8, 'category': 'business'},
        '反垄断拆分': {'weight': 8, 'category': 'business'},
        'antitrust breakup': {'weight': 8, 'category': 'business'},
        # Actions
        '财报超预期': {'weight': 7, 'category': 'business'},
        'earnings beat': {'weight': 7, 'category': 'business'},
        '并购': {'weight': 7, 'category': 'business'},
        'm&a': {'weight': 7, 'category': 'business'},
        'ipo复苏': {'weight': 6, 'category': 'business'},
        'ipo revival': {'weight': 6, 'category': 'business'},
        # Bases
        '字节跳动': {'weight': 5, 'category': 'business'},
        'bytedance': {'weight': 5, 'category': 'business'},
        '拼多多': {'weight': 5, 'category': 'business'},
        'pdd': {'weight': 5, 'category': 'business'},
        'openai': {'weight': 5, 'category': 'business'},

        # ================= 🏛️ 政治 (Politics) =================
        # Combos (25/26趋势: AI法案、关税升级、小院高墙)
        'ai安全法案': {'weight': 8, 'category': 'politics'},
        'ai safety act': {'weight': 8, 'category': 'politics'},
        '小院高墙': {'weight': 8, 'category': 'politics'},
        'small yard high fence': {'weight': 8, 'category': 'politics'},
        '关税壁垒': {'weight': 8, 'category': 'politics'},
        'tariff barriers': {'weight': 8, 'category': 'politics'},
        '出口管制': {'weight': 8, 'category': 'politics'},
        'export control': {'weight': 8, 'category': 'politics'},
        '科技冷战': {'weight': 8, 'category': 'politics'},
        'tech cold war': {'weight': 8, 'category': 'politics'},
        # Actions
        '制裁升级': {'weight': 7, 'category': 'politics'},
        'sanction': {'weight': 7, 'category': 'politics'},
        '否决': {'weight': 7, 'category': 'politics'},
        'veto': {'weight': 7, 'category': 'politics'},
        '补贴战': {'weight': 6, 'category': 'politics'},
        'subsidy war': {'weight': 6, 'category': 'politics'},
        # Bases (脱敏安全版)
        '中方高层': {'weight': 5, 'category': 'politics'},
        'chinese leadership': {'weight': 5, 'category': 'politics'},
        '美国政府': {'weight': 5, 'category': 'politics'},
        'us administration': {'weight': 5, 'category': 'politics'},
        '欧盟委员会': {'weight': 5, 'category': 'politics'},
        'eu commission': {'weight': 5, 'category': 'politics'}
    }
}

# ==================== 输出配置 ====================
OUTPUT_CONFIG = {
    'output_file': 'data/news.json',
    'top_n': 10,              # 输出Top N篇
    'min_score': 0.5,         # 最低分数要求
    'max_articles': 1000      # 处理的最大文章数
}

# 向下兼容 main.py
OUTPUT_FILE = OUTPUT_CONFIG['output_file']
TOP_N = OUTPUT_CONFIG['top_n']

# ==================== 分类显示配置 ====================
CATEGORY_CONFIG = {
    'tech': {
        'name_zh': '科技类',
        'name_en': 'Technology',
        'emoji': '🔧',
        'color': '#667eea'
    },
    'supply_chain': {
        'name_zh': '供应链',
        'name_en': 'Supply Chain',
        'emoji': '📦',
        'color': '#f093fb'
    },
    'politics': {
        'name_zh': '政治',
        'name_en': 'Politics',
        'emoji': '🏛️',
        'color': '#4facfe'
    },
    'ai': {
        'name_zh': 'AI专题',
        'name_en': 'AI',
        'emoji': '🤖',
        'color': '#43e97b'
    },
    'business': {
        'name_zh': '商业类',
        'name_en': 'Business',
        'emoji': '💼',
        'color': '#fa709a'
    }
}
