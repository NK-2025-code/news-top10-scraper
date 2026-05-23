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
    
    # 🏛️ 政治 (4个顶级源，替换CNN，更专业客观)
    {
        'name': 'BBC News',
        'url': 'http://feeds.bbc.co.uk/news/world/rss.xml',
        'weight': 0.95,
        'category': 'politics'
    },
    {
        'name': 'The Guardian',
        'url': 'https://www.theguardian.com/world/rss',
        'weight': 0.95,
        'category': 'politics'
    },
    {
        'name': 'Politico',
        'url': 'https://rss.politico.com/politics-news.xml',
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
