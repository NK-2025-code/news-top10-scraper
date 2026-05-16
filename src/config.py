# RSS源配置
RSS_SOURCES = [
    {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/feed/',
        'weight': 1.0
    },
    {
        'name': 'Caixin',
        'url': 'https://rsshub.app/caixin/article',
        'weight': 0.8
    },
    {
        'name': 'ReadHub',
        'url': 'https://rsshub.app/readhub/category/topic',
        'weight': 0.9
    }
]

# 输出配置
OUTPUT_FILE = 'data/news.json'
TOP_N = 10
