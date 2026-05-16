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
    
    # 💼 商业类 (3个源)
    {
        'name': '财新网',
        'url': 'https://rsshub.app/caixin/article',
        'weight': 0.85,
        'category': 'business'
    },
    {
        'name': '36氪',
        'url': 'https://rsshub.app/36kr/latest',
        'weight': 0.85,
        'category': 'business'
    },
    {
        'name': '投资界',
        'url': 'https://rsshub.app/investworld/news',
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
    
    # 关键词权重系统
    'keywords': {
        # 高权重关键词 (8分)
        'breakthrough': {'weight': 8, 'category': None},
        'revolution': {'weight': 8, 'category': None},
        'first': {'weight': 8, 'category': None},
        
        # 📦 科技型供应链 & 物流 (6-7分，权重提升)
        'supply chain': {'weight': 7, 'category': 'supply_chain'},
        'logistics': {'weight': 7, 'category': 'supply_chain'},
        'automation': {'weight': 7, 'category': 'supply_chain'}, # 新增：自动化
        'iot': {'weight': 6, 'category': 'tech'},                # 新增：物联网
        'robotics': {'weight': 6, 'category': 'tech'},           # 新增：机器人
        'shipping': {'weight': 6, 'category': 'supply_chain'},
        
        # 🤖 AI相关 (6-7分)
        'chatgpt': {'weight': 7, 'category': 'ai'},
        'gpt-4': {'weight': 7, 'category': 'ai'},
        'openai': {'weight': 6, 'category': 'ai'},
        'deepmind': {'weight': 6, 'category': 'ai'},
        'agi': {'weight': 7, 'category': 'ai'},
        'llm': {'weight': 6, 'category': 'ai'},
        
        # 💼 融资/商业 (5-6分)
        'funding': {'weight': 6, 'category': 'business'},
        'acquisition': {'weight': 6, 'category': 'business'},
        'investment': {'weight': 5, 'category': 'business'},
        'ipo': {'weight': 6, 'category': 'business'},
        
        # 🔧 技术 (5分)
        'technology': {'weight': 5, 'category': 'tech'},
        'innovation': {'weight': 4, 'category': 'tech'},
        
        # 🏛️ 政治 (3-4分)
        'policy': {'weight': 4, 'category': 'politics'},
        'government': {'weight': 3, 'category': 'politics'},
        'election': {'weight': 3, 'category': 'politics'},
    }
}

# ==================== 输出配置 ====================
OUTPUT_CONFIG = {
    'output_file': 'data/news.json',
    'top_n': 10,              # 输出Top N篇
    'min_score': 0.5,         # 最低分数要求
    'max_articles': 1000      # 处理的最大文章数
}

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
